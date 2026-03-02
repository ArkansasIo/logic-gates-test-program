"""
8-bit Computer Architecture Components
Implements: CPU, RAM, ROM, Storage, CMOS, BIOS, EEPROM, and basic OS
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import time
from logic_gates import BinaryOperations, AND, OR, XOR, NOT

# ============================================================================
# MEMORY COMPONENTS
# ============================================================================

class RAM:
    """Random Access Memory - 8-bit addressable, volatile storage"""
    
    def __init__(self, size: int = 256):
        """Initialize RAM with specified size (default 256 bytes)"""
        self.size = size
        self.memory = [0] * size
        self.access_count = 0
    
    def read(self, address: int) -> int:
        """Read 8-bit value from memory address"""
        if 0 <= address < self.size:
            self.access_count += 1
            return self.memory[address]
        raise MemoryError(f"RAM read address out of bounds: {address}")
    
    def write(self, address: int, value: int):
        """Write 8-bit value to memory address"""
        if 0 <= address < self.size:
            self.access_count += 1
            self.memory[address] = value & 0xFF  # Ensure 8-bit
        else:
            raise MemoryError(f"RAM write address out of bounds: {address}")
    
    def clear(self):
        """Clear all RAM (set to 0)"""
        self.memory = [0] * self.size
    
    def dump(self, start: int = 0, end: int = 16) -> str:
        """Dump memory contents in hex format"""
        output = f"RAM Dump (0x{start:02X} to 0x{end:02X}):\n"
        for i in range(start, min(end, self.size), 16):
            output += f"0x{i:04X}: "
            for j in range(16):
                if i + j < self.size:
                    output += f"{self.memory[i+j]:02X} "
            output += "\n"
        return output


class ROM:
    """Read-Only Memory - Permanent storage for BIOS and firmware"""
    
    def __init__(self, size: int = 256):
        """Initialize ROM with specified size"""
        self.size = size
        self.memory = [0] * size
        self.locked = False
    
    def read(self, address: int) -> int:
        """Read 8-bit value from ROM address"""
        if 0 <= address < self.size:
            return self.memory[address]
        raise MemoryError(f"ROM read address out of bounds: {address}")
    
    def program(self, address: int, value: int):
        """Program ROM (only when unlocked)"""
        if self.locked:
            raise MemoryError("ROM is locked - cannot write")
        if 0 <= address < self.size:
            self.memory[address] = value & 0xFF
        else:
            raise MemoryError(f"ROM address out of bounds: {address}")
    
    def lock(self):
        """Lock ROM to prevent further writes"""
        self.locked = True
    
    def unlock(self):
        """Unlock ROM to allow programming"""
        self.locked = False


class EEPROM:
    """Electrically Erasable Programmable ROM - For BIOS settings"""
    
    def __init__(self, size: int = 128):
        """Initialize EEPROM"""
        self.size = size
        self.memory = [0xFF] * size  # EEPROM defaults to 0xFF
        self.write_cycles = [0] * size
        self.max_write_cycles = 100000
    
    def read(self, address: int) -> int:
        """Read from EEPROM"""
        if 0 <= address < self.size:
            return self.memory[address]
        raise MemoryError(f"EEPROM read address out of bounds: {address}")
    
    def write(self, address: int, value: int):
        """Write to EEPROM (limited write cycles)"""
        if 0 <= address < self.size:
            if self.write_cycles[address] < self.max_write_cycles:
                self.memory[address] = value & 0xFF
                self.write_cycles[address] += 1
            else:
                raise MemoryError(f"EEPROM cell {address} exceeded write cycles")
        else:
            raise MemoryError(f"EEPROM address out of bounds: {address}")
    
    def erase(self):
        """Erase all EEPROM (set to 0xFF)"""
        self.memory = [0xFF] * self.size


class Storage:
    """Persistent storage device (like HDD/SSD)"""
    
    def __init__(self, size: int = 65536):
        """Initialize storage with size in bytes"""
        self.size = size
        self.sectors = [[0] * 512 for _ in range(size // 512)]
        self.read_count = 0
        self.write_count = 0
    
    def read_sector(self, sector: int) -> List[int]:
        """Read 512-byte sector"""
        if 0 <= sector < len(self.sectors):
            self.read_count += 1
            return self.sectors[sector].copy()
        raise IOError(f"Storage sector out of bounds: {sector}")
    
    def write_sector(self, sector: int, data: List[int]):
        """Write 512-byte sector"""
        if 0 <= sector < len(self.sectors):
            if len(data) <= 512:
                self.write_count += 1
                self.sectors[sector] = (data + [0] * 512)[:512]
            else:
                raise ValueError("Data exceeds sector size")
        else:
            raise IOError(f"Storage sector out of bounds: {sector}")

# ============================================================================
# CMOS (Complementary Metal-Oxide-Semiconductor)
# ============================================================================

@dataclass
class CMOSSettings:
    """CMOS configuration data"""
    year: int = 2026
    month: int = 3
    day: int = 2
    hour: int = 0
    minute: int = 0
    second: int = 0
    boot_order: List[str] = None
    cpu_speed: int = 8  # MHz
    ram_size: int = 256  # bytes
    
    def __post_init__(self):
        if self.boot_order is None:
            self.boot_order = ["HDD", "ROM"]


class CMOS:
    """CMOS - Stores BIOS settings and real-time clock"""
    
    def __init__(self):
        """Initialize CMOS with default settings"""
        self.settings = CMOSSettings()
        self.battery_backed_ram = [0] * 128
        self.battery_level = 100  # percentage
    
    def get_time(self) -> Dict[str, int]:
        """Get current time from RTC"""
        return {
            'year': self.settings.year,
            'month': self.settings.month,
            'day': self.settings.day,
            'hour': self.settings.hour,
            'minute': self.settings.minute,
            'second': self.settings.second
        }
    
    def set_time(self, year: int, month: int, day: int, hour: int, minute: int, second: int):
        """Set RTC time"""
        self.settings.year = year
        self.settings.month = month
        self.settings.day = day
        self.settings.hour = hour
        self.settings.minute = minute
        self.settings.second = second
    
    def get_setting(self, key: str):
        """Get CMOS setting"""
        return getattr(self.settings, key, None)
    
    def set_setting(self, key: str, value):
        """Set CMOS setting"""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)

# ============================================================================
# BIOS (Basic Input/Output System)
# ============================================================================

class BIOS:
    """BIOS - Handles hardware initialization and boot process"""
    
    def __init__(self, rom: ROM, cmos: CMOS):
        """Initialize BIOS with ROM and CMOS"""
        self.rom = rom
        self.cmos = cmos
        self.version = "1.0.0"
        self.initialized = False
    
    def power_on_self_test(self, ram: RAM, cpu: 'CPU') -> bool:
        """POST - Power-On Self Test"""
        print("=" * 60)
        print(f"BIOS Version {self.version}")
        print("Performing Power-On Self Test (POST)...")
        print("=" * 60)
        
        # Test CPU
        print("Testing CPU...", end=" ")
        if cpu:
            print("OK")
        else:
            print("FAIL")
            return False
        
        # Test RAM
        print(f"Testing RAM ({ram.size} bytes)...", end=" ")
        try:
            ram.write(0, 0xAA)
            if ram.read(0) == 0xAA:
                ram.write(0, 0x55)
                if ram.read(0) == 0x55:
                    print("OK")
                else:
                    print("FAIL")
                    return False
            else:
                print("FAIL")
                return False
        except:
            print("FAIL")
            return False
        
        # Check CMOS
        print("Checking CMOS...", end=" ")
        time_data = self.cmos.get_time()
        print(f"OK (Date: {time_data['year']}-{time_data['month']:02d}-{time_data['day']:02d})")
        
        print("\nPOST completed successfully!")
        self.initialized = True
        return True
    
    def boot(self, storage: Storage = None) -> bool:
        """Boot sequence - load OS from storage"""
        if not self.initialized:
            print("ERROR: POST not completed")
            return False
        
        print("\nBooting system...")
        boot_order = self.cmos.get_setting('boot_order')
        
        for device in boot_order:
            print(f"Attempting to boot from {device}...", end=" ")
            if device == "HDD" and storage:
                bootloader = storage.read_sector(0)
                if bootloader[510] == 0x55 and bootloader[511] == 0xAA:
                    print("Bootloader found!")
                    return True
                else:
                    print("No bootloader")
            elif device == "ROM":
                print("ROM boot not implemented")
        
        print("\nNo bootable device found!")
        return False

# ============================================================================
# CPU REGISTERS
# ============================================================================

@dataclass
class Registers:
    """CPU Registers (8-bit)"""
    A: int = 0      # Accumulator
    B: int = 0      # General purpose
    C: int = 0      # General purpose
    D: int = 0      # General purpose
    PC: int = 0     # Program Counter
    SP: int = 0xFF  # Stack Pointer
    FLAGS: int = 0  # Flags register (Z, C, N, O)
    
    def get_flag(self, flag: str) -> int:
        """Get flag value (Z=Zero, C=Carry, N=Negative, O=Overflow)"""
        flags = {'Z': 0, 'C': 1, 'N': 2, 'O': 3}
        if flag in flags:
            return (self.FLAGS >> flags[flag]) & 1
        return 0
    
    def set_flag(self, flag: str, value: int):
        """Set flag value"""
        flags = {'Z': 0, 'C': 1, 'N': 2, 'O': 3}
        if flag in flags:
            if value:
                self.FLAGS |= (1 << flags[flag])
            else:
                self.FLAGS &= ~(1 << flags[flag])

# ============================================================================
# INSTRUCTION SET
# ============================================================================

class Opcode(Enum):
    """8-bit CPU Instruction Set"""
    NOP = 0x00      # No operation
    LDA = 0x01      # Load A from memory
    LDB = 0x02      # Load B from memory
    STA = 0x03      # Store A to memory
    STB = 0x04      # Store B to memory
    ADD = 0x10      # A = A + B
    SUB = 0x11      # A = A - B
    AND = 0x12      # A = A AND B
    OR  = 0x13      # A = A OR B
    XOR = 0x14      # A = A XOR B
    NOT = 0x15      # A = NOT A
    SHL = 0x16      # Shift left
    SHR = 0x17      # Shift right
    JMP = 0x20      # Jump to address
    JZ  = 0x21      # Jump if zero
    JNZ = 0x22      # Jump if not zero
    CALL = 0x30     # Call subroutine
    RET = 0x31      # Return from subroutine
    PUSH = 0x40     # Push to stack
    POP = 0x41      # Pop from stack
    HLT = 0xFF      # Halt

# ============================================================================
# CPU (Central Processing Unit)
# ============================================================================

class CPU:
    """8-bit CPU with basic instruction set"""
    
    def __init__(self, ram: RAM):
        """Initialize CPU with RAM"""
        self.ram = ram
        self.registers = Registers()
        self.clock_speed = 8  # MHz (simulated)
        self.cycles = 0
        self.halted = False
    
    def fetch(self) -> int:
        """Fetch instruction from memory"""
        instruction = self.ram.read(self.registers.PC)
        self.registers.PC = (self.registers.PC + 1) & 0xFF
        self.cycles += 1
        return instruction
    
    def execute(self, opcode: int):
        """Execute instruction"""
        self.cycles += 1
        
        if opcode == Opcode.NOP.value:
            pass
        
        elif opcode == Opcode.LDA.value:
            addr = self.fetch()
            self.registers.A = self.ram.read(addr)
        
        elif opcode == Opcode.LDB.value:
            addr = self.fetch()
            self.registers.B = self.ram.read(addr)
        
        elif opcode == Opcode.STA.value:
            addr = self.fetch()
            self.ram.write(addr, self.registers.A)
        
        elif opcode == Opcode.STB.value:
            addr = self.fetch()
            self.ram.write(addr, self.registers.B)
        
        elif opcode == Opcode.ADD.value:
            result = self.registers.A + self.registers.B
            self.registers.set_flag('C', 1 if result > 255 else 0)
            self.registers.A = result & 0xFF
            self.registers.set_flag('Z', 1 if self.registers.A == 0 else 0)
        
        elif opcode == Opcode.SUB.value:
            result = self.registers.A - self.registers.B
            self.registers.set_flag('C', 1 if result < 0 else 0)
            self.registers.A = result & 0xFF
            self.registers.set_flag('Z', 1 if self.registers.A == 0 else 0)
        
        elif opcode == Opcode.AND.value:
            a_bits = BinaryOperations.int_to_8bit(self.registers.A)
            b_bits = BinaryOperations.int_to_8bit(self.registers.B)
            result = [AND(a_bits[i], b_bits[i]) for i in range(8)]
            self.registers.A = BinaryOperations.bit_to_int(result)
            self.registers.set_flag('Z', 1 if self.registers.A == 0 else 0)
        
        elif opcode == Opcode.OR.value:
            a_bits = BinaryOperations.int_to_8bit(self.registers.A)
            b_bits = BinaryOperations.int_to_8bit(self.registers.B)
            result = [OR(a_bits[i], b_bits[i]) for i in range(8)]
            self.registers.A = BinaryOperations.bit_to_int(result)
            self.registers.set_flag('Z', 1 if self.registers.A == 0 else 0)
        
        elif opcode == Opcode.XOR.value:
            a_bits = BinaryOperations.int_to_8bit(self.registers.A)
            b_bits = BinaryOperations.int_to_8bit(self.registers.B)
            result = [XOR(a_bits[i], b_bits[i]) for i in range(8)]
            self.registers.A = BinaryOperations.bit_to_int(result)
            self.registers.set_flag('Z', 1 if self.registers.A == 0 else 0)
        
        elif opcode == Opcode.NOT.value:
            a_bits = BinaryOperations.int_to_8bit(self.registers.A)
            result = [NOT(bit) for bit in a_bits]
            self.registers.A = BinaryOperations.bit_to_int(result)
        
        elif opcode == Opcode.JMP.value:
            addr = self.fetch()
            self.registers.PC = addr
        
        elif opcode == Opcode.JZ.value:
            addr = self.fetch()
            if self.registers.get_flag('Z') == 1:
                self.registers.PC = addr
        
        elif opcode == Opcode.HLT.value:
            self.halted = True
        
        else:
            print(f"Unknown opcode: 0x{opcode:02X}")
    
    def step(self):
        """Execute one instruction"""
        if not self.halted:
            opcode = self.fetch()
            self.execute(opcode)
    
    def run(self, max_cycles: int = 1000):
        """Run CPU until halt or max cycles"""
        while not self.halted and self.cycles < max_cycles:
            self.step()
    
    def reset(self):
        """Reset CPU"""
        self.registers = Registers()
        self.cycles = 0
        self.halted = False

# ============================================================================
# GPU (Graphics Processing Unit - Simple)
# ============================================================================

class GPU:
    """Simple 8-bit GPU for text and simple graphics"""
    
    def __init__(self, width: int = 40, height: int = 25):
        """Initialize GPU with text buffer"""
        self.width = width
        self.height = height
        self.text_buffer = [[' ' for _ in range(width)] for _ in range(height)]
        self.framebuffer = [[0 for _ in range(width)] for _ in range(height)]
        self.cursor_x = 0
        self.cursor_y = 0
    
    def clear_screen(self):
        """Clear screen"""
        self.text_buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.cursor_x = 0
        self.cursor_y = 0
    
    def put_char(self, x: int, y: int, char: str):
        """Put character at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.text_buffer[y][x] = char
    
    def print_text(self, text: str):
        """Print text at cursor position"""
        for char in text:
            if char == '\n':
                self.cursor_y += 1
                self.cursor_x = 0
            else:
                self.put_char(self.cursor_x, self.cursor_y, char)
                self.cursor_x += 1
                if self.cursor_x >= self.width:
                    self.cursor_x = 0
                    self.cursor_y += 1
    
    def render(self) -> str:
        """Render screen to string"""
        output = "+" + "-" * self.width + "+\n"
        for row in self.text_buffer:
            output += "|" + ''.join(row) + "|\n"
        output += "+" + "-" * self.width + "+"
        return output
    
    def set_pixel(self, x: int, y: int, value: int):
        """Set pixel in framebuffer"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.framebuffer[y][x] = value & 0xFF

# ============================================================================
# SIMPLE OPERATING SYSTEM
# ============================================================================

class SimpleOS:
    """Simple 8-bit Operating System"""
    
    def __init__(self, cpu: CPU, ram: RAM, storage: Storage, gpu: GPU):
        """Initialize OS"""
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.gpu = gpu
        self.running = False
        self.version = "SimpleOS v1.0"
    
    def boot(self):
        """Boot operating system"""
        self.running = True
        self.gpu.clear_screen()
        self.gpu.print_text(f"{self.version}\n")
        self.gpu.print_text("System Ready\n")
        return self.gpu.render()
    
    def load_program(self, program: List[int], start_address: int = 0):
        """Load program into RAM"""
        for i, byte in enumerate(program):
            self.ram.write(start_address + i, byte)
    
    def execute_program(self):
        """Execute program in RAM"""
        self.cpu.reset()
        self.cpu.run()
    
    def shutdown(self):
        """Shutdown OS"""
        self.running = False
        self.gpu.print_text("\nSystem Halted\n")
        return self.gpu.render()


if __name__ == "__main__":
    print("8-bit Computer Components Demo")
    print("=" * 60)
    
    # Initialize components
    ram = RAM(256)
    rom = ROM(256)
    eeprom = EEPROM(128)
    storage = Storage(65536)
    cmos = CMOS()
    
    # Initialize CPU and GPU
    cpu = CPU(ram)
    gpu = GPU(40, 25)
    
    # Initialize BIOS
    bios = BIOS(rom, cmos)
    
    # Run POST
    bios.power_on_self_test(ram, cpu)
    
    # Create simple OS
    os = SimpleOS(cpu, ram, storage, gpu)
    print("\n" + os.boot())
    
    # Simple program: Load 5 into A, load 3 into B, add them, store result
    program = [
        0x01, 0x10,  # LDA [0x10]
        0x02, 0x11,  # LDB [0x11]
        0x10,        # ADD
        0x03, 0x12,  # STA [0x12]
        0xFF         # HLT
    ]
    
    # Data
    ram.write(0x10, 5)
    ram.write(0x11, 3)
    
    print("\nLoading and executing program...")
    os.load_program(program, 0x00)
    os.execute_program()
    
    result = ram.read(0x12)
    print(f"Result: {result} (5 + 3)")
    print(f"CPU Cycles: {cpu.cycles}")
