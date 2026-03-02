"""
QUICK START GUIDE
Run this to see all features in action!
"""

print("""
╔══════════════════════════════════════════════════════════════════╗
║      8-BIT COMPUTER SIMULATION - QUICK START GUIDE              ║
╚══════════════════════════════════════════════════════════════════╝

Welcome! This project contains a complete 8-bit computer simulation
built from logic gates up to a working CPU with assembly language.

═══════════════════════════════════════════════════════════════════
                        QUICK START
═══════════════════════════════════════════════════════════════════

1. RUN THE MAIN PROGRAM (Interactive Menu):
   
   python main.py
   
   This gives you an interactive menu to explore all features.

2. TEST INDIVIDUAL COMPONENTS:

   python logic_gates.py          # See all logic gates in action
   python computer_components.py  # Test CPU, RAM, ROM, etc.
   python assembly_language.py    # Try the assembler
   python database_manager.py     # Create SQL database

═══════════════════════════════════════════════════════════════════
                     WHAT'S INCLUDED
═══════════════════════════════════════════════════════════════════

✓ ALL LOGIC GATES (AND, OR, NOT, NAND, NOR, XOR, XNOR)
  - Pure functions working with 0 and 1
  - Object-oriented gate classes
  - Dataclass structures

✓ COMPOUND GATES
  - Half Adder & Full Adder
  - Multiplexer & Demultiplexer
  - Encoder & Decoder

✓ 8-BIT BINARY OPERATIONS
  - Addition with carry
  - Bitwise AND, OR, XOR, NOT
  - Shift left/right operations

✓ COMPUTER COMPONENTS
  - CPU (8-bit with 20+ instructions)
  - RAM (256 bytes, volatile)
  - ROM (256 bytes, permanent)
  - EEPROM (128 bytes)
  - Storage (64KB hard drive)
  - CMOS (Settings & RTC)
  - BIOS (Boot & POST)
  - GPU (40x25 text display)

✓ ASSEMBLY LANGUAGE
  - Full assembler (text → machine code)
  - Disassembler (machine code → text)
  - Sample programs included

✓ SQL DATABASE
  - Truth tables for all gates
  - CPU instruction set
  - Component specifications
  - Operation logging

═══════════════════════════════════════════════════════════════════
                      EXAMPLE USAGE
═══════════════════════════════════════════════════════════════════

>>> from logic_gates import AND, OR, XOR, NOT
>>> AND(1, 1)
1
>>> XOR(1, 0)
1
>>> NOT(1)
0

>>> from logic_gates import CompoundGates
>>> CompoundGates.HALF_ADDER(1, 1)
(0, 1)  # sum=0, carry=1

>>> from logic_gates import BinaryOperations
>>> a = BinaryOperations.int_to_8bit(25)
>>> b = BinaryOperations.int_to_8bit(17)
>>> result = BinaryOperations.add_8bit(a, b)
>>> BinaryOperations.bit_to_int(result)
42

>>> from computer_components import RAM, CPU
>>> ram = RAM(256)
>>> cpu = CPU(ram)
>>> # Load and run program...

>>> from assembly_language import Assembler
>>> asm = Assembler()
>>> code = asm.assemble("LDA 0x10\\nADD\\nHLT")

═══════════════════════════════════════════════════════════════════
                     FILE STRUCTURE
═══════════════════════════════════════════════════════════════════

logic_gates.py            - All logic gate implementations
computer_components.py    - CPU, RAM, ROM, BIOS, GPU, etc.
assembly_language.py      - Assembler and sample programs
database_manager.py       - SQL database interface
logic_gates_database.sql  - Database schema with truth tables
main.py                   - Interactive demonstration program
README.md                 - Complete documentation
requirements.txt          - Dependencies (none required!)

═══════════════════════════════════════════════════════════════════
                      LEARN MORE
═══════════════════════════════════════════════════════════════════

Read README.md for detailed documentation including:
  • Complete truth tables
  • CPU instruction set reference
  • Assembly language tutorial
  • Database schema documentation
  • Architecture diagrams
  • Sample programs explained

═══════════════════════════════════════════════════════════════════

                Ready to start? Run: python main.py

═══════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    import os
    import sys
    
    print("\n🚀 Would you like to run the main program now? (y/n): ", end="")
    choice = input().strip().lower()
    
    if choice == 'y':
        print("\nLaunching main program...\n")
        try:
            import main
            main.main()
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
        except Exception as e:
            print(f"\nError: {e}")
            print("\nPlease run: python main.py")
    else:
        print("\n📚 Check out README.md for more information!")
        print("💡 Run 'python main.py' when ready!")
