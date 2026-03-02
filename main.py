"""
MAIN PROGRAM - Complete 8-bit Computer Simulation
Demonstrates all logic gates, computer components, and assembly language
"""

import sys
from logic_gates import *
from computer_components import *
from assembly_language import *

def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def demo_logic_gates():
    """Demonstrate all logic gates"""
    print_header("LOGIC GATES DEMONSTRATION")
    
    # Test all basic gates
    gates = [
        ('AND', AND, [(0,0), (0,1), (1,0), (1,1)]),
        ('OR', OR, [(0,0), (0,1), (1,0), (1,1)]),
        ('NOT', NOT, [(0,), (1,)]),
        ('NAND', NAND, [(0,0), (0,1), (1,0), (1,1)]),
        ('NOR', NOR, [(0,0), (0,1), (1,0), (1,1)]),
        ('XOR', XOR, [(0,0), (0,1), (1,0), (1,1)]),
        ('XNOR', XNOR, [(0,0), (0,1), (1,0), (1,1)])
    ]
    
    for gate_name, gate_func, test_cases in gates:
        print(f"{gate_name} Gate:")
        if len(test_cases[0]) == 1:
            print("  Input | Output")
            print("  ------|-------")
            for inputs in test_cases:
                result = gate_func(*inputs)
                print(f"    {inputs[0]}   |   {result}")
        else:
            print("  A | B | Output")
            print("  --|---|-------")
            for inputs in test_cases:
                result = gate_func(*inputs)
                print(f"  {inputs[0]} | {inputs[1]} |   {result}")
        print()

def demo_compound_gates():
    """Demonstrate compound gates"""
    print_header("COMPOUND GATES DEMONSTRATION")
    
    # Half Adder
    print("HALF ADDER")
    print("Adds two 1-bit numbers\n")
    print("A | B | Sum | Carry")
    print("--|---|-----|------")
    for a in [0, 1]:
        for b in [0, 1]:
            sum_bit, carry = CompoundGates.HALF_ADDER(a, b)
            print(f"{a} | {b} |  {sum_bit}  |   {carry}")
    
    # Full Adder
    print("\n\nFULL ADDER")
    print("Adds two 1-bit numbers plus carry-in\n")
    print("A | B | Cin | Sum | Cout")
    print("--|---|-----|-----|-----")
    for a in [0, 1]:
        for b in [0, 1]:
            for cin in [0, 1]:
                sum_bit, cout = CompoundGates.FULL_ADDER(a, b, cin)
                print(f"{a} | {b} |  {cin}  |  {sum_bit}  |  {cout}")
    
    # Multiplexer
    print("\n\n2-TO-1 MULTIPLEXER")
    print("Selects between two inputs\n")
    print("A | B | Sel | Out")
    print("--|---|-----|----")
    for a in [0, 1]:
        for b in [0, 1]:
            for sel in [0, 1]:
                out = CompoundGates.MULTIPLEXER_2to1(a, b, sel)
                print(f"{a} | {b} |  {sel}  |  {out}")

