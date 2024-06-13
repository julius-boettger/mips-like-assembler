import re

comment_pattern = r";",
identifier_pattern = r"([a-z]+)" # capture group for identifier (of label)
hex_byte_pattern = r"[\da-f]{2}"
label_pattern = identifier_pattern + r":",


# get hex address like "0f" of label, using line and index of instruction (see doc below)
def label_address(line: str, index: int) -> str:
    # TODO
    return "00"


# get content of capture group, using pattern matching with line and index of instruction (see doc below)
def capture_group_content(line: str, index: int) -> str:
    # TODO
    return "00"


# get hex machinecode for resb instruction, using line and index of instruction (see doc below)
def resb_machinecode(line: str, index: int) -> str:
    # TODO
    return "00"


instructions = [
    {
        # regex pattern to match line of assembly code
        "pattern": r"nop",
        # receives: line of assembly code (str), index in instruction array (int)
        # returns: hex bytes without spaces (str)
        "machinecode": lambda i1, i2: "02",
    },
    {
        "pattern": r"halt",
        "machinecode": lambda i1, i2: "03",
    },
    {
        "pattern": r"in a",
        "machinecode": lambda i1, i2: "04",
    },
    {
        "pattern": r"in b",
        "machinecode": lambda i1, i2: "05",
    },
    {
        "pattern": r"out a",
        "machinecode": lambda i1, i2: "06",
    },
    {
        "pattern": r"out b",
        "machinecode": lambda i1, i2: "07",
    },
    {
        "pattern": r"inc a",
        "machinecode": lambda i1, i2: "08",
    },
    {
        "pattern": r"inc b",
        "machinecode": lambda i1, i2: "09",
    },
    {
        "pattern": r"add ab",
        "machinecode": lambda i1, i2: "0a",
    },
    {
        "pattern": r"sub ab",
        "machinecode": lambda i1, i2: "0b",
    },
    {
        "pattern": r"and ab",
        "machinecode": lambda i1, i2: "0c",
    },
    {
        "pattern": r"or ab",
        "machinecode": lambda i1, i2: "0d",
    },
    {
        "pattern": r"mov ba",
        "machinecode": lambda i1, i2: "0e",
    },
    {
        "pattern": r"jmp " + identifier_pattern,
        "machinecode": lambda line, index: "0f" + label_address(line, index),
    },
    {
        "pattern": r"breq " + identifier_pattern,
        "machinecode": lambda line, index: "12" + label_address(line, index),
    },
    {
        "pattern": r"load a,\s*#(" + hex_byte_pattern + r")",
        "machinecode": lambda line, index: "15" + capture_group_content(line, index),
    },
    {
        "pattern": r"load a,\s*" + identifier_pattern,
        "machinecode": lambda line, index: "18" + label_address(line, index),
    },
    {
        "pattern": r"store " + identifier_pattern,
        "machinecode": lambda line, index: "1f" + label_address(line, index),
    },
    {
        "pattern": r"db #(" + hex_byte_pattern + r")",
        "machinecode": lambda line, index: capture_group_content(line, index),
    },
    {
        "pattern": r"resb #(" + hex_byte_pattern + r")+",
        "machinecode": lambda line, index: resb_machinecode(line, index)
    },
]

input_path = "input.txt"
output_path = "input.txt"

with open(input_path, "r") as file:
    input_lines = file.readlines()

for line_number, line in enumerate(input_lines):
    line = line.replace("\n", "")
    print(f"{line_number}: {line}")
