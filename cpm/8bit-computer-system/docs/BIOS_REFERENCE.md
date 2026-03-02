# BIOS Function Reference

## Overview
The BIOS (Basic Input/Output System) provides low-level hardware access functions.

## Entry Points

All BIOS functions are called through jump vectors starting at address 0x0000:

| Address | Function | Description |
|---------|----------|-------------|
| 0x0000 | BOOT | Cold boot system |
| 0x0003 | WBOOT | Warm boot system |
| 0x0006 | CONST | Console status |
| 0x0009 | CONIN | Console input |
| 0x000C | CONOUT | Console output |
| 0x000F | LIST | List output |
| 0x0012 | PUNCH | Punch output |
| 0x0015 | READER | Reader input |

## Function Details

### BOOT (0x0000)
Cold boot - initializes system
- **Input**: None
- **Output**: None
- **Destroys**: All registers

### WBOOT (0x0003)
Warm boot - restart system
- **Input**: None
- **Output**: None
- **Destroys**: All registers

### CONST (0x0006)
Console status - check if character available
- **Input**: None
- **Output**: A = 0xFF if char ready, 0x00 otherwise
- **Destroys**: A

### CONIN (0x0009)
Console input - read character
- **Input**: None
- **Output**: A = character
- **Destroys**: A
- **Note**: Blocks until character available

### CONOUT (0x000C)
Console output - write character
- **Input**: C = character to output
- **Output**: None
- **Destroys**: None

### Example Usage

```asm
; Print a character
LD C, 'A'
CALL 0x000C         ; CONOUT

; Check if key available
CALL 0x0006         ; CONST
OR A
JR Z, no_key
; Key is available

; Read a character
CALL 0x0009         ; CONIN
; Character now in A
```

## Print String Helper
Many programs need a print string function:

```asm
print_string:
    LD A, (HL)
    OR A
    RET Z
    LD C, A
    CALL 0x000C
    INC HL
    JR print_string
```

## Hardware I/O Ports
The BIOS abstracts these, but direct access is possible:

### GPU (0x00-0x0F)
- 0x00: Control register
- 0x09: Character output

### Keyboard (0x10-0x1F)
- 0x10: Data
- 0x11: Status

### Serial (0x20-0x2F)
- 0x20: Data
- 0x21: Status

### CMOS (0x40-0x4F)
- 0x40: Address
- 0x41: Data
