# Getting Started

## Quick Start

### 1. Building the Project

**On Windows (with GCC/MinGW installed):**
```powershell
.\build.ps1
```

**Or manually:**
```bash
# Create directories
mkdir build bin

# Build emulator
gcc -Wall -O2 -Iinclude -o bin/emulator.exe src/main.c src/cpu/z80.c src/memory/ram.c src/gpu/gpu.c src/io/*.c src/cpm/cpm.c -lm

# Build assembler
gcc -Wall -O2 -o bin/assembler.exe asm/assembler.c
```

**On Linux/macOS:**
```bash
make
```

### 2. Running the Emulator

**Run with default settings:**
```bash
./bin/emulator
```

**Load and run a program:**
```bash
./bin/emulator examples/hello/hello.bin
```

**Debug mode:**
```bash
./bin/emulator --debug examples/hello/hello.bin
```

## Writing Assembly Programs

### Hello World Example

Create a file `hello.asm`:
```asm
    ORG 0x8000

START:
    LD HL, MESSAGE
    CALL PRINT

PRINT:
    LD A, (HL)
    OR A
    RET Z
    OUT (0x09), A    ; Output to GPU
    INC HL
    JR PRINT

MESSAGE:
    DB "Hello, World!", 0
```

### Assembling

```bash
./bin/assembler hello.asm -o hello.bin
```

### Running

```bash
./bin/emulator hello.bin
```

## Hardware Reference

### Memory Map
- `0x0000-0x1FFF`: ROM (BIOS) - 8KB
- `0x2000-0xDFFF`: RAM - 48KB
- `0xE000-0xFFFF`: Video RAM - 8KB

### I/O Ports

**GPU (0x00-0x0F)**
- `0x00`: Control register
- `0x01`: Status register
- `0x02`: Cursor X position
- `0x03`: Cursor Y position
- `0x04`: Current color
- `0x09`: Character output

**Keyboard (0x10-0x1F)**
- `0x10`: Data port
- `0x11`: Status port

**Serial Port (0x20-0x2F)**
- `0x20`: Data port
- `0x21`: Status port

**CMOS/RTC (0x40-0x4F)**
- `0x40`: Address register
- `0x41`: Data register

## Debug Commands

In debug mode, you can use:
- `s` or `n` - Step one instruction
- `c` - Continue execution
- `r` - Reset system
- `m <addr>` - Dump memory (hex address)
- `g <addr>` - Set PC to address
- `q` - Quit
- `h` or `?` - Show help

## Examples

### 1. Simple Output
```asm
    ORG 0x8000
    LD A, 'A'
    OUT (0x09), A
    HALT
```

### 2. Loop
```asm
    ORG 0x8000
    LD B, 10
LOOP:
    LD A, 'X'
    OUT (0x09), A
    DEC B
    JR NZ, LOOP
    HALT
```

### 3. Using Stack
```asm
    ORG 0x8000
    LD HL, 0x1234
    PUSH HL
    CALL SUBROUTINE
    POP HL
    HALT

SUBROUTINE:
    ; Do something
    RET
```

## Troubleshooting

### Emulator won't start
- Check that all source files compiled without errors
- Ensure GCC is installed and in PATH
- On Windows, make sure you have MinGW-w64 or similar

### Assembly errors
- Check syntax - instructions must be uppercase
- Verify addresses are in hex format (0x prefix)
- Ensure labels end with colon (:)

### Program doesn't run
- Verify ORG directive sets correct start address
- Default entry point is PC=0x0000, so set ORG 0x8000 for user programs
- Use `--debug` mode to step through execution

## Next Steps

1. Read the [CPU Reference](docs/CPU_REFERENCE.md) for instruction details
2. Review [BIOS Reference](docs/BIOS_REFERENCE.md) for system calls
3. Study the example programs in `examples/`
4. Experiment with writing your own programs!

## Resources

- Z80 instruction set: http://www.z80.info/
- Assembly language tutorials
- CP/M documentation for CP/M mode features
