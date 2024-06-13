import re

identifier_pattern = r"\w+"
label_pattern = identifier_pattern + r":",

instructions = [
    {
        "name": r"nop",
        "opcode": "02",
    },
    {
        "name": r"halt",
        "opcode": "03",
    },
    {
        "name": r"in a",
        "opcode": "04",
    },
    {
        "name": r"in b",
        "opcode": "05",
    },
    {
        "name": r"out a",
        "opcode": "06",
    },
    {
        "name": r"out b",
        "opcode": "07",
    },
    {
        "name": r"inc a",
        "opcode": "08",
    },
    {
        "name": r"inc b",
        "opcode": "09",
    },
    {
        "name": r"add ab",
        "opcode": "0a",
    },
    {
        "name": r"sub ab",
        "opcode": "0b",
    },
    {
        "name": r"and ab",
        "opcode": "0c",
    },
    {
        "name": r"or ab",
        "opcode": "0d",
    },
    {
        "name": r"mov ba",
        "opcode": "0e",
    },
    {
        "name": r"jmp " + identifier_pattern,
        "opcode": "0f",
    },
    {
        "name": r"breq " + identifier_pattern,
        "opcode": "12",
    },
    {
        "name": r"load a,\s*#[\da-f]{2}",
        "opcode": "15",
    },
    {
        "name": r"load a,\s*" + identifier_pattern,
        "opcode": "18",
    },
    {
        "name": r"store " + identifier_pattern,
        "opcode": "1f",
    },
]

print(instructions)