def demo_binary_operations():
    """Demonstrate 8-bit binary operations"""
    print_header("8-BIT BINARY OPERATIONS")
    
    # Addition
    a = BinaryOperations.int_to_8bit(25)
    b = BinaryOperations.int_to_8bit(17)
    result = BinaryOperations.add_8bit(a, b)
    
    print("8-BIT ADDITION")
    print(f"  25 = {''.join(map(str, a))}")
    print(f"+ 17 = {''.join(map(str, b))}")
    print("  " + "-" * 34)
    print(f"  42 = {''.join(map(str, result))}")
    print(f"\nDecimal result: {BinaryOperations.bit_to_int(result)}")
    
    # Bitwise operations
    a = BinaryOperations.int_to_8bit(0b11110000)
    b = BinaryOperations.int_to_8bit(0b10101010)
    
    print("\n\nBITWISE OPERATIONS")
    print(f"A = {''.join(map(str, a))} (0x{BinaryOperations.bit_to_int(a):02X})")
    print(f"B = {''.join(map(str, b))} (0x{BinaryOperations.bit_to_int(b):02X})")
    
    and_result = BinaryOperations.bitwise_and_8bit(a, b)
    or_result = BinaryOperations.bitwise_or_8bit(a, b)
    xor_result = BinaryOperations.bitwise_xor_8bit(a, b)
    not_result = BinaryOperations.bitwise_not_8bit(a)
    
    print(f"\nA AND B = {''.join(map(str, and_result))} (0x{BinaryOperations.bit_to_int(and_result):02X})")
    print(f"A OR  B = {''.join(map(str, or_result))} (0x{BinaryOperations.bit_to_int(or_result):02X})")
    print(f"A XOR B = {''.join(map(str, xor_result))} (0x{BinaryOperations.bit_to_int(xor_result):02X})")
    print(f"NOT A   = {''.join(map(str, not_result))} (0x{BinaryOperations.bit_to_int(not_result):02X})")
    
    # Shifts
    print("\n\nSHIFT OPERATIONS")
    value = BinaryOperations.int_to_8bit(0b00001100)  # 12
    print(f"Original:    {''.join(map(str, value))} = {BinaryOperations.bit_to_int(value)}")
    
    left = BinaryOperations.shift_left(value, 1)
    print(f"Shift Left:  {''.join(map(str, left))} = {BinaryOperations.bit_to_int(left)} (x2)")
    
    right = BinaryOperations.shift_right(value, 1)
    print(f"Shift Right: {''.join(map(str, right))} = {BinaryOperations.bit_to_int(right)} (÷2)")

def demo_computer_components():
    """Demonstrate computer components"""
    print_header("COMPUTER COMPONENTS DEMONSTRATION")
    
    # Initialize components
    print("Initializing computer components...\n")
    ram = RAM(256)
    rom = ROM(256)
    eeprom = EEPROM(128)
    storage = Storage(65536)
    cmos = CMOS()
    cpu = CPU(ram)
    gpu = GPU(40, 25)
    
    # RAM test
    print("RAM TEST")
    print("-" * 40)
    ram.write(0x00, 0xAA)
    ram.write(0x01, 0x55)
    ram.write(0x02, 0xFF)
    print(f"Write to RAM[0x00] = 0xAA")
    print(f"Write to RAM[0x01] = 0x55")
    print(f"Write to RAM[0x02] = 0xFF")
    print(f"\nRead from RAM[0x00] = 0x{ram.read(0x00):02X}")
    print(f"Read from RAM[0x01] = 0x{ram.read(0x01):02X}")
    print(f"Read from RAM[0x02] = 0x{ram.read(0x02):02X}")
    print(f"\nTotal RAM accesses: {ram.access_count}")
    
    # ROM test
    print("\n\nROM TEST")
    print("-" * 40)
    rom.unlock()
    rom.program(0x00, 0xDE)
    rom.program(0x01, 0xAD)
    rom.program(0x02, 0xBE)
    rom.program(0x03, 0xEF)
    rom.lock()
    print("Programmed ROM with magic values")
    print(f"ROM[0x00-0x03] = {rom.read(0x00):02X} {rom.read(0x01):02X} {rom.read(0x02):02X} {rom.read(0x03):02X}")
    print("ROM is now locked (read-only)")
    
    # CMOS test
    print("\n\nCMOS / BIOS SETTINGS")
    print("-" * 40)
    time_info = cmos.get_time()
    print(f"RTC Date: {time_info['year']}-{time_info['month']:02d}-{time_info['day']:02d}")
    print(f"RTC Time: {time_info['hour']:02d}:{time_info['minute']:02d}:{time_info['second']:02d}")
    print(f"CPU Speed: {cmos.get_setting('cpu_speed')} MHz")
    print(f"RAM Size: {cmos.get_setting('ram_size')} bytes")
    print(f"Boot Order: {', '.join(cmos.get_setting('boot_order'))}")
    
    # GPU test
    print("\n\nGPU / DISPLAY TEST")
    print("-" * 40)
    gpu.clear_screen()
    gpu.print_text("Hello, Computer!")
    gpu.print_text("\nLogic Gate System Ready")
    gpu.print_text("\n\n8-bit CPU Online")
    print(gpu.render())

