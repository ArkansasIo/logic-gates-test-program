# 8-BIT COMPUTER SIMULATION WITH LOGIC GATES
## Complete Implementation of Logic Gates, Computer Components, and Assembly Language

---

## 📋 PROJECT OVERVIEW

This project is a comprehensive simulation of an 8-bit computer system built from the ground up using logic gates. It includes:

- **All basic logic gates** (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUFFER)
- **Compound gates** (Half Adder, Full Adder, Multiplexer, Demultiplexer, Encoder, Decoder)
- **8-bit CPU** with complete instruction set
- **Computer components**: RAM, ROM, EEPROM, Storage, CMOS, BIOS, GPU
- **Assembly language** with assembler/disassembler
- **SQL database** with truth tables and component data
- **Binary operations** for 8-bit arithmetic and logic

---

## 📁 PROJECT FILES

### Core Modules

1. **`logic_gates.py`** - Logic gate implementations
   - All basic logic gates working with 0 and 1
   - Logic gate classes and structures
   - Compound gates (adders, multiplexers, etc.)
   - Binary operations (8-bit arithmetic)

2. **`computer_components.py`** - Computer architecture
   - RAM (Random Access Memory, 256 bytes)
   - ROM (Read-Only Memory, 256 bytes)
   - EEPROM (Electrically Erasable Programmable ROM, 128 bytes)
   - Storage (Hard Drive simulation, 65536 bytes)
   - CMOS (Settings and Real-Time Clock)
   - BIOS (Boot sequence and POST)
   - CPU (8-bit processor with registers)
   - GPU (Simple graphics/text display)
   - Simple Operating System

3. **`assembly_language.py`** - Assembly programming
   - 8-bit assembler
   - Disassembler
   - Sample programs demonstrating CPU features
   - Machine code generation

4. **`database_manager.py`** - SQL database interface
   - Creates and manages SQLite database
   - Logs gate operations
   - Truth table queries
   - Memory operation tracking

5. **`logic_gates_database.sql`** - Database schema
   - Truth tables for all logic gates
   - Computer components catalog
   - CPU instruction set
   - Memory operations log
   - Useful views and queries

6. **`main.py`** - Main demonstration program
   - Interactive menu system
   - All demonstrations in one place
   - Easy-to-use interface

---

## 🚀 GETTING STARTED

### Prerequisites

- Python 3.7 or higher
- SQLite3 (included with Python)

### Running the Program

1. **Run the main demonstration**:
   ```bash
   python main.py
   ```
   This provides an interactive menu with all demonstrations.

2. **Test individual components**:
   ```bash
   python logic_gates.py          # Logic gates demo
   python computer_components.py  # Computer components demo
   python assembly_language.py    # Assembly language demo
   python database_manager.py     # Create and test database
   ```

3. **Create the SQL database**:
   ```bash
   python database_manager.py
   ```
   This creates `logic_gates.db` with all truth tables and component data.

---

## 🔧 FEATURES IN DETAIL

### 1. Logic Gates

All logic gates operate on binary values (0 and 1):

**Basic Gates:**
- `AND(a, b)` - Returns 1 only if both inputs are 1
- `OR(a, b)` - Returns 1 if at least one input is 1
- `NOT(a)` - Inverts the input
- `NAND(a, b)` - NOT-AND, returns 0 only if both are 1
- `NOR(a, b)` - NOT-OR, returns 1 only if both are 0
- `XOR(a, b)` - Returns 1 if inputs are different
- `XNOR(a, b)` - Returns 1 if inputs are the same

**Example Usage:**
```python
from logic_gates import AND, OR, NOT, XOR

result1 = AND(1, 1)      # Returns 1
result2 = OR(0, 1)       # Returns 1
result3 = XOR(1, 0)      # Returns 1
result4 = NOT(1)         # Returns 0
```

### 2. Compound Gates

Built from basic logic gates:

- **Half Adder**: Adds two 1-bit numbers
- **Full Adder**: Adds two 1-bit numbers plus carry
- **Multiplexer**: Selects between inputs
- **Demultiplexer**: Routes input to outputs
- **Encoder/Decoder**: Binary encoding/decoding

**Example:**
```python
from logic_gates import CompoundGates

# Add two bits
sum_bit, carry = CompoundGates.HALF_ADDER(1, 1)
# sum_bit = 0, carry = 1 (binary: 10)

# Full adder with carry-in
sum_bit, carry_out = CompoundGates.FULL_ADDER(1, 1, 1)
# sum_bit = 1, carry_out = 1 (binary: 11)
```

### 3. 8-bit Binary Operations

```python
from logic_gates import BinaryOperations

# Convert integer to 8-bit binary
a = BinaryOperations.int_to_8bit(25)  # [0,0,0,1,1,0,0,1]
b = BinaryOperations.int_to_8bit(17)  # [0,0,0,1,0,0,0,1]

# 8-bit addition
result = BinaryOperations.add_8bit(a, b)  # [0,0,1,0,1,0,1,0] = 42

# Bitwise operations
and_result = BinaryOperations.bitwise_and_8bit(a, b)
or_result = BinaryOperations.bitwise_or_8bit(a, b)
xor_result = BinaryOperations.bitwise_xor_8bit(a, b)

# Shift operations
left = BinaryOperations.shift_left(a, 1)   # Multiply by 2
right = BinaryOperations.shift_right(a, 1)  # Divide by 2
```

