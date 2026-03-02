"""
GUI and UI Layout System
Text-based interface with visual components
Includes input/output displays, transistor diagrams, and system blueprints
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import os

# ============================================================================
# UI COMPONENTS
# ============================================================================

class UIComponent:
    """Base class for UI components"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_style = "single"
    
    def render(self) -> List[str]:
        """Render component to list of strings"""
        raise NotImplementedError("Subclass must implement render()")

class Box(UIComponent):
    """Box UI component with border"""
    
    BORDER_STYLES = {
        'single': {'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘', 'h': '─', 'v': '│'},
        'double': {'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝', 'h': '═', 'v': '║'},
        'thick': {'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛', 'h': '━', 'v': '┃'},
    }
    
    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        super().__init__(x, y, width, height)
        self.title = title
        self.content: List[str] = []
    
    def add_line(self, text: str):
        """Add line to box content"""
        self.content.append(text)
    
    def render(self) -> List[str]:
        """Render box with border"""
        border = self.BORDER_STYLES[self.border_style]
        lines = []
        
        # Top border
        top = border['tl'] + border['h'] * (self.width - 2) + border['tr']
        if self.title:
            title_text = f" {self.title} "
            pos = (self.width - len(title_text)) // 2
            top = border['tl'] + border['h'] * pos + title_text + border['h'] * (self.width - pos - len(title_text) - 1) + border['tr']
        lines.append(top)
        
        # Content lines
        for i in range(self.height - 2):
            if i < len(self.content):
                text = self.content[i][:self.width - 4]
                line = border['v'] + ' ' + text.ljust(self.width - 4) + ' ' + border['v']
            else:
                line = border['v'] + ' ' * (self.width - 2) + border['v']
            lines.append(line)
        
        # Bottom border
        lines.append(border['bl'] + border['h'] * (self.width - 2) + border['br'])
        
        return lines

class TextDisplay(UIComponent):
    """Text display component"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.lines: List[str] = []
    
    def set_text(self, text: str):
        """Set display text"""
        self.lines = text.split('\n')[:self.height]
    
    def render(self) -> List[str]:
        """Render text"""
        rendered = []
        for i in range(self.height):
            if i < len(self.lines):
                rendered.append(self.lines[i][:self.width].ljust(self.width))
            else:
                rendered.append(' ' * self.width)
        return rendered

class Button(UIComponent):
    """Button component"""
    
    def __init__(self, x: int, y: int, width: int, label: str):
        super().__init__(x, y, width, 3)
        self.label = label
        self.selected = False
    
    def render(self) -> List[str]:
        """Render button"""
        if self.selected:
            top = '╔' + '═' * (self.width - 2) + '╗'
            mid = '║' + self.label.center(self.width - 2) + '║'
            bot = '╚' + '═' * (self.width - 2) + '╝'
        else:
            top = '┌' + '─' * (self.width - 2) + '┐'
            mid = '│' + self.label.center(self.width - 2) + '│'
            bot = '└' + '─' * (self.width - 2) + '┘'
        
        return [top, mid, bot]

# ============================================================================
# TRANSISTOR DIAGRAMS
# ============================================================================

class TransistorDiagram:
    """Generate ASCII art transistor diagrams"""
    
    @staticmethod
    def nand_transistor() -> str:
        """NAND gate transistor-level diagram"""
        return """
    NAND Gate Transistor-Level Diagram
    ====================================
    
         Vcc (+5V)
           |
           ├─────────┐
           │         │
          ┌┴┐       ┌┴┐
        ──┤Q1├──   ──┤Q2├──  (PMOS)
          └┬┘       └┬┘
           │         │
        A──┤       B─┤
           │         │
           ├─────────┼────── OUT
           │         │
          ┌┴┐       ┌┴┐
        ──┤Q3├──   ──┤Q4├──  (NMOS)
          └┬┘       └┬┘
           │         │
        A──┤       B─┤
           │         │
          GND       GND
    
    Truth Table:
    A | B | OUT
    --|---|----
    0 | 0 |  1
    0 | 1 |  1
    1 | 0 |  1
    1 | 1 |  0
"""
    
    @staticmethod
    def inverter_transistor() -> str:
        """NOT gate (Inverter) transistor diagram"""
        return """
    NOT Gate (Inverter) Transistor Diagram
    =======================================
    
         Vcc (+5V)
           |
          ┌┴┐
        ──┤Q1├──  (PMOS)
          └┬┘
           │
        IN─┤
           ├────── OUT
           │
          ┌┴┐
        ──┤Q2├──  (NMOS)
          └┬┘
           │
        IN─┤
           │
          GND
    
    Truth Table:
    IN | OUT
    ---|----
     0 |  1
     1 |  0
