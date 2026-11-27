"""Run a deterministic SyGuS transfer comparison; Z3 checks full-domain equivalence."""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random
import re
import subprocess
import time
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
MASK = 2**32 - 1
OPS = ("bvnot", "bvneg", "bvand", "bvor", "bvxor", "bvsub", "bvadd",
       "bvlshr", "bvashr", "bvshl", "bvmul", "bvudiv")
HISTORY = ("hd-01", "hd-02", "hd-04", "hd-06")
FAMILIES = {"low-bit": (3, 5, 7, 8, 17, 20), "signed": (9, 13),
            "averages": (14, 15), "permutation": (19,)}
SAMPLES = 24


def parse(source):
    stack = [[]]
    for word in re.findall(r"\(|\)|[^()\s]+", re.sub(r";[^\n]*", "", source)):
        if word == "(":
            stack.append([])
        elif word == ")":
            expr = tuple(stack.pop())
            stack[-1].append(expr)
        else:
            stack[-1].append(word)
    if len(stack) != 1:
        raise ValueError("Unbalanced input")
    return stack[0]


def fmt(t):
    return t if isinstance(t, str) else "(" + " ".join(map(fmt, t)) + ")"


def walk(t):
    yield t
    if isinstance(t, tuple):
        for child in t[1:]:
            yield from walk(child)


def substitute(t, arg):
    if isinstance(t, str):
        return arg if t == "x" else t
    return (t[0], *(substitute(c, arg) for c in t[1:]))


def smt(script):
    out = subprocess.run(["z3", "-in", "-T:8"], input="(set-logic QF_BV)\n" + script,
                         text=True, capture_output=True, check=True)
    if "(error" in out.stdout:
        raise ValueError(out.stdout)
    return out.stdout.strip()


def different(args, a, b):
    decl = "".join(f"(declare-const {x} (_ BitVec 32))\n" for x in args)
    return smt(decl + f"(assert (distinct {fmt(a)} {fmt(b)}))\n(check-sat)")


def load(cache):
    cache.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((HERE / "inputs.json").read_text())
    tasks = {}
    for row in manifest["files"]:
        file = cache / Path(row["path"]).name
        if not file.exists():
            url = f'https://raw.githubusercontent.com/SyGuS-Org/benchmarks/{manifest["revision"]}/{row["path"]}'
            with urlopen(url, timeout=30) as response:
                data = response.read()
        else:
            data = file.read_bytes()
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError(row["id"])
        if not file.exists():
            file.write_bytes(data)
        forms = {r[0]: r for r in parse(data.decode())}
        _, name, args, _, body = forms["define-fun"]
        grammar = forms["synth-fun"][-1][0][2]
        names = tuple(k for k, _ in args)
        if forms["constraint"][1] != ("=", (name, *names), ("f", *names)):
            raise ValueError("Unsupported specification " + name)
        tasks[row["id"]] = (names, body, grammar)
    return tasks


def library(tasks):
    history = [tasks[k][1] for k in HISTORY]
    counts = Counter(node for tree in history for node in list(walk(tree))[1:] if isinstance(node, tuple))
    routines = sorted(counts, key=lambda t: (-counts[t], fmt(t)))[:2]
    return {"none": [], "whole": history[:2], "routines": routines}, sum(len(list(walk(t))) for t in history)


def examples(args):
    rng = random.Random(417 + len(args))
    edge = [0, 1, 2, 3, 7, 8, 15, 16, 31, MASK, MASK-1, 1 << 31]
    return [tuple(edge[(i + j*3) % len(edge)] if i < len(edge) else rng.getrandbits(32)
                  for j in range(len(args))) for i in range(SAMPLES)]


def operate(op, a, b=0):
    if op == "bvnot": return MASK ^ a
    if op == "bvneg": return -a & MASK
    if op == "bvand": return a & b
    if op == "bvor": return a | b
    if op == "bvxor": return a ^ b
    if op == "bvsub": return (a-b) & MASK
    if op == "bvadd": return (a+b) & MASK
    if op == "bvmul": return (a*b) & MASK
    if op == "bvudiv": return a//b if b else MASK
    if op == "bvshl": return (a << b) & MASK if b < 32 else 0
    if op == "bvlshr": return a >> min(b, 32)
    if op == "bvashr": return ((a if a < 2**31 else a-2**32) >> min(b,32)) & MASK
    raise ValueError(op)


