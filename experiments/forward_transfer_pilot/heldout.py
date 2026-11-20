"""Independent reference formulas for the fixed four-bit task families."""

FAMILIES = {
    "retained-parity": {
        "p01": ("inverted left parity cyclic footer", lambda x: (2 * (15 ^ ((2 * x) % 16))) % 16 + (15 ^ ((2 * x) % 16)) // 8),
        "p02": ("masked inverted left field", lambda x: (15 - ((2 * x) % 16)) % 8),
        "p03": ("left flag from inverted shifted word", lambda x: (2 * (15 - ((2 * x) % 16))) % 16),
    },
    "wrapped-coordinate": {
        "w01": ("cyclic low field then multiply coordinate", lambda x: 2 * (((2 * x) % 16 + x // 8) % 8)),
        "w02": ("fold wrapped low field into pair", lambda x: (((2 * x) % 16 + x // 8) % 8) // 2),
        "w03": ("wrapped low coordinate with two flags", lambda x: (((2 * x) % 16 + x // 8) % 8) ^ 9),
    },
    "mixed-signal": {
        "m01": ("transit inverted marker high bit polarity", lambda x: (15 - ((2 * x) % 16)) ^ 9),
        "m02": ("packet rotate low marker high bit cyclic", lambda x: (2 * ((((2 * x) % 16 + x // 8) % 8) ^ 8)) % 16 + 1),
        "m03": ("flip high marker right cyclic shift twice", lambda x: (4 * ((x ^ 8) // 2)) % 16 + ((x ^ 8) // 2) // 4),
    },
    "out-of-family": {
        "a01": ("square ordinal with modular carry", lambda x: x * x % 16),
        "a02": ("count flags in the word", lambda x: x.bit_count()),
        "a03": ("reverse four coordinate bits", lambda x: sum(((x >> n) & 1) << (3 - n) for n in range(4))),
    },
}

OPERATIONS = {
    "left": lambda word: word[1:] + "0",
    "right": lambda word: "0" + word[:-1],
    "rotate": lambda word: word[1:] + word[0],
    "low": lambda word: "0" + word[1:],
    "flip": lambda word: "".join("0" if bit == "1" else "1" for bit in word),
    "odd": lambda word: word[:-1] + ("0" if word[-1] == "1" else "1"),
    "high": lambda word: ("0" if word[0] == "1" else "1") + word[1:],
}


def verify(program, expected):
    operations = 0
    for word, output in enumerate(expected):
        encoded = format(word, "04b")
        for command in program:
            encoded = OPERATIONS[command](encoded)
            operations += 1
        if int(encoded, 2) != output:
            return {"input": word, "expected": output, "actual": int(encoded, 2)}, operations
    return None, operations