"""
    
    @staticmethod
    def and_gate_cmos() -> str:
        """AND gate using CMOS"""
        return """
    AND Gate (NAND + NOT) CMOS Implementation
    ==========================================
    
         ┌────────────┐      ┌───────┐
    A ───┤            │      │       │
         │   NAND     ├──────┤  NOT  ├───── OUT
    B ───┤   Gate     │      │       │
         └────────────┘      └───────┘
    
    Composition: AND = NAND + NOT
    
    Stage 1 (NAND):     Stage 2 (NOT):
         Vcc                 Vcc
          │                   │
        ┌─┴─┬─┐              ┌┴┐
        │P1 │P2│            ──┤P├──
        └─┬─┴─┘              └┬┘
     A────┤B                  │
          │                NAND─┤
        ┌─┴─┐                  │
        │N1 │N2│              ┌┴┐
        └─┬─┴─┘              ──┤N├──
     A────┤B                  └┬┘
        GND                   GND
    
    Truth Table:
    A | B | NAND | AND
    --|---|------|----
    0 | 0 |  1   |  0
    0 | 1 |  1   |  0
    1 | 0 |  1   |  0
    1 | 1 |  0   |  1
"""
    
    @staticmethod
    def full_adder_transistor() -> str:
        """Full adder transistor-level"""
        return """
    Full Adder Transistor-Level Implementation
    ===========================================
    
    Inputs: A, B, Cin
    Outputs: Sum, Cout
    
    Components:
    - 2 XOR gates (for Sum)
    - 2 AND gates (for Carry)
    - 1 OR gate (for Carry)
    
        A ───┐
             │  XOR ───┐
        B ───┘         │  XOR ─── Sum
                       │
              Cin ─────┘
        
        A ───┐
             │  AND ───┐
        B ───┘         │
                       │  OR ──── Cout
        (A⊕B) ────┐    │
                  │ AND┘
           Cin ───┘
    
    Transistor Count:
    - XOR: 12 transistors each × 2 = 24
    - AND: 6 transistors each × 2 = 12
    - OR: 6 transistors = 6
    Total: 42 transistors
    
    Truth Table:
    A | B | Cin | Sum | Cout
    --|---|-----|-----|-----
    0 | 0 |  0  |  0  |  0
    0 | 0 |  1  |  1  |  0
    0 | 1 |  0  |  1  |  0
    0 | 1 |  1  |  0  |  1
    1 | 0 |  0  |  1  |  0
    1 | 0 |  1  |  0  |  1
    1 | 1 |  0  |  0  |  1
    1 | 1 |  1  |  1  |  1
"""

# ============================================================================
# FLASH TABLES
# ============================================================================

class FlashTable:
    """Flash memory truth tables and characteristics"""
    
    @staticmethod
    def flash_cell_diagram() -> str:
        """Flash memory cell diagram"""
        return """
    Flash Memory Cell Structure
    ============================
    
            Control Gate (CG)
                  │
                  │
          ┌───────┴───────┐
          │   Oxide Layer  │
          │  (Insulator)   │
          ├────────────────┤
          │  Floating Gate │ ← Stores charge
          │   (Isolated)   │
          ├────────────────┤
          │   Oxide Layer  │
          └────────────────┘
                  │
         ┌────────┴────────┐
         │   Source    Drain│
         │      │       │   │
         └──────┼───────┼───┘
                │       │
              Channel (Si)
    
    States:
    ╔═══════════╦══════════╦═══════════════╗
    ║ State     ║ Charge   ║ Binary Value  ║
    ╠═══════════╬══════════╬═══════════════╣
    ║ Erased    ║ No charge║      1        ║
    ║ Programmed║ Charged  ║      0        ║
    ╚═══════════╩══════════╩═══════════════╝
