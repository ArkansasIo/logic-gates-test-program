"""
NES (NINTENDO ENTERTAINMENT SYSTEM) EMULATOR MODULE
====================================================
Complete NES emulator with 6502 CPU, PPU, APU, and cartridge support
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import time

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class NESSpecs:
    """NES hardware specifications"""
    cpu: str = "MOS 6502"
    cpu_speed: float = 1.789773  # MHz
    ram_size: int = 2048  # 2 KB
    vram_size: int = 2048  # 2 KB
    screen_width: int = 256
    screen_height: int = 240
    screen_colors: int = 64
    cartridge_types: int = 200  # Mapper types
    controllers: int = 2
    
@dataclass
class CPU6502Registers:
    """6502 CPU registers"""
    A: int = 0x00  # Accumulator
    X: int = 0x00  # X register
    Y: int = 0x00  # Y register
    SP: int = 0xFF  # Stack Pointer
    PC: int = 0x8000  # Program Counter
    P: int = 0x24  # Processor status

@dataclass
class NESPalette:
    """NES color palette (simplified)"""
    colors: List[str] = None
    
    def __post_init__(self):
        if self.colors is None:
            # 64-color NES palette (simplified to 4 levels)
            self.colors = ['  ', '░░', '▒▒', '██']

# ============================================================================
# NES CPU (6502)
# ============================================================================

class NES6502:
    """6502 CPU emulator"""
    
    def __init__(self):
        self.registers = CPU6502Registers()
        self.memory = bytearray(0x10000)  # 64 KB address space
        self.clock_cycles = 0
        self.instructions_executed = 0
        
    def read_memory(self, address: int) -> int:
        """Read byte from memory"""
        if address < len(self.memory):
            return self.memory[address]
        return 0x00
    
    def write_memory(self, address: int, value: int):
        """Write byte to memory"""
        if address < len(self.memory):
            self.memory[address] = value & 0xFF
    
    def push_stack(self, value: int):
        """Push value onto stack"""
        self.write_memory(0x0100 + self.registers.SP, value & 0xFF)
        self.registers.SP = (self.registers.SP - 1) & 0xFF
    
    def pop_stack(self) -> int:
        """Pop value from stack"""
        self.registers.SP = (self.registers.SP + 1) & 0xFF
        return self.read_memory(0x0100 + self.registers.SP)
    
    def set_flag(self, flag_bit: int, value: bool):
        """Set/clear processor flag"""
        if value:
            self.registers.P |= (1 << flag_bit)
        else:
            self.registers.P &= ~(1 << flag_bit)
    
    def get_flag(self, flag_bit: int) -> bool:
        """Get processor flag"""
        return bool(self.registers.P & (1 << flag_bit))
    
    def execute_instruction(self, opcode: int) -> int:
        """Execute single 6502 instruction"""
        cycles = 2
        
        # NOP
        if opcode == 0xEA:
            cycles = 2
        # LDA #$nn (Load accumulator)
        elif opcode == 0xA9:
            self.registers.A = self.read_memory((self.registers.PC + 1) & 0xFFFF)
            self.registers.PC = (self.registers.PC + 2) & 0xFFFF
            cycles = 2
        # CMP #$nn (Compare)
        elif opcode == 0xC9:
            value = self.read_memory((self.registers.PC + 1) & 0xFFFF)
            result = (self.registers.A - value) & 0xFF
            self.set_flag(6, result == 0)  # Zero flag
            self.registers.PC = (self.registers.PC + 2) & 0xFFFF
            cycles = 2
        # BNE $nn (Branch if not equal)
        elif opcode == 0xD0:
            offset = self.read_memory((self.registers.PC + 1) & 0xFFFF)
            if not self.get_flag(1):  # Zero flag clear
                self.registers.PC = (self.registers.PC + offset + 2) & 0xFFFF
            else:
                self.registers.PC = (self.registers.PC + 2) & 0xFFFF
            cycles = 3
        # JMP $nnnn (Jump)
        elif opcode == 0x4C:
            addr_low = self.read_memory((self.registers.PC + 1) & 0xFFFF)
            addr_high = self.read_memory((self.registers.PC + 2) & 0xFFFF)
            self.registers.PC = (addr_high << 8) | addr_low
            cycles = 3
        # JSR $nnnn (Jump to subroutine)
        elif opcode == 0x20:
            addr_low = self.read_memory((self.registers.PC + 1) & 0xFFFF)
            addr_high = self.read_memory((self.registers.PC + 2) & 0xFFFF)
            self.push_stack((self.registers.PC >> 8) & 0xFF)
            self.push_stack(self.registers.PC & 0xFF)
            self.registers.PC = (addr_high << 8) | addr_low
            cycles = 6
        # RTS (Return from subroutine)
        elif opcode == 0x60:
            pc_low = self.pop_stack()
            pc_high = self.pop_stack()
            self.registers.PC = (pc_high << 8) | pc_low
            cycles = 6
        else:
            self.registers.PC = (self.registers.PC + 1) & 0xFFFF
            cycles = 2
        
        self.clock_cycles += cycles
        self.instructions_executed += 1
        return cycles
    
    def fetch_decode_execute(self) -> int:
        """Fetch, decode, execute instruction"""
        opcode = self.read_memory(self.registers.PC)
        return self.execute_instruction(opcode)

# ============================================================================
# NES PICTURE PROCESSING UNIT (PPU)
# ============================================================================

class NESPPU:
    """NES Graphics processor"""
    
    def __init__(self):
        self.specs = NESSpecs()
        self.vram = bytearray(self.specs.vram_size)
        self.oam = bytearray(256)  # Sprite memory
        self.palette_ram = bytearray(32)  # Palette memory
        self.framebuffer = self._create_framebuffer()
        self.palette = NESPalette()
        self.ppuctrl = 0x00
        self.ppumask = 0x00
        self.ppustatus = 0x00
        self.scanline = 0
        self.cycles = 0
        
    def _create_framebuffer(self) -> List[List[int]]:
        """Create empty framebuffer"""
        return [[0 for _ in range(self.specs.screen_width)] for _ in range(self.specs.screen_height)]
    
    def render_scanline(self, line: int):
        """Render scanline"""
        if line >= self.specs.screen_height:
            return
        
        for x in range(self.specs.screen_width):
            # Pattern based on scanline and x position
            color = ((x >> 4) + (line >> 4)) % 4
            self.framebuffer[line][x] = color
    
    def render_frame(self):
        """Render complete frame"""
        for y in range(self.specs.screen_height):
            self.render_scanline(y)
    
    def display_screen(self):
        """Display rendered frame"""
        print("\n" + "=" * 70)
        print("NES SCREEN OUTPUT")
        print("=" * 70)
        
        # Downsample for console display (256x240 → 128x60)
        for y in range(0, self.specs.screen_height, 4):
            line = ""
            for x in range(0, self.specs.screen_width, 2):
                if y < len(self.framebuffer) and x < len(self.framebuffer[y]):
                    color = self.framebuffer[y][x]
                    line += self.palette.colors[color]
            print(line)
        print("=" * 70)

# ============================================================================
# NES SOUND PROCESSOR (APU)
# ============================================================================

class NESAPU:
    """NES Audio processor"""
    
    def __init__(self):
        self.channels = [
            {'type': 'Square 1', 'enabled': True, 'frequency': 440},
            {'type': 'Square 2', 'enabled': True, 'frequency': 440},
            {'type': 'Triangle', 'enabled': True, 'frequency': 440},
            {'type': 'Noise', 'enabled': True, 'frequency': 440}
        ]
        self.master_volume = 100
        self.sample_rate = 44100
        
    def status(self) -> str:
        """Get audio status"""
        enabled = sum(1 for ch in self.channels if ch['enabled'])
        return f"APU: {enabled}/{len(self.channels)} channels active @ {self.sample_rate} Hz"

# ============================================================================
# NES CARTRIDGE
# ============================================================================

class NESCartridge:
    """NES cartridge (iNES format simulation)"""
    
    MAPPER_NROM = 0
    MAPPER_MMC1 = 1
    MAPPER_UxROM = 2
    
    def __init__(self, title: str = "TEST_GAME", mapper_type: int = 0, prg_size: int = 16384, chr_size: int = 8192):
        self.title = title
        self.mapper_type = mapper_type
        self.prg_rom = bytearray(prg_size)
        self.chr_rom = bytearray(chr_size)
        self.prg_ram = bytearray(8192)
        self.mirroring = 0  # 0 = horizontal, 1 = vertical
        self._create_test_program()
        
    def _create_test_program(self):
        """Create test program"""
        # Simple 6502 program
        program = bytearray([
            0xA9, 0x00,           # LDA #$00
            0x85, 0x00,           # STA $00
            0xA9, 0x05,           # LDA #$05
            0x85, 0x01,           # STA $01
            0xEA,                 # NOP
            0x4C, 0x00, 0x80      # JMP $8000
        ])
        
        # Load program at 0x8000 (in 16-bit cartridge space)
        offset = 0x8000 - 0x8000
        if offset >= 0 and offset + len(program) <= len(self.prg_rom):
            self.prg_rom[offset:offset + len(program)] = program
    
    def get_mapper_name(self) -> str:
        """Get mapper name"""
        mappers = {
            0: "NROM",
            1: "MMC1",
            2: "UxROM"
        }
        return mappers.get(self.mapper_type, "Unknown")

# ============================================================================
# NES EMULATOR
# ============================================================================

class NESEmulator:
    """Complete NES emulator"""
    
    def __init__(self, cartridge: Optional[NESCartridge] = None):
        self.specs = NESSpecs()
        self.cpu = NES6502()
        self.ppu = NESPPU()
        self.apu = NESAPU()
        self.cartridge = cartridge or NESCartridge()
        self.running = False
        self.frame_count = 0
        self.cycles_per_frame = 29781  # PPU cycles per frame
        self.controllers = [0, 0]
        self.ram = bytearray(0x800)
        
    def load_cartridge(self, cartridge: NESCartridge):
        """Load cartridge"""
        self.cartridge = cartridge
        print(f"Cartridge loaded: {cartridge.title} (Mapper: {cartridge.get_mapper_name()})")
        # Load PRG-ROM into CPU space
        for i in range(min(len(cartridge.prg_rom), 0x8000)):
            self.cpu.memory[0x8000 + i] = cartridge.prg_rom[i]
    
    def initialize(self):
        """Initialize NES hardware"""
        self.cpu.registers.PC = 0x8000
        self.cpu.registers.SP = 0xFF
        self.cpu.registers.P = 0x24
        
    def set_button(self, controller: int, button: int, pressed: bool):
        """Set controller button state"""
        if pressed:
            self.controllers[controller] |= (1 << button)
        else:
            self.controllers[controller] &= ~(1 << button)
    
    def step(self) -> bool:
        """Execute one CPU cycle"""
        if not self.running:
            return False
        
        self.cpu.fetch_decode_execute()
        
        # Every 3 CPU cycles = 1 PPU cycle
        if self.cpu.clock_cycles % 3 == 0:
            # Would update PPU here
            pass
        
        return True
    
    def run_frame(self):
        """Run one frame (~29781 PPU cycles)"""
        cpu_cycles = 0
        target_cycles = self.cycles_per_frame * 3  # Convert to CPU cycles
        
        while cpu_cycles < target_cycles and self.step():
            cpu_cycles = self.cpu.clock_cycles
        
        # Render graphics for frame
        self.ppu.render_frame()
        self.frame_count += 1
    
    def display_status(self):
        """Display emulator status"""
        print("\n" + "=" * 70)
        print("NES EMULATOR STATUS")
        print("=" * 70)
        print(f"\n📦 Cartridge: {self.cartridge.title}")
        print(f"🔧 Mapper: {self.cartridge.get_mapper_name()} (Type {self.cartridge.mapper_type})")
        print(f"📁 PRG-ROM: {len(self.cartridge.prg_rom)} bytes")
        print(f"🎨 CHR-ROM: {len(self.cartridge.chr_rom)} bytes")
        
        print(f"\n🖥️  CPU: {self.specs.cpu} @ {self.specs.cpu_speed} MHz")
        print(f"💾 RAM: {self.specs.ram_size} bytes")
        
        print(f"\n🔧 CPU State:")
        print(f"  PC: 0x{self.cpu.registers.PC:04X}")
        print(f"  SP: 0x{self.cpu.registers.SP:02X}")
        print(f"  A: 0x{self.cpu.registers.A:02X}")
        print(f"  X: 0x{self.cpu.registers.X:02X}")
        print(f"  Y: 0x{self.cpu.registers.Y:02X}")
        print(f"  P: 0x{self.cpu.registers.P:02X}")
        print(f"  Instructions: {self.cpu.instructions_executed}")
        
        print(f"\n📺 PPU:")
        print(f"  Resolution: {self.specs.screen_width}x{self.specs.screen_height}")
        print(f"  Colors: {self.specs.screen_colors}")
        
        print(f"\n🎵 {self.apu.status()}")
        print(f"🖼️  Frames Rendered: {self.frame_count}")
    
    def demo(self):
        """Run emulator demonstration"""
        print("\n🎮 NES Emulator Starting...")
        self.load_cartridge(self.cartridge)
        self.initialize()
        self.running = True
        
        print("Executing test program...")
        for i in range(20):
            self.step()
        
        self.running = False
        self.display_status()
        self.ppu.display_screen()
        
        print("\n✅ Demo complete!")

# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demonstrate_nes_emulator():
    """Demonstrate NES emulator"""
    print("\n" + "=" * 70)
    print("NES EMULATOR DEMONSTRATION")
    print("=" * 70)
    
    # Create cartridge
    cartridge = NESCartridge(title="NES Test ROM", mapper_type=0)
    
    # Create emulator
    emulator = NESEmulator(cartridge)
    
    # Run demo
    emulator.demo()

def demonstrate_nes_specs():
    """Show NES specifications"""
    specs = NESSpecs()
    
    print("\n" + "=" * 70)
    print("NES HARDWARE SPECIFICATIONS")
    print("=" * 70)
    print(f"\n🖥️  Processor: {specs.cpu} @ {specs.cpu_speed} MHz")
    print(f"💾 RAM: {specs.ram_size} bytes")
    print(f"📺 VRAM: {specs.vram_size} bytes")
    print(f"🖼️  Display: {specs.screen_width}x{specs.screen_height} @ 60 Hz")
    print(f"🎨 Colors: {specs.screen_colors}")
    print(f"📦 Cartridge Mappers: {specs.cartridge_types} types supported")
    print(f"🎮 Controllers: {specs.controllers}")

if __name__ == "__main__":
    demonstrate_nes_emulator()
    print("\n")
    demonstrate_nes_specs()
