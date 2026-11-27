"""Collect a fresh loopback release observation. Replay the retained rows with score.py."""
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import itertools
import json
import multiprocessing
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import time
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ARMS = ("primary_only", "direct", "gateway")


def read(port, route):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        conn.request("GET", route)
        response = conn.getresponse()
        body = response.read()
        return (response.status, body, int(response.getheader("Inner-Requests", 0)),
                int(response.getheader("Inner-Bytes", 0)))
    finally:
        conn.close()


def lookup(primary, observer, route, fallback):
    status, body, _, _ = read(primary, route)
    size = len(body)
    if status == 503 and fallback:
        status, body, _, _ = read(observer, route)
        return status, body, 2, size + len(body)
    return status, body, 1, size


def serve(pipe, role, root, primary=None, observer=None):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            name = self.path.removeprefix("/")
            if not name.isalnum():
                self.send_error(400)
                return
            inner = size = 0
            if role == "gateway":
                status, body, inner, size = lookup(primary, observer, self.path, True)
            else:
                cell = Path(root) / name
                if (cell / (role + ".down")).exists():
                    status, body = 503, b"unavailable"
                elif (cell / "published.md").exists():
                    status, body = 200, hashlib.sha256((cell / "published.md").read_bytes()).hexdigest().encode()
                else:
                    status, body = 404, b"absent"
            self.send_response(status)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Inner-Requests", str(inner))
            self.send_header("Inner-Bytes", str(size))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        pipe.send(server.server_port)
        pipe.close()
        server.serve_forever()


def collect():
    cohort = json.loads((HERE / "cohort.json").read_text())
    inputs = []
    for task in cohort:
        with urlopen(task["url"], timeout=30) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != task["sha256"]:
            raise ValueError(task["repo"])
        inputs.append(data)
    rows = []
    with TemporaryDirectory() as root:
        processes = []

        def start(role, *ports):
            receive, send = multiprocessing.Pipe(duplex=False)
            process = multiprocessing.Process(target=serve, args=(send, role, root, *ports))
            process.start()
            processes.append(process)
            try:
                if not receive.poll(10):
                    raise RuntimeError("Observer failed to start")
                return receive.recv()
            finally:
                receive.close()
                send.close()

        try:
            primary, observer = start("primary"), start("observer")
            gateway = start("gateway", primary, observer)
            conditions = itertools.product(range(len(inputs)), ("exact", "absent", "wrong"),
                                           ("up", "down"), ("shared", "separate"))
            for i, (task, effect, availability, source) in enumerate(conditions):
                arms = {}
                for j in range(len(ARMS)):
                    arm = ARMS[(i+j) % len(ARMS)]
                    name = f"task{i}arm{j}"
                    cell = Path(root) / name
                    cell.mkdir()
                    if availability == "down":
                        (cell / "primary.down").touch()
                        if source == "shared":
                            (cell / "observer.down").touch()
                    published = cell / "published.md"
                    staged = cell / "incoming.md"
                    staged.write_bytes(inputs[task] if effect != "wrong" else inputs[(task+1) % len(inputs)])
                    if effect != "absent":
                        staged.replace(published)
                    # The caller has no acknowledgement identifying which bytes committed.
                    start_ns = time.perf_counter_ns()
                    if arm == "gateway":
                        status, body, inner, size = read(gateway, "/" + name)
                        caller, requests, size = 1, inner + 1, size + len(body)
                    else:
                        status, body, requests, size = lookup(primary, observer, "/" + name, arm == "direct")
                        caller = requests
                    elapsed = time.perf_counter_ns() - start_ns
                    observed = body.decode()
                    closed = status == 200 and observed == cohort[task]["sha256"]
                    truth = published.exists() and published.read_bytes() == inputs[task]
                    arms[arm] = dict(status=status, observed=observed, closed=closed, truth=truth,
                                     caller_requests=caller, requests=requests, body_bytes=size, elapsed_ns=elapsed)
                rows.append(dict(id=f"{cohort[task]['repo'].split('/')[1]}-{effect}-{availability}-{source}",
                                 task=cohort[task]["repo"], effect=effect, primary=availability, fallback=source, arms=arms))
        finally:
            for process in processes:
                process.terminate()
                process.join()
    return rows


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
