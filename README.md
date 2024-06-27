# [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture)-like assembler
A very simple two-pass assembler for a self-designed 8-bit CPU based on [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture).

Written in collaboration with [NilsPvR](https://github.com/NilsPvR).

### Prerequisites
- `python` is installed / accessible

### Installation
Get the code, e.g. by running
```sh
git clone https://github.com/julius-boettger/mips-like-assembler
```

### Usage
- Write assembly in a file, e.g. `input.txt` (see [considerations](#considerations-when-coding-for-this-assembler) and [instructions](#supported-instructions) below)
    - `input.txt` in this repo is an example program
- Set `input_path` in `main.py` to the path to your file, e.g. `"/path/to/input.txt"`
- Optionally set `output_path` in `main.py` to something other than `output.txt`
- Run `python main.py`
- Optionally load the output file into your CPUs RAM in [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution)

## Considerations when coding for this assembler
- Labels have to be followed by an instruction _on the same line_, e.g. `my_label: nop`
- The entire code is case-insensitive (even the labels!)
- Use empty lines and extra spaces where you feel like it, they will be ignored
- Place comments anywhere (starting with `;`) like usual

## Supported instructions
Parameters are one of the following:
- `[value]`: A number in hexadecimal notation, usually one byte at most, e.g. `0`, `a`, `1c`, `ff`
- `[label]`: A self-defined label, which will be replaced with the memory address it is pointing to, e.g. `start`, `loop`, `else`, `finally`
    - Labels can contain letters (a-z), numbers (0-9) and underscores, but may not start with a number

| Instruction | Description (sometimes C-equivalent) |
| ----------- | ----------- |
| `nop` | No operation |
| `halt` | Halt program |
| `in a`, `input a` | `a = input` |
| `in b`, `input b` | `b = input` |
| `out a`, `output a` | `output = a` |
| `out b`, `output b` | `output = b` |
| `inc a` | `a++` |
| `inc b` | `b++` |
| `add ab` | `a = a + b` |
| `sub ab` | `a = a - b` |
| `and ab` | `a = a & b` |
| `or ab` | `a = a \| b` |
| `mov ba` | `b = a` |
| `jmp [label]` | Jump to `[label]` |
| `beq [label]` | "Branch if equal", jump to `[label]` if `a == b` |
| `loadi a, #[value]` | "Load immediate", `a = value` |
| `loadi a, [label]` | "Load immediate", `a = label` |
| `load a, [label]` | `a = value_at(label)`, `b = address_of_next_instruction` |
| `store [label], a` | `value_at(label) = a`, `b = address_of_next_instruction` |
| `db #[value]` | "Define byte", write `[value]` to memory (usually used with label) |
| `db [label]` | "Define byte", write address of `[label]` to memory (usually used with label) |
| `resb #[value]`, `ds #[value]` | "Reserve bytes" / "data space", write byte `00` to memory `[value]` times (usually used with label) |
| `[label]: equ #[value]` | "Equate", define constant named `[label]` to be used during assembly process, e.g. `constant: equ #1` and `loadv a, constant` |