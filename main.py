import re

input_path = "input.txt"
output_path = "output.txt"

identifier_pattern = r"([_a-z]\w*)" # capture group for identifier (of label)
hex_byte_pattern = r"[\da-f]{1,2}"
label_pattern = identifier_pattern + r"\s*:"


# remove comment from a line of code
def remove_comment(line: str) -> str:
    i = line.find(";")
    if i == -1:
        return line
    return line[:i]


# put spaces in a string every 2 chars, e.g. "000000" => "00 00 00"
def space_every_two(string: str) -> str:
    return " ".join(re.findall(r"..", string))


# append "0" to beginning of string if its length is 1, e.g. "a" => "0a"
def two_hex_chars(string: str) -> str:
    if len(string) == 1:
        return "0" + string
    return string


# get 1 byte hex address like "0f" of label, using line and pattern of instruction (see doc below)
def label_address(line: str, pattern: str) -> str:
    return "%0.2x" % label_table[capture_group_content(line, pattern)]


# get content of first capture group, using pattern matching with line and pattern of instruction (see doc below)
def capture_group_content(line: str, pattern: str) -> str:
    return re.compile(pattern, re.IGNORECASE).search(line).group(1).lower()


# get hex machinecode for resb instruction, using line and pattern of instruction (see doc below)
def resb_machinecode(line: str, pattern: str) -> str:
    return "00" * resb_bytes(line, pattern)


# get number of hex bytes for resb instruction, using line and pattern of instruction (see doc below)
def resb_bytes(line: str, pattern: str) -> int:
    return int(capture_group_content(line, pattern), 16)


# shared code of both assembler passes
def pass_setup() -> dict:
    global line_number
    line_number += 1 # dont count from 0
    global line
    line = remove_comment(line.replace("\n", "")).strip().lower()

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
    return instruction_match


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
        "pattern": r"in\s+a",
        "machinecode": lambda i1, i2: "04",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"in\s+b",
        "machinecode": lambda i1, i2: "05",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"out\s+a",
        "machinecode": lambda i1, i2: "06",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"out\s+b",
        "machinecode": lambda i1, i2: "07",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"inc\s+a",
        "machinecode": lambda i1, i2: "08",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"inc\s+b",
        "machinecode": lambda i1, i2: "09",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"add\s+ab",
        "machinecode": lambda i1, i2: "0a",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"sub\s+ab",
        "machinecode": lambda i1, i2: "0b",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"and\s+ab",
        "machinecode": lambda i1, i2: "0c",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"or\s+ab",
        "machinecode": lambda i1, i2: "0d",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"mov\s+ba",
        "machinecode": lambda i1, i2: "0e",
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"jmp\s+" + identifier_pattern,
        "machinecode": lambda line, pattern: "0f" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"breq\s+" + identifier_pattern,
        "machinecode": lambda line, pattern: "12" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"loadv\s+a\s*,\s*#(" + hex_byte_pattern + r")",
        "machinecode": lambda line, pattern: "15" + two_hex_chars(capture_group_content(line, pattern)),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"loadv\s+a\s*,\s*" + identifier_pattern,
        "machinecode": lambda line, pattern: "15" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"load\s+a\s*,\s*" + identifier_pattern,
        "machinecode": lambda line, pattern: "18" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"store\s+" + identifier_pattern + r"\s*,\s*a",
        "machinecode": lambda line, pattern: "1f" + label_address(line, pattern),
        "bytes": lambda i1, i2: 2,
    },
    {
        "pattern": r"equ\s+#(" + hex_byte_pattern + r")",
        "machinecode": lambda line, pattern: "",
        "bytes": lambda i1, i2: 0,
    },
    {
        "pattern": r"db\s+#(" + hex_byte_pattern + r")",
        "machinecode": lambda line, pattern: two_hex_chars(capture_group_content(line, pattern)),
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"db\s+" + identifier_pattern,
        "machinecode": lambda line, pattern: label_address(line, pattern),
        "bytes": lambda i1, i2: 1,
    },
    {
        "pattern": r"resb\s+#(" + hex_byte_pattern + r")+",
        "machinecode": lambda line, pattern: resb_machinecode(line, pattern),
        "bytes": lambda line, pattern: resb_bytes(line, pattern),
    },
]


# read file
with open(input_path, "r") as file:
    input_lines = file.readlines()

# first pass: register labels
ilc = 0
label_table = {
    #"label_name": address_in_ram (int)
}
for line_number, line in enumerate(input_lines):
    instruction_match = pass_setup()
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
        if ilc > 2**8:
            print(f"\033[91mError\033[0m: Translating line {line_number} would result in a program that exceeds the memory capacity ({2**8} bytes)")
            exit(1)
    elif re.compile(r"^\s*$", re.IGNORECASE).fullmatch(line) is None:
        print(f"\033[91mError\033[0m: Line {line_number} is syntactically invalid")
        exit(1)

# second pass: translate to machine code
output = "" # machine code in hex without spaces like "0f0f0f0f"
for line_number, line in enumerate(input_lines):
    instruction_match = pass_setup()
    if instruction_match is not None:
        instruction = instruction_match["instruction"]

        try:
            machinecode = instruction["machinecode"](line, instruction["pattern"])
        # if referencing a label that was never defined
        except KeyError:
            print(f'\033[91mError\033[0m: Line {line_number} is referencing a label that was never defined: {capture_group_content(line, instruction["pattern"])}')
            exit(1)

        if machinecode != "":
            print(f'{line_number}: {instruction_match["match"].group(0)} ; => {space_every_two(machinecode)}')
        output += machinecode

# make output readable with logisim evolution
output = "v3.0 hex words plain\n" + space_every_two(output)

# write file
with open(output_path, "w") as file:
    file.writelines(output)

print(f"\n\033[92mSuccess\033[0m. Wrote file {output_path} with machine code:\n" + output)