def demo_bios_boot():
    """Demonstrate BIOS and boot process"""
    print_header("BIOS AND BOOT SEQUENCE")
    
    # Initialize hardware
    ram = RAM(256)
    rom = ROM(256)
    cmos = CMOS()
    storage = Storage(65536)
    cpu = CPU(ram)
    gpu = GPU(40, 25)
    
    # Create BIOS
    bios = BIOS(rom, cmos)
    
    # Run POST
    success = bios.power_on_self_test(ram, cpu)
    
    if success:
        # Create bootloader signature
        bootloader = [0] * 512
        bootloader[510] = 0x55
        bootloader[511] = 0xAA
        storage.write_sector(0, bootloader)
        
        # Attempt boot
        bios.boot(storage)
        
        # Create OS
        os = SimpleOS(cpu, ram, storage, gpu)
        print("\n" + os.boot())

def demo_cpu_execution():
    """Demonstrate CPU program execution"""
    print_header("CPU PROGRAM EXECUTION")
    
    # Initialize system
    ram = RAM(256)
    cpu = CPU(ram)
    
    # Simple program: Add two numbers
    print("Program: Add two numbers (5 + 3)")
    print("-" * 40)
    print("Assembly Code:")
    print("  LDA [0x10]  ; Load 5 into A")
    print("  LDB [0x11]  ; Load 3 into B")
    print("  ADD         ; A = A + B")
    print("  STA [0x12]  ; Store result")
    print("  HLT         ; Halt")
    
    # Machine code
    program = [
        0x01, 0x10,  # LDA [0x10]
        0x02, 0x11,  # LDB [0x11]
        0x10,        # ADD
        0x03, 0x12,  # STA [0x12]
        0xFF         # HLT
    ]
    
    # Load data
    ram.write(0x10, 5)
    ram.write(0x11, 3)
    
    # Load program
    for i, byte in enumerate(program):
        ram.write(i, byte)
    
    print("\n\nInitial State:")
    print(f"  RAM[0x10] = {ram.read(0x10)}")
    print(f"  RAM[0x11] = {ram.read(0x11)}")
    print(f"  Register A = {cpu.registers.A}")
    print(f"  Register B = {cpu.registers.B}")
    
    # Execute
    print("\nExecuting program...")
    cpu.run()
    
    print("\n\nFinal State:")
    print(f"  RAM[0x12] = {ram.read(0x12)} (result)")
    print(f"  Register A = {cpu.registers.A}")
    print(f"  Register B = {cpu.registers.B}")
    print(f"  CPU Cycles = {cpu.cycles}")
    print(f"  Zero Flag = {cpu.registers.get_flag('Z')}")
    print(f"  Carry Flag = {cpu.registers.get_flag('C')}")

def demo_assembler():
    """Demonstrate assembly language"""
    print_header("ASSEMBLY LANGUAGE DEMONSTRATION")
    
    assembler = Assembler()
    
    print("Assembly Code:")
    print("-" * 40)
    print(PROGRAM_ADD)
    
    print("\nAssembling...")
    machine_code = assembler.assemble(PROGRAM_ADD)
    
    print("\nMachine Code (Hexadecimal):")
    print("-" * 40)
    for i in range(0, len(machine_code), 8):
        addr = f"0x{i:04X}:"
        hex_bytes = " ".join(f"{b:02X}" for b in machine_code[i:i+8])
        print(f"{addr}  {hex_bytes}")
    
    print("\n\nDisassembly:")
    print("-" * 40)
    print(assembler.disassemble(machine_code))