### 4. Computer Components

#### RAM (Random Access Memory)
- 256 bytes of volatile memory
- Read/write operations
- Access counter

```python
from computer_components import RAM

ram = RAM(256)
ram.write(0x00, 0xAA)
value = ram.read(0x00)  # Returns 0xAA
```

#### ROM (Read-Only Memory)
- 256 bytes of permanent storage
- Lock/unlock mechanism
- Ideal for BIOS/firmware

```python
from computer_components import ROM

rom = ROM(256)
rom.unlock()
rom.program(0x00, 0xFF)
rom.lock()  # Now read-only
```

#### CPU (Central Processing Unit)
- 8-bit architecture
- Registers: A, B, C, D, PC, SP, FLAGS
- 20+ instructions

```python
from computer_components import CPU, RAM

ram = RAM(256)
cpu = CPU(ram)

# Load program into RAM
program = [0x01, 0x10, 0x02, 0x11, 0x10, 0xFF]  # LDA, LDB, ADD, HLT
for i, byte in enumerate(program):
    ram.write(i, byte)

# Execute
cpu.run()
```

### 5. CPU Instruction Set

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x00 | NOP | No operation |
| 0x01 | LDA | Load A from memory |
| 0x02 | LDB | Load B from memory |
| 0x03 | STA | Store A to memory |
| 0x04 | STB | Store B to memory |
| 0x10 | ADD | A = A + B |
| 0x11 | SUB | A = A - B |
| 0x12 | AND | A = A AND B |
| 0x13 | OR | A = A OR B |
| 0x14 | XOR | A = A XOR B |
| 0x15 | NOT | A = NOT A |
| 0x16 | SHL | Shift left |
| 0x17 | SHR | Shift right |
| 0x20 | JMP | Jump to address |
| 0x21 | JZ | Jump if zero |
| 0x22 | JNZ | Jump if not zero |
| 0x30 | CALL | Call subroutine |
| 0x31 | RET | Return from subroutine |
| 0x40 | PUSH | Push to stack |
| 0x41 | POP | Pop from stack |
| 0xFF | HLT | Halt execution |

### 6. Assembly Language

Write programs in assembly and convert to machine code:

```assembly
; Add two numbers
    LDA 0x10    ; Load value from address 0x10
    LDB 0x11    ; Load value from address 0x11
    ADD         ; A = A + B
    STA 0x12    ; Store result
    HLT         ; Halt
```

**Assembler Usage:**
```python
from assembly_language import Assembler

assembler = Assembler()
program = """
    LDA 0x10
    LDB 0x11
    ADD
    STA 0x12
    HLT
"""

machine_code = assembler.assemble(program)
# Returns: [0x01, 0x10, 0x02, 0x11, 0x10, 0x03, 0x12, 0xFF]
```

### 7. SQL Database

The database contains:

**Tables:**
- `gate_types` - All logic gate definitions
- `truth_table` - Complete truth tables for all gates
- `computer_components` - Hardware component specifications
- `cpu_instructions` - Full instruction set
- `gate_operations` - Log of gate operations
- `memory_operations` - Log of memory accesses

**Sample Queries:**
```sql
-- Get truth table for AND gate
SELECT * FROM v_truth_tables WHERE gate_name = 'AND';

-- Get all arithmetic instructions
SELECT * FROM cpu_instructions WHERE opcode BETWEEN 0x10 AND 0x1F;

-- Memory operation statistics
SELECT component_name, COUNT(*) as operations
FROM memory_operations mo
JOIN computer_components cc ON mo.component_id = cc.component_id
GROUP BY component_name;
```

---

## 📊 TRUTH TABLES

### AND Gate
| A | B | Output |
|---|---|--------|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

### OR Gate
| A | B | Output |
|---|---|--------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

### XOR Gate
| A | B | Output |
|---|---|--------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### NOT Gate
| A | Output |
|---|--------|
| 0 | 1 |
| 1 | 0 |

---

## 💡 EXAMPLE PROGRAMS

### 1. Simple Addition
```assembly
LDA 0x10    ; Load first number
LDB 0x11    ; Load second number
ADD         ; Add them
STA 0x12    ; Store result
HLT         ; Stop
```

### 2. Counter Loop
```assembly
start:
    LDA 0x20    ; Load counter
    LDB 0x21    ; Load increment (1)
    ADD         ; Increment
    STA 0x20    ; Save counter
    LDB 0x22    ; Load limit
    SUB         ; Check if done
    JZ end      ; If zero, exit
    JMP start   ; Otherwise, loop
end:
    HLT         ; Stop
```

