# [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture)-like assembler
A very simple two-pass assembler for a self-designed 8-bit CPU based on [MIPS](https://en.wikipedia.org/wiki/MIPS_architecture).

### Prerequisites
- `python` is installed / accessible

### Installation
Get the code, e.g. by running
```sh
git clone https://github.com/julius-boettger/mips-like-assembler
```

### Usage
- Write assembly in a file, e.g. `input.txt` (see [considerations when writing assembly](#considerations-when-writing-assembly-for-this-assembler) below)
- Set `input_path` in `main.py` to the path to your file, e.g. `"/path/to/input.txt"`
- Optionally set `output_path` in `main.py` to something other than `output.txt`
- Run `python main.py`
- Optionally load the output file into your CPUs RAM in [Logisim-evolution](https://github.com/logisim-evolution/logisim-evolution)

### Considerations when writing assembly (for this assembler)
- Labels have to be followed by an instruction _on the same line_, e.g. `my_label: nop`
- All numbers are in hexadecimal notation, e.g. `db #0f`
- The entire code is case-insensitive (even the labels!)
- Use empty lines and extra spaces where you feel like it, they will be ignored
- Place comments anywhere (starting with `;`) like usual