def demo_logic_operations_cpu():
    """Demonstrate logic operations using CPU"""
    print_header("LOGIC OPERATIONS ON CPU")
    
    ram = RAM(256)
    cpu = CPU(ram)
    
    # Test values
    a_val = 0b11110000
    b_val = 0b10101010
    
    print(f"Input A = 0b{a_val:08b} (0x{a_val:02X})")
    print(f"Input B = 0b{b_val:08b} (0x{b_val:02X})")
    print("\n" + "-" * 50)
    
    # Store test values
    ram.write(0x30, a_val)
    ram.write(0x31, b_val)
    
    # Assemble logic operations program
    assembler = Assembler()
    machine_code = assembler.assemble(PROGRAM_BITWISE)
    
    # Load program
    for i, byte in enumerate(machine_code):
        ram.write(i, byte)
    
    # Execute
    cpu.run()
    
    # Display results
    and_result = ram.read(0x90)
    or_result = ram.read(0x91)
    xor_result = ram.read(0x92)
    not_result = ram.read(0x93)
    
    print("\nResults:")
    print(f"A AND B = 0b{and_result:08b} (0x{and_result:02X})")
    print(f"A OR  B = 0b{or_result:08b} (0x{or_result:02X})")
    print(f"A XOR B = 0b{xor_result:08b} (0x{xor_result:02X})")
    print(f"NOT A   = 0b{not_result:08b} (0x{not_result:02X})")
    print(f"\nTotal CPU cycles: {cpu.cycles}")

def show_menu():
    """Main menu"""
    print("\n" + "=" * 70)
    print("  8-BIT COMPUTER SIMULATION - MAIN MENU")
    print("=" * 70)
    print("\n1.  Logic Gates Demonstration")
    print("2.  Compound Gates (Half Adder, Full Adder, Multiplexer)")
    print("3.  8-bit Binary Operations")
    print("4.  Computer Components (RAM, ROM, CMOS, etc.)")
    print("5.  BIOS and Boot Sequence")
    print("6.  CPU Program Execution")
    print("7.  Assembly Language")
    print("8.  Logic Operations on CPU")
    print("9.  Run ALL Demonstrations")
    print("0.  Exit")
    print("\nEnter choice: ", end='')

def main():
    """Main program"""
    print("=" * 70)
    print(" " * 15 + "8-BIT COMPUTER SIMULATION")
    print(" " * 10 + "Complete Logic Gate & Computer System")
    print("=" * 70)
    print("\nFeatures:")
    print("  • All basic logic gates (AND, OR, NOT, NAND, NOR, XOR, XNOR)")
    print("  • Compound gates (Adders, Multiplexers, Encoders)")
    print("  • 8-bit CPU with instruction set")
    print("  • RAM, ROM, EEPROM, Storage")
    print("  • BIOS, CMOS, GPU")
    print("  • Assembly language and assembler")
    print("  • Binary operations and arithmetic")
    
    while True:
        show_menu()
        choice = input().strip()
        
        if choice == '1':
            demo_logic_gates()
        elif choice == '2':
            demo_compound_gates()
        elif choice == '3':
            demo_binary_operations()
        elif choice == '4':
            demo_computer_components()
        elif choice == '5':
            demo_bios_boot()
        elif choice == '6':
            demo_cpu_execution()
        elif choice == '7':
            demo_assembler()
        elif choice == '8':
            demo_logic_operations_cpu()
        elif choice == '9':
            # Run all demos
            demo_logic_gates()
            demo_compound_gates()
            demo_binary_operations()
            demo_computer_components()
            demo_bios_boot()
            demo_cpu_execution()
            demo_assembler()
            demo_logic_operations_cpu()
        elif choice == '0':
            print("\nShutting down system... Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