### 3. Logic Operations
```assembly
    LDA 0x30    ; Load value 1
    LDB 0x31    ; Load value 2
    AND         ; Perform AND
    STA 0x40    ; Store result
    
    LDA 0x30    ; Reload value 1
    LDB 0x31    ; Reload value 2
    OR          ; Perform OR
    STA 0x41    ; Store result
    
    HLT         ; Stop
```

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────┐
│                   8-BIT COMPUTER                    │
├─────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │   CPU    │  │   GPU    │  │   BIOS   │         │
│  │  8-bit   │  │  40x25   │  │  v1.0    │         │
│  └────┬─────┘  └──────────┘  └──────────┘         │
│       │                                             │
│  ┌────┴──────────────────────────────────┐         │
│  │           MEMORY BUS                  │         │
│  └────┬──────┬──────┬──────┬─────┬───────┘         │
│       │      │      │      │     │                 │
│  ┌────┴───┐ ┌┴────┐ ┌┴────┐ ┌───┴──┐ ┌─────────┐  │
│  │  RAM   │ │ ROM │ │EEPROM│ │CMOS │ │ Storage │  │
│  │ 256B   │ │256B │ │128B  │ │128B │ │  64KB   │  │
│  └────────┘ └─────┘ └──────┘ └─────┘ └─────────┘  │
└─────────────────────────────────────────────────────┘

│
├─ LOGIC LAYER (Uses actual logic gates)
│  └─ AND, OR, NOT, NAND, NOR, XOR, XNOR
│     └─ Adders, Multiplexers, Encoders
│        └─ ALU, Memory Controllers
│           └─ Complete CPU
```

---

## 🎮 INTERACTIVE MENU

When you run `main.py`, you get an interactive menu:

```
8-BIT COMPUTER SIMULATION - MAIN MENU

1.  Logic Gates Demonstration
2.  Compound Gates (Half Adder, Full Adder, Multiplexer)
3.  8-bit Binary Operations
4.  Computer Components (RAM, ROM, CMOS, etc.)
5.  BIOS and Boot Sequence
6.  CPU Program Execution
7.  Assembly Language
8.  Logic Operations on CPU
9.  Run ALL Demonstrations
0.  Exit
```

---

## 🧪 TESTING

Run the test suite:
```bash
python -m pytest
```

Or run component tests individually:
```bash
python logic_gates.py
python computer_components.py
python assembly_language.py
```

---

## 📚 EDUCATIONAL VALUE

This project demonstrates:

1. **Digital Logic**: How computers work at the gate level
2. **Computer Architecture**: CPU, memory hierarchy, bus systems
3. **Assembly Programming**: Low-level programming concepts
4. **Operating Systems**: Boot process, BIOS, memory management
5. **Binary Arithmetic**: How numbers are represented and manipulated
6. **Database Design**: Storing and querying structured data

---

## 🔍 CODE STRUCTURE

```
logic_gates.py
├─ Basic Gates (AND, OR, NOT, etc.)
├─ Gate Classes (OOP implementations)
├─ Compound Gates (Adders, Multiplexers)
└─ Binary Operations (8-bit arithmetic)

computer_components.py
├─ Memory Components (RAM, ROM, EEPROM, Storage)
├─ CMOS and RTC
├─ BIOS (POST and boot)
├─ CPU (Registers, instruction execution)
├─ GPU (Text/graphics buffer)
└─ Simple OS

assembly_language.py
├─ Assembler (Assembly to machine code)
├─ Disassembler (Machine code to assembly)
└─ Sample Programs

database_manager.py
├─ Database creation
├─ Truth table queries
├─ Operation logging
└─ Statistics

main.py
└─ Interactive demonstrations
```

---

## 🎯 FUTURE ENHANCEMENTS

Possible additions:
- [ ] More CPU instructions (multiplication, division)
- [ ] Interrupts and I/O
- [ ] Virtual memory
- [ ] Multi-core simulation
- [ ] Network interface
- [ ] More complex graphics
- [ ] Assembler macro support
- [ ] Debugger with breakpoints

---

## 📝 LICENSE

This project is provided as educational material. Feel free to use, modify, and distribute.

---

## 👨‍💻 AUTHOR

Created as a comprehensive demonstration of digital logic, computer architecture, and low-level programming.

---

## 🙏 ACKNOWLEDGMENTS

This project demonstrates fundamental computer science concepts:
- Boolean algebra and logic gates
- Von Neumann architecture
- Assembly language programming
- Operating system basics
- Database systems

---

## 📞 SUPPORT

For questions or issues:
1. Check the demonstration programs in `main.py`
2. Review the SQL database schema
3. Read through the code comments
4. Experiment with the interactive menu

---

## 🎓 LEARNING PATH

1. Start with **logic gates** (`python logic_gates.py`)
2. Understand **binary operations**
3. Explore **computer components**
4. Learn **assembly language**
5. Study **CPU execution**
6. Query the **SQL database**
7. Experiment with **custom programs**

Enjoy exploring the fundamentals of computing! 🚀