"""
    
    @staticmethod
    def flash_operations_table() -> str:
        """Flash memory operations"""
        return """
    Flash Memory Operations
    ========================
    
    ╔═══════════╦═══════════════╦════════════╦════════════╗
    ║ Operation ║ Voltage (CG)  ║ Time       ║ Effect     ║
    ╠═══════════╬═══════════════╬════════════╬════════════╣
    ║ READ      ║ +5V           ║ ~25ns      ║ Check cell ║
    ║ PROGRAM   ║ +12V          ║ ~100µs     ║ Write 0    ║
    ║ ERASE     ║ -12V          ║ ~1ms       ║ Write 1    ║
    ╚═══════════╩═══════════════╩════════════╩════════════╝
    
    Endurance: ~100,000 Program/Erase cycles
    Retention: 10+ years
    
    Flash Types:
    ┌─────────────┬──────────────────────────────┐
    │ Type        │ Characteristics              │
    ├─────────────┼──────────────────────────────┤
    │ NOR Flash   │ - Random access              │
    │             │ - Execute in place           │
    │             │ - Slower write               │
    │             │ - Used for: BIOS, firmware   │
    ├─────────────┼──────────────────────────────┤
    │ NAND Flash  │ - Sequential access          │
    │             │ - High density               │
    │             │ - Faster write               │
    │             │ - Used for: Storage, SSD     │
    └─────────────┴──────────────────────────────┘
"""
    
    @staticmethod
    def eeprom_vs_flash_table() -> str:
        """EEPROM vs Flash comparison"""
        return """
    EEPROM vs Flash Memory Comparison
    ==================================
    
    ╔═══════════════╦════════════════╦════════════════╗
    ║ Feature       ║ EEPROM         ║ Flash Memory   ║
    ╠═══════════════╬════════════════╬════════════════╣
    ║ Erase Unit    ║ Byte-level     ║ Block-level    ║
    ║ Write Speed   ║ Slow (~5ms)    ║ Fast (~100µs)  ║
    ║ Density       ║ Low            ║ High           ║
    ║ Cost/Bit      ║ High           ║ Low            ║
    ║ Endurance     ║ 1M cycles      ║ 100K cycles    ║
    ║ Use Cases     ║ Config data    ║ Mass storage   ║
    ╚═══════════════╩════════════════╩════════════════╝
"""

# ============================================================================
# 8-BIT SYSTEM BLUEPRINT
# ============================================================================

class SystemBlueprint:
    """8-bit computer system blueprints"""
    
    @staticmethod
    def full_system_diagram() -> str:
        """Complete 8-bit system diagram"""
        return """
    8-Bit Computer System Architecture Blueprint
    =============================================
    
                    ┌─────────────────────────────────────────────┐
                    │         8-BIT COMPUTER SYSTEM               │
                    └─────────────────────────────────────────────┘
    
    ┌───────────────────────────────────────────────────────────────────┐
    │                         SYSTEM BUS (8-bit data, 8-bit address)    │
    └───┬───────┬───────┬───────┬───────┬───────┬───────┬──────────────┘
        │       │       │       │       │       │       │
    ┌───┴────┐ ┌┴─────┐ ┌┴────┐ ┌┴────┐ ┌┴────┐ ┌┴────┐ ┌┴────────┐
    │  CPU   │ │ RAM  │ │ ROM │ │EEPROM│ │CMOS │ │BIOS │ │ Storage │
    │ 8-bit  │ │256B  │ │256B │ │ 128B │ │128B │ │ FW  │ │  64KB   │
    └────────┘ └──────┘ └─────┘ └──────┘ └─────┘ └─────┘ └─────────┘
        │
    ┌───┴───────────────────────────────────────────────────────────┐
    │                    CPU Internal Architecture                   │
    ├────────────────────────────────────────────────────────────────┤
    │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
    │  │  Registers   │  │     ALU      │  │  Control Unit       │ │
    │  │  ┌────────┐  │  │   ┌──────┐   │  │  ┌──────────────┐  │ │
    │  │  │   A    │  │  │   │ ADD  │   │  │  │  Instruction │  │ │
    │  │  ├────────┤  │  │   ├──────┤   │  │  │   Decoder    │  │ │
    │  │  │   B    │  │  │   │ SUB  │   │  │  └──────────────┘  │ │
    │  │  ├────────┤  │  │   ├──────┤   │  │  ┌──────────────┐  │ │
    │  │  │   C    │  │  │   │ AND  │   │  │  │   Sequencer  │  │ │
    │  │  ├────────┤  │  │   ├──────┤   │  │  └──────────────┘  │ │
    │  │  │   D    │  │  │   │  OR  │   │  └────────┬────────────┘ │
    │  │  ├────────┤  │  │   ├──────┤   │           │              │
    │  │  │   PC   │  │  │   │ XOR  │   │      ┌────┴────┐         │
    │  │  ├────────┤  │  │   ├──────┤   │      │ Clock   │         │
    │  │  │   SP   │  │  │   │ SHL  │   │      │ 8 MHz   │         │
    │  │  ├────────┤  │  │   ├──────┤   │      └─────────┘         │
    │  │  │ FLAGS  │  │  │   │ SHR  │   │                           │
    │  │  └────────┘  │  │   └──────┘   │                           │
    │  └──────────────┘  └──────────────┘                           │
    └────────────────────────────────────────────────────────────────┘
    
    ┌────────────────────────────────────────────────────────────────┐
    │                     I/O and Peripherals                        │
    ├────────────────────────────────────────────────────────────────┤
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
    │  │   GPU    │  │ Keyboard │  │  Display │  │    Serial    │  │
    │  │  40x25   │  │  Input   │  │  Output  │  │     Port     │  │
    │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
    └────────────────────────────────────────────────────────────────┘
    
    Signal Flow:
    ╔═══════════════════════════════════════════════════════════════╗
    ║  Clock → Control Unit → ALU → Registers → Memory Bus          ║
    ║     ↑                                           ↓              ║
    ║     └─────────── Feedback Loop ←────────────────┘             ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    Power Distribution:
    +5V ────┬────┬───────┬───────┬──────────┬────────┐
            │    │       │       │          │        │
          CPU  RAM    ROM   EEPROM   CMOS   Peripherals
            │    │       │       │          │        │
    GND ────┴────┴───────┴───────┴──────────┴────────┘
