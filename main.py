import re

identifier_pattern = r"([a-z]+)" # capture group for identifier (of label)
hex_byte_pattern = r"[\da-f]{2}"
label_pattern = identifier_pattern + r": "


# get 1 byte hex address like "0f" of label, using line and pattern of instruction (see doc below)
def label_address(line: str, pattern: str) -> str:
    return "%0.2x" % label_table[capture_group_content(line, pattern)]


# get content of first capture group, using pattern matching with line and pattern of instruction (see doc below)
def capture_group_content(line: str, pattern: str) -> str:
    return re.compile(pattern, re.IGNORECASE).search(line).group(1)


# get hex machinecode for resb instruction, using line and pattern of instruction (see doc below)
def resb_machinecode(line: str, pattern: str) -> str:
    return "00" * resb_bytes(line, pattern)


# get number of hex bytes for resb instruction, using line and pattern of instruction (see doc below)
def resb_bytes(line: str, pattern: str) -> int:
    return int(capture_group_content(line, pattern), 16)


instructions = [
    {
        # regex pattern to match line of assembly code
        "pattern": r"nop",
        # receives: line of assembly code (str), pattern of instruction (str)
        # returns: hex bytes without spaces (str)
        "machinecode": lambda i1, i2: "02",
        # receives: line of assembly code (str), pattern in instruction array (int)
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
        "machinecode": lambda line, pattern: "0f" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"breq " + identifier_pattern,
        "machinecode": lambda line, pattern: "12" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"loadv a,\s*#(" + hex_byte_pattern + r")",
        "machinecode": lambda line, pattern: "15" + capture_group_content(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"load a,\s*" + identifier_pattern,
        "machinecode": lambda line, pattern: "18" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"store " + identifier_pattern,
        "machinecode": lambda line, pattern: "1f" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"equ #(" + hex_byte_pattern + r")",
        "machinecode": lambda line, pattern: "",
        "bytes": lambda i1, i2: 0,
    },
    {
        "pattern": r"db #(" + hex_byte_pattern + r")",
        "machinecode": lambda line, pattern: capture_group_content(line, pattern),
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"resb #(" + hex_byte_pattern + r")+",
        "machinecode": lambda line, pattern: resb_machinecode(line, pattern),
        "bytes": lambda line, pattern: resb_bytes(line, pattern),
    },
]


def remove_comment(line: str) -> str:
    i = line.find(";")
    if i == -1:
        return line
    return line[:i]


def space_every_two(string: str) -> str:
    return " ".join(re.findall(r"..", string))


input_path = "input.txt"
output_path = "input.txt"

# read file
with open(input_path, "r") as file:
    input_lines = file.readlines()

# first pass: register labels
ilc = 0
label_table = {
    #"label_name": address_in_ram (int)
}
for line_number, line in enumerate(input_lines):
    line_number += 1 # dont count from 0
    line = remove_comment(line.replace("\n", ""))

    # match valid assembly code line with instruction (and possibly a label too)
    instruction_match = None
    for instruction in instructions:
        pattern = r"^\s*(?:" + label_pattern + r")?\s*" + instruction["pattern"] + r"\s*$"
        match = re.compile(pattern, re.IGNORECASE).fullmatch(line)
        if match is not None:
            instruction_match = {
                "match": match,
                "instruction": instruction,
            }

    if instruction_match is not None:
        instruction = instruction_match["instruction"]
        label = instruction_match["match"].group(1)
        # label was found
        if label is not None:
            if "equ" in instruction["pattern"]:
                label_table[label] = int(capture_group_content(line, instruction["pattern"]), 16)
            else:
                label_table[label] = ilc
        ilc += instruction["bytes"](line, instruction["pattern"])
    elif re.compile(r"^\s*$", re.IGNORECASE).fullmatch(line) is None:
        print(f"line {line_number} is invalid!")
        exit(1)

# second pass: translate to machine code
output = "" # machine code in hex without spaces like "0f0f0f0f"
for line_number, line in enumerate(input_lines):
    line_number += 1 # dont count from 0
    line = remove_comment(line.replace("\n", ""))

    # match valid assembly code line with instruction (and possibly a label too)
    instruction_match = None
    for instruction in instructions:
        pattern = r"^\s*(?:" + label_pattern + r")?\s*" + instruction["pattern"] + r"\s*$"
        match = re.compile(pattern, re.IGNORECASE).fullmatch(line)
        if match is not None:
            instruction_match = {
                "match": match,
                "instruction": instruction,
            }

    if instruction_match is not None:
        instruction = instruction_match["instruction"]
        machinecode = instruction["machinecode"](line, instruction["pattern"])
        if machinecode != "":
            print(f'{line_number}: {instruction_match["match"].group(0)} ; => {space_every_two(machinecode)}')
        output += machinecode

print("\nSuccessfully assembled. Machine code:\n" + space_every_two(output))
