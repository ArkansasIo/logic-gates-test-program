# 8-Bit Computer System

A complete 8-bit computer system emulator with Z80 CPU, GPU, BIOS, CMOS, operating system, and CP/M compatibility.

## Features

- **Z80 CPU Emulator**: Full 8-bit Z80 processor implementation with all instructions
- **Memory System**: 64KB RAM, 16KB ROM with bank switching support
- **GPU**: Simple 8-bit graphics processor with 320x240 resolution, 256 colors
- **BIOS**: Basic Input/Output System for hardware initialization
- **CMOS**: Battery-backed configuration storage
- **Operating System**: Simple multitasking OS with file system support
- **CP/M Compatibility**: Run CP/M programs and applications
- **Z80 Assembler**: Built-in assembler for Z80 assembly language
- **I/O System**: Keyboard, serial port, and parallel port emulation

## Architecture

```
┌─────────────────────────────────────────────┐
│             Z80 CPU (8-bit)                 │
│  - 8-bit data bus, 16-bit address bus       │
│  - 158 instructions, 4MHz clock             │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌─────────▼────────┐
│  RAM (56KB)    │    │  ROM (8KB)       │
│  Video (8KB)   │    │  BIOS            │
└────────────────┘    └──────────────────┘
        │                       │
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌─────────▼────────┐
│  GPU           │    │  I/O Devices     │
│  320x240x8bpp  │    │  Keyboard, etc.  │
└────────────────┘    └──────────────────┘
```

## Memory Map

```
0x0000 - 0x1FFF : ROM (BIOS) - 8KB
0x2000 - 0xDFFF : RAM (Main Memory) - 48KB
0xE000 - 0xFFFF : Video RAM - 8KB
```

## I/O Ports

```
0x00 - 0x0F : GPU Control
0x10 - 0x1F : Keyboard
0x20 - 0x2F : Serial Port
0x30 - 0x3F : Parallel Port
0x40 - 0x4F : CMOS/RTC
0x50 - 0x5F : Disk Controller
```

## Building

### Windows
```bash
cd 8bit-computer-system
gcc -o emulator src/*.c src/cpu/*.c src/memory/*.c src/gpu/*.c src/io/*.c src/cpm/*.c -Iinclude
```

### Linux/macOS
```bash
cd 8bit-computer-system
gcc -o emulator src/*.c src/cpu/*.c src/memory/*.c src/gpu/*.c src/io/*.c src/cpm/*.c -Iinclude -lm
```

## Running

```bash
# Run with BIOS
./emulator

# Load and run a program
./emulator program.bin

# Run CP/M mode
./emulator --cpm disk.img
```

## Assembly Programming

Example Z80 assembly program:

```asm
; Hello World in Z80 Assembly
    ORG 0x8000
    
start:
    LD HL, message
    CALL print_string
    HALT
    
print_string:
    LD A, (HL)
    OR A
    RET Z
    OUT (0x10), A
    INC HL
    JR print_string
    
message:
    DB "Hello, World!", 0
```

Assemble with:
```bash
./assembler hello.asm -o hello.bin
./emulator hello.bin
```

## Project Structure

```
8bit-computer-system/
├── src/
│   ├── main.c              # Main emulator entry point
│   ├── cpu/
│   │   ├── z80.c           # Z80 CPU implementation
│   │   └── instructions.c  # Instruction set
│   ├── memory/
│   │   ├── ram.c           # RAM implementation
│   │   └── rom.c           # ROM and BIOS loader
│   ├── gpu/
│   │   ├── gpu.c           # GPU implementation
│   │   └── video.c         # Video output
│   ├── io/
│   │   ├── keyboard.c      # Keyboard input
│   │   ├── serial.c        # Serial port
│   │   └── cmos.c          # CMOS/RTC
│   └── cpm/
│       └── cpm.c           # CP/M compatibility layer
├── include/
│   ├── z80.h               # CPU header
│   ├── memory.h            # Memory system header
│   ├── gpu.h               # GPU header
│   └── io.h                # I/O system header
├── bios/
│   ├── bios.asm            # BIOS source code
│   └── bios.bin            # Compiled BIOS
├── os/
│   ├── kernel.asm          # OS kernel
│   ├── loader.asm          # Bootloader
│   └── syscalls.asm        # System calls
├── asm/
│   ├── assembler.c         # Z80 assembler
│   └── lib/
│       └── stdlib.asm      # Standard library
└── examples/
    ├── hello/
    │   └── hello.asm       # Hello world example
    └── graphics/
        └── demo.asm        # Graphics demo
```

## Documentation

See the `docs/` directory for detailed documentation:
- CPU instruction set reference
- BIOS function reference
- OS system call reference
- Assembly language guide

## License

MIT License - See LICENSE file for details