def evaluate(t, env):
    if isinstance(t, str):
        return int(t[2:],16) if t.startswith("#x") else env[t]
    return operate(t[0], *(evaluate(c, env) for c in t[1:]))


def proposals(size, pool, grammar, macros, schedule):
    for leaf in grammar:
        if size == 1 and isinstance(leaf, str):
            yield leaf
    for op in OPS:
        if (op, "Start") in grammar:
            for a in pool.get(size-1, ()):
                yield op, a
        elif (op, "Start", "Start") in grammar:
            for k in range(1, size-1):
                for a in pool.get(k, ()):
                    for b in pool.get(size-1-k, ()):
                        yield op, a, b
    for tree in macros:
        nodes = list(walk(tree))
        holes = nodes.count("x")
        if schedule == "handles":
            key = size-1
        else:
            remainder = size - (len(nodes)-holes)
            if remainder % holes:
                continue
            key = remainder//holes
        for a in pool.get(key, ()):
            yield substitute(tree, a)


def search(task, macros, schedule):
    args, spec, grammar = task
    samples = examples(args)
    # Z3 evaluates the upstream targets; search only receives the example vector.
    queries = "".join("(simplify " + fmt(replace_vars(spec, {k:f"#x{v:08x}" for k,v in zip(args,x)})) + ")\n"
                      for x in samples)
    target = tuple(int(s[2:],16) for s in smt(queries).splitlines())
    if len(target) != SAMPLES: raise ValueError("Unexpected oracle response")
    envs = [dict(zip(args,x)) for x in samples]
    probes = work = checks = verify_ns = 0
    pool, seen = defaultdict(list), set()
    start = time.perf_counter_ns()
    def finish(reason, tree=None):
        return dict(stop=reason, solution=fmt(tree) if tree else None, proposals=probes,
                    screen_ops=work, solver_checks=checks, verify_ns=verify_ns,
                    search_ns=time.perf_counter_ns()-start-verify_ns)
    size = 1
    while True:
        for tree in proposals(size,pool,grammar,macros,schedule):
            needed = SAMPLES * sum(isinstance(t,tuple) for t in walk(tree))
            if probes == 12000: return finish("proposal cap")
            if work + needed > 1500000: return finish("work cap")
            probes += 1
            work += needed
            signature = tuple(evaluate(tree,e) for e in envs)
            if signature in seen: continue
            if signature == target:
                tick = time.perf_counter_ns()
                verdict = different(args,spec,tree)
                verify_ns += time.perf_counter_ns()-tick
                checks += 1
                if verdict == "unsat": return finish("verified",tree)
                # Another candidate matching all examples may pass the universal check.
                if verdict not in ("sat","unknown","timeout"): raise ValueError(verdict)
            else:
                seen.add(signature)
            pool[size].append(tree)
        size += 1


def replace_vars(t, table):
    if isinstance(t,str): return table.get(t,t)
    return (t[0], *(replace_vars(c,table) for c in t[1:]))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("cache",type=Path)
    ap.add_argument("--freeze-library",action="store_true")
    opts=ap.parse_args()
    tasks=load(opts.cache)
    libraries,cost=library(tasks)
    frozen={name:[fmt(t) for t in trees] for name,trees in libraries.items()}
    if opts.freeze_library:
        print(json.dumps(frozen,indent=2));return
    if json.loads((HERE/"library.json").read_text()) != frozen: raise ValueError("Library differs")
    pairs=0
    for a,b in combinations(tasks.values(),2):
        if a[0]==b[0]:
            if different(a[0],a[1],b[1]) != "sat": raise ValueError("Redundant or undecided target pair")
            pairs+=1
    cases=[]
    for family, ids in FAMILIES.items():
        for num in ids:
            name=f"hd-{num:02d}"
            args,_,grammar=tasks[name]
            for arm,trees in libraries.items():
                legal=set(t if isinstance(t,str) else t[0] for t in grammar)
                if any((n[0] if isinstance(n,tuple) else n) not in legal for t in trees for n in walk(t)):
                    raise ValueError("Incompatible macro for "+name)
                for schedule in ("handles","expanded"):
                    cases.append(dict(task=name,family=family,arm=arm,schedule=schedule,
                                      **search(tasks[name],trees,schedule)))
    print(json.dumps(dict(solver=subprocess.check_output(["z3","-version"],text=True).strip(),
        deduplicated_pairs=pairs,history_nodes=cost,stored_nodes={k:sum(len(list(walk(t))) for t in v) for k,v in libraries.items()},cases=cases),indent=2))


if __name__ == "__main__":
    main()