"""
    
    @staticmethod
    def cpu_datapath_diagram() -> str:
        """CPU datapath detailed diagram"""
        return """
    CPU Datapath - Detailed Architecture
    =====================================
    
                        Instruction Fetch
                              │
                    ┌─────────┴──────────┐
                    │   Program Counter  │
                    │       (PC)         │
                    └─────────┬──────────┘
                              │
                    ┌─────────┴──────────┐
                    │  Instruction Memory │
                    │     (ROM/RAM)      │
                    └─────────┬──────────┘
                              │
                    ┌─────────┴──────────┐
                    │ Instruction Register│
                    │       (IR)          │
                    └─────────┬──────────┘
                              │
                    ┌─────────┴──────────┐
                    │  Instruction Decoder│
                    └────┬────────┬───────┘
                         │        │
                 ┌───────┘        └────────┐
                 │                          │
         ┌───────┴────────┐       ┌────────┴──────┐
         │  Register File │       │  Control Unit  │
         │  ┌──┐  ┌──┐    │       │                │
         │  │A │  │B │    │       │  State Machine │
         │  └──┘  └──┘    │       │  & Sequencer   │
         └───┬────────┬───┘       └────────────────┘
             │        │
         ┌───┴────────┴───┐
         │      ALU        │
         │  ┌──────────┐   │
         │  │ Adder    │   │
         │  ├──────────┤   │
         │  │ Logic    │   │
         │  ├──────────┤   │
         │  │ Shifter  │   │
         │  └──────────┘   │
         └────────┬─────────┘
                  │
         ┌────────┴─────────┐
         │   Result Bus     │
         └────────┬─────────┘
                  │
         ┌────────┴─────────┐
         │  Write-Back      │
                 │
         ┌────────┴─────────┐
         │   Data Memory    │
         │     (RAM)        │
         └──────────────────┘
    
    Pipeline Stages:
    ╔═══════════════════════════════════════════╗
    ║ 1. Fetch (IF)    │ Get instruction        ║
    ║ 2. Decode (ID)   │ Decode & read regs     ║
    ║ 3. Execute (EX)  │ ALU operation          ║
    ║ 4. Memory (MEM)  │ Access memory          ║
    ║ 5. Write-Back(WB)│ Write result to reg    ║
    ╚═══════════════════════════════════════════╝
