import re

comment_pattern = r";",
identifier_pattern = r"([a-z]+)" # capture group for identifier (of label)
hex_byte_pattern = r"[\da-f]{2}"
label_pattern = identifier_pattern + r":",


# get hex address like "0f" of label, using line and index of instruction (see doc below)
def label_address(line: str, index: int) -> str:
    # TODO
    return "00"


# get content of first capture group, using pattern matching with line and index of instruction (see doc below)
def capture_group_content(line: str, index: int) -> str:
    return re.compile(instructions[index]["pattern"], re.IGNORECASE).match(line).group(1)


# get hex machinecode for resb instruction, using line and index of instruction (see doc below)
def resb_machinecode(line: str, index: int) -> str:
    return "00" * resb_bytes(line, index)


# get number of hex bytes for resb instruction, using line and index of instruction (see doc below)
def resb_bytes(line: str, index: int) -> int:
    return int(capture_group_content(line, index), 16)


instructions = [
    {
        # regex pattern to match line of assembly code
        "pattern": r"nop",
        # receives: line of assembly code (str), index in instruction array (int)
        # returns: hex bytes without spaces (str)
        "machinecode": lambda i1, i2: "02",
        # receives: line of assembly code (str), index in instruction array (int)
        # returns: number of hex bytes (int)
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"halt",
        "machinecode": lambda i1, i2: "03",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"in a",
        "machinecode": lambda i1, i2: "04",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"in b",
        "machinecode": lambda i1, i2: "05",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"out a",
        "machinecode": lambda i1, i2: "06",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"out b",
        "machinecode": lambda i1, i2: "07",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"inc a",
        "machinecode": lambda i1, i2: "08",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"inc b",
        "machinecode": lambda i1, i2: "09",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"add ab",
        "machinecode": lambda i1, i2: "0a",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"sub ab",
        "machinecode": lambda i1, i2: "0b",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"and ab",
        "machinecode": lambda i1, i2: "0c",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"or ab",
        "machinecode": lambda i1, i2: "0d",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"mov ba",
        "machinecode": lambda i1, i2: "0e",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"jmp " + identifier_pattern,
        "machinecode": lambda line, index: "0f" + label_address(line, index),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"breq " + identifier_pattern,
        "machinecode": lambda line, index: "12" + label_address(line, index),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"loadv a,\s*#(" + hex_byte_pattern + r")",
        "machinecode": lambda line, index: "15" + capture_group_content(line, index),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"load a,\s*" + identifier_pattern,
        "machinecode": lambda line, index: "18" + label_address(line, index),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"store " + identifier_pattern,
        "machinecode": lambda line, index: "1f" + label_address(line, index),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"equ #(" + hex_byte_pattern + r")",
        "machinecode": lambda line, index: "",
        "bytes": lambda i1, i2: 0,
    },
    {
        "pattern": r"db #(" + hex_byte_pattern + r")",
        "machinecode": lambda line, index: capture_group_content(line, index),
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"resb #(" + hex_byte_pattern + r")+",
        "machinecode": lambda line, index: resb_machinecode(line, index),
        "bytes": lambda line, index: resb_bytes(line, index),
    },
]

input_path = "input.txt"
output_path = "input.txt"

with open(input_path, "r") as file:
    input_lines = file.readlines()

for line_number, line in enumerate(input_lines):
    line = line.replace("\n", "")
    print(f"{line_number}: {line}")
