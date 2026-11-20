"""Fixed later targets and a full-domain interpreter independent of search."""

DOMAIN = range(32)

def rol(x):
    return (2 * x) % 32 + x // 16

def inv(x):
    return 31 - x

FAMILIES = {
    "board-routing": {
        "b21": ("inverted shift mirror board rotate twice", lambda x: rol(rol(inv((2*x) % 32)))),
        "b22": ("mirror complementary board suffix masked", lambda x: ((inv((2*x) % 32) ^ 1) // 2) % 16),
        "b23": ("gray shade rotated palette rise", lambda x: (2 * inv(rol(x))) % 32),
        "b24": ("inverse pulse serial track right mask", lambda x: inv(rol(x ^ 1)) // 2),
    },
    "cell-address": {
        "c21": ("cyclic low grid coordinate variant", lambda x: rol((rol(x) % 16) ^ 16)),
        "c22": ("coordinate grid low marker fold", lambda x: ((rol(x) % 16) ^ 1) // 2),
        "c23": ("high intake register bank clipped", lambda x: inv((x ^ 16) // 2) % 16),
        "c24": ("register intake right fold tag", lambda x: rol((x ^ 16) // 2) ^ 1),
    },
    "display-code": {
        "d21": ("right shifted marker parity offset", lambda x: (2 * ((x // 2) ^ 1)) % 32),
        "d22": ("offset right parity under clipping", lambda x: inv((x // 2) ^ 1) % 16),
        "d23": ("serial odd pulse track inversion", lambda x: inv(rol(x ^ 1)) ^ 16),
        "d24": ("shade rotate palette complementary flag", lambda x: (inv(rol(x)) ^ 1) ^ 16),
    },
    "adverse-mixing": {
        "a21": ("number of active display flags", lambda x: x.bit_count()),
        "a22": ("square a display value modulo width", lambda x: x * x % 32),
        "a23": ("reverse the positions of bits", lambda x: sum(((x >> n) & 1) << (4 - n) for n in range(5))),
        "a24": ("combine adjacent field changes", lambda x: x ^ (x // 2)),
    },
}

def toggle(bit):
    return "0" if bit == "1" else "1"

OPERATIONS = {
    "left": lambda word: word[1:] + "0",
    "right": lambda word: "0" + word[:-1],
    "roll": lambda word: word[1:] + word[0],
    "low": lambda word: "0" + word[1:],
    "flip": lambda word: "".join(map(toggle, word)),
    "odd": lambda word: word[:-1] + toggle(word[-1]),
    "high": lambda word: toggle(word[0]) + word[1:],
}

def verify(program, expected):
    witness = None
    for word, target in zip(DOMAIN, expected, strict=True):
        value = format(word, "05b")
        for op in program:
            value = OPERATIONS[op](value)
        actual = int(value, 2)
        if actual != target and witness is None:
            witness = {"input": word, "expected": target, "observed": actual}
    return witness