"""
    
    @staticmethod
    def memory_hierarchy_diagram() -> str:
        """Memory hierarchy diagram"""
        return """
    Memory Hierarchy and Organization
    ==================================
    
              ┌────────────────────────────┐
              │     CPU Registers (8B)     │ ← Fastest
              │  Access: 0 cycles          │
              └──────────┬─────────────────┘
                         │
              ┌──────────┴─────────────────┐
              │      Cache (Optional)      │
              │  Access: 1-2 cycles        │
              └──────────┬─────────────────┘
                         │
              ┌──────────┴─────────────────┐
              │      RAM (256 bytes)       │
              │  Access: 2-4 cycles        │
              │  ┌──────────────────────┐  │
              │  │ Stack  │  Heap       │  │
              │  │ 0xFF─→ │  ←─0x00     │  │
              │  └──────────────────────┘  │
              └──────────┬─────────────────┘
                         │
              ┌──────────┴─────────────────┐
              │    ROM/EEPROM (384B)       │
              │  Access: 4-8 cycles        │
              │  ┌──────────────────────┐  │
              │  │  BIOS  │  Firmware   │  │
              │  └──────────────────────┘  │
              └──────────┬─────────────────┘
                         │
              ┌──────────┴─────────────────┐
              │     Storage (64KB)         │ ← Slowest
              │  Access: 100+ cycles       │
              │  ┌──────────────────────┐  │
              │  │ Files │ Programs │OS │  │
              │  └──────────────────────┘  │
              └────────────────────────────┘
    
    Memory Map:
    ╔═══════════╦═════════════╦══════════════════════╗
    ║  Address  ║   Size      ║  Usage               ║
    ╠═══════════╬═════════════╬══════════════════════╣
    ║ 0x00-0x0F ║  16 bytes   ║  System vectors       ║
    ║ 0x10-0x7F ║  112 bytes  ║  User program        ║
    ║ 0x80-0xEF ║  112 bytes  ║  Stack space         ║
    ║ 0xF0-0xFF ║  16 bytes   ║  System variables    ║
    ╚═══════════╩═════════════╩══════════════════════╝
"""

# ============================================================================
# MAIN UI CLASS
# ============================================================================

class LogicGatesUI:
    """Main UI for logic gates system"""
    
    def __init__(self):
        self.screen_width = 80
        self.screen_height = 40
        self.components: List[UIComponent] = []
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_main_menu(self):
        """Create main menu UI"""
        self.clear_screen()
        
        title = Box(0, 0, 78, 5, "8-Bit Logic Gates System")
        title.border_style = "double"
        title.add_line("Complete Computer Architecture Simulation")
        title.add_line("Version 1.0.0")
        
        menu = Box(0, 6, 78, 20, "Main Menu")
        menu.add_line("1. Logic Gates Operations")
        menu.add_line("2. Calculator Functions")
        menu.add_line("3. Assembly Programming")
        menu.add_line("4. CPU Execution")
        menu.add_line("5. Memory Management")
        menu.add_line("6. Transistor Diagrams")
        menu.add_line("7. System Blueprints")
        menu.add_line("8. Flash Memory Tables")
        menu.add_line("9. API Documentation")
        menu.add_line("0. Exit")
        
        for line in title.render():
            print(line)
        
        for line in menu.render():
            print(line)
    
    def show_transistor_diagrams(self):
        """Display transistor diagrams"""
        self.clear_screen()
        print(TransistorDiagram.nand_transistor())
        input("\nPress Enter to see NOT gate...")
        self.clear_screen()
        print(TransistorDiagram.inverter_transistor())
        input("\nPress Enter to see AND gate...")
        self.clear_screen()
        print(TransistorDiagram.and_gate_cmos())
        input("\nPress Enter to see Full Adder...")
        self.clear_screen()
        print(TransistorDiagram.full_adder_transistor())
    
    def show_flash_tables(self):
        """Display flash memory tables"""
        self.clear_screen()
        print(FlashTable.flash_cell_diagram())
        input("\nPress Enter to continue...")
        self.clear_screen()
        print(FlashTable.flash_operations_table())
        input("\nPress Enter to continue...")
        self.clear_screen()
        print(FlashTable.eeprom_vs_flash_table())
    
    def show_system_blueprints(self):
        """Display system blueprints"""
        self.clear_screen()
        print(SystemBlueprint.full_system_diagram())
        input("\nPress Enter to see CPU datapath...")
        self.clear_screen()
        print(SystemBlueprint.cpu_datapath_diagram())
        input("\nPress Enter to see memory hierarchy...")
        self.clear_screen()
        print(SystemBlueprint.memory_hierarchy_diagram())

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_ui():
    """Demonstrate UI system"""
    ui = LogicGatesUI()
    
    while True:
        ui.create_main_menu()
        choice = input("\nEnter choice: ").strip()
        
        if choice == '6':
            ui.show_transistor_diagrams()
        elif choice == '7':
            ui.show_system_blueprints()
        elif choice == '8':
            ui.show_flash_tables()
        elif choice == '0':
            print("\nShutting down system. Goodbye!")
            break
        else:
            print("\nFeature not yet implemented. Press Enter to continue...")
            input()

if __name__ == "__main__":
    demonstrate_ui()
