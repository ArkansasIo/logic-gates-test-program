"""
Interactive Blueprint and Drawing System
Visual circuit design and system layout mapping
Includes circuit schematics, component interconnections, and interactive drawing
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# CIRCUIT DRAWING PRIMITIVES
# ============================================================================

class Component(Enum):
    """Electronic component types"""
    GATE_AND = "AND"
    GATE_OR = "OR"
    GATE_NOT = "NOT"
    GATE_NAND = "NAND"
    GATE_NOR = "NOR"
    GATE_XOR = "XOR"
    RESISTOR = "RES"
    CAPACITOR = "CAP"
    TRANSISTOR = "TRN"
    LED = "LED"
    WIRE = "WIRE"
    POWER = "VCC"
    GROUND = "GND"

@dataclass
class Point:
    """2D point"""
    x: int
    y: int

@dataclass
class Circuit:
    """Circuit schematic"""
    name: str
    components: List[Tuple[Component, Point]]
    connections: List[Tuple[Point, Point]]

class CircuitDrawer:
    """Draw ASCII circuit diagrams"""
    
    @staticmethod
    def draw_and_gate(x: int, y: int) -> List[str]:
        """Draw AND gate symbol"""
        return [
            "     ╭────",
            "  ───┤    ╮",
            "     │ &  ├───",
            "  ───┤    ╯",
            "     ╰────"
        ]
    
    @staticmethod
    def draw_or_gate(x: int, y: int) -> List[str]:
        """Draw OR gate symbol"""
        return [
            "     ╭────",
            "  ───┤    ╮",
            "     │ ≥1 ├───",
            "  ───┤    ╯",
            "     ╰────"
        ]
    
    @staticmethod
    def draw_not_gate(x: int, y: int) -> List[str]:
        """Draw NOT gate symbol"""
        return [
            "       ○",
            "  ────▷○───",
            "       "
        ]
    
    @staticmethod
    def draw_transistor(x: int, y: int) -> List[str]:
        """Draw transistor symbol"""
        return [
            "    C",
            "    │",
            "    ┌┴┐",
            " B──┤ ├",
            "    └┬┘",
            "    │",
            "    E"
        ]
    
    @staticmethod
    def draw_full_adder_circuit() -> str:
        """Complete full adder circuit"""
        return """
    Full Adder Circuit Schematic
    =============================
    
    A ────┬─────────────────┐
          │                 │
          │    ╭────╮       │    ╭────╮
          └────┤    │       └────┤    │
               │XOR1├────┬───────┤    │
          ┌────┤    │    │       │XOR2├──── Sum
          │    ╰────╯    │   ┌───┤    │
    B ────┼──────────────┘   │   ╰────╯
          │                  │
          │                  │
        Cin ─────────────────┴──────────┬───┐
          │                             │   │
          │    ╭────╮              ╭────╮  │
          └────┤    │              │    │  │
               │AND1├───┐      ┌───┤AND2│  │
          ┌────┤    │   │      │   │    │  │
          │    ╰────╯   │      │   ╰────╯  │
    A ────┼─────────────┘      └────────┐  │
          │                              │  │
    B ────┘                         ╭────╮ │
                                    │    │ │
                                ┌───┤ OR ├─┴── Cout
                                │   │    │
                                │   ╰────╯
                                │
    
    Logic Equations:
    Sum  = A ⊕ B ⊕ Cin
    Cout = (A·B) + (Cin·(A⊕B))
"""

    @staticmethod
    def draw_8bit_alu_circuit() -> str:
        """8-bit ALU circuit"""
        return """
    8-Bit ALU (Arithmetic Logic Unit) Circuit
    ==========================================
    
    ┌────────────────────────────────────────────────────────────┐
    │                    8-BIT ALU                               │
    └────────────────────────────────────────────────────────────┘
    
    A[7:0] ─────────┬──────────┬──────────┬──────────┬──────────┐
                    │          │          │          │          │
              ┌─────▼────┐ ┌──▼────┐ ┌──▼────┐ ┌──▼────┐ ┌──▼────┐
              │  ADDER   │ │  AND  │ │  OR   │ │  XOR  │ │SHIFTER│
              │  UNIT    │ │ ARRAY │ │ ARRAY │ │ ARRAY │ │       │
              └─────┬────┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    B[7:0] ─────────┼──────────┼──────────┼──────────┼──────────┤
                    │          │          │          │          │
              ┌─────▼──────────▼──────────▼──────────▼──────────▼──┐
              │            8-to-1 MULTIPLEXER                      │
              │              (Operation Select)                     │
              └─────────────────────┬────────────────────────────┘
                               OP[2:0]
                                    │
                            ┌───────▼────────┐
                            │   Result[7:0]  │
                            │   Flags: CZNV  │
                            └────────────────┘
    
    Operations:
    OP  | Function      | Description
    ----|---------------|---------------------------
    000 | ADD           | A + B
    001 | SUB           | A - B
    010 | AND           | A & B
    011 | OR            | A | B
    100 | XOR           | A ^ B
    101 | SHL           | A << 1
    110 | SHR           | A >> 1
    111 | NOT           | ~A
    
    Flags:
    C = Carry, Z = Zero, N = Negative, V = Overflow
"""

    @staticmethod
    def draw_memory_circuit() -> str:
        """Memory cell circuit"""
        return """
    Static RAM (SRAM) Cell Circuit
    ================================
    
    Word Line (WL)
        │
        ├────────────────────────┐
        │                        │
       ┌┴┐                      ┌┴┐
       │T1│ Access Transistor   │T2│
       └┬┘                      └┬┘
        │                        │
    ┌───┴───┐              ┌────┴────┐
    │       │              │         │
    │  ┌────▽────┐    ┌────▽────┐   │
    │  │ INV 1   │    │ INV 2   │   │
    │  │   Q     ├────┤   Q̄     │   │
    │  └────┬────┘    └────┬────┘   │
    │       └──────────────┘         │
    │                                │
    │                                │
    BL (Bit Line)            B̄L (Bit Line)
    
    SRAM Cell: 6-Transistor (6T) Design
    - 2 Access transistors (T1, T2)
    - 4 Transistors forming 2 inverters
    - Cross-coupled inverters store 1 bit
    
    Dynamic RAM (DRAM) Cell Circuit
    ================================
    
    Word Line (WL)
        │
       ┌┴┐
       │T│ Access Transistor
       └┬┘
        │
       ─┴─  Capacitor (stores charge)
       ─┬─
        │
       ═══ Ground
    
    Bit Line (BL)
    
    DRAM Cell: 1-Transistor 1-Capacitor (1T1C)
    - Simpler than SRAM
    - Requires refresh (charge leaks)
    - Higher density
"""

# ============================================================================
# SYSTEM INTERCONNECTION MAPS
# ============================================================================

class SystemMap:
    """System interconnection diagrams"""
    
    @staticmethod
    def cpu_memory_interconnect() -> str:
        """CPU-Memory interconnection"""
        return """
    CPU-Memory System Interconnection
    ==================================
    
                      ┌──────────────────┐
                      │   ADDRESS BUS    │ (8-bit)
                      │    A[7:0]        │
                      └────────┬─────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────▼────┐          ┌─────▼────┐          ┌────▼────┐
    │   CPU   │          │   RAM    │          │   ROM   │
    │         │          │  (256B)  │          │  (256B) │
    │ ┌─────┐ │          │          │          │         │
    │ │ MAR │ │          └─────┬────┘          └────┬────┘
    │ └──┬──┘ │                │                    │
    │    │    │          ┌─────▼────────────────────▼────┐
    │ ┌──▼──┐ │          │      DATA BUS D[7:0]          │
    │ │ MDR │◄├──────────┤         (8-bit)               │
    │ └─────┘ │          └───────────────────────────────┘
    │         │                     │
    │ ┌─────┐ │          ┌──────────▼──────────┐
    │ │ ALU │ │          │   CONTROL SIGNALS   │
    │ └─────┘ │          │  RD  WR  MREQ  CS   │
    │         │          └─────────────────────┘
    └─────────┘
    
    Signal Descriptions:
    ╔═══════════╦════════════════════════════════════╗
    ║  Signal   ║  Description                       ║
    ╠═══════════╬════════════════════════════════════╣
    ║ A[7:0]    ║ Address bus (256 locations)        ║
    ║ D[7:0]    ║ Data bus (8-bit data)              ║
    ║ RD        ║ Read enable (active low)           ║
    ║ WR        ║ Write enable (active low)          ║
    ║ MREQ      ║ Memory request                     ║
    ║ CS        ║ Chip select                        ║
    ╚═══════════╩════════════════════════════════════╝
    
    Timing Diagram:
    
    CLK  ─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─
          └─┘ └─┘ └─┘ └─┘ └─┘
    
    ADDR ════X═══X═══X═══X═══X═══ Valid Address
    
    RD   ────┘       └───────────  Read Cycle
    
    DATA ════════X═══════X════════ Valid Data
"""
    
    @staticmethod
    def complete_system_map() -> str:
        """Complete system component map"""
        return """
    Complete 8-Bit Computer System Map
    ===================================
    
    ┌───────────────────────────────────────────────────────────────┐
    │                     POWER SUPPLY SYSTEM                        │
    │  +5V DC ────┬────┬────┬────┬────┬────┬────┬────┬────          │
    │             │    │    │    │    │    │    │    │              │
    └─────────────┼────┼────┼────┼────┼────┼────┼────┼──────────────┘
                  │    │    │    │    │    │    │    │
    ┌─────────────▼────▼────▼────▼────▼────▼────▼────▼──────────────┐
    │                      CLOCK GENERATOR                           │
    │        Crystal Oscillator (8 MHz) + Divider                    │
    │  CLK ──────────────────────┬───────────────────────────        │
    └────────────────────────────┼──────────────────────────────────┘
                                 │
         ┌───────────────────────┼────────────────────────┐
         │                       │                        │
    ┌────▼────────┐    ┌─────────▼────────┐    ┌─────────▼────────┐
    │    CPU      │    │    MEMORY        │    │     I/O          │
    │  (8-bit)    │    │   SUBSYSTEM      │    │   DEVICES        │
    │             │    │                  │    │                  │
    │  ┌────────┐ │    │  ┌─────┐        │    │  ┌────────────┐ │
    │  │Reg File│ │    │  │ RAM │ 256B   │    │  │  Keyboard  │ │
    │  │ A B C D│ │    │  └─────┘        │    │  └────────────┘ │
    │  └────────┘ │    │                  │    │                  │
    │  ┌────────┐ │    │  ┌─────┐        │    │  ┌────────────┐ │
    │  │  ALU   │ │    │  │ ROM │ 256B   │    │  │  Display   │ │
    │  │ 8-bit  │ │    │  └─────┘        │    │  │   40x25    │ │
    │  └────────┘ │    │                  │    │  └────────────┘ │
    │  ┌────────┐ │    │  ┌─────┐        │    │                  │
    │  │Control │ │    │  │EEPROM 128B   │    │  ┌────────────┐ │
    │  │  Unit  │ │    │  └─────┘        │    │  │   Serial   │ │
    │  └────────┘ │    │                  │    │  │    Port    │ │
    │             │    │  ┌─────┐        │    │  └────────────┘ │
    │  PC: 0x00   │    │  │CMOS │ 128B   │    │                  │
    │  SP: 0xFF   │    │  └─────┘        │    │  ┌────────────┐ │
    │             │    │                  │    │  │    GPU     │ │
    └─────┬───────┘    └────────┬─────────┘    └────────┬───────┘
          │                     │                       │
    ┌─────▼─────────────────────▼───────────────────────▼─────────┐
    │                   SYSTEM BUS CONTROLLER                      │
    │         Address Bus [7:0] | Data Bus [7:0] | Control        │
    └──────────────────────────────────────────────────────────────┘
          │                     │                       │
    ┌─────▼─────────────────────▼───────────────────────▼─────────┐
    │                    STORAGE SUBSYSTEM                         │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
    │  │   Flash      │  │     BIOS     │  │  Boot Loader │      │
    │  │   64KB       │  │   Firmware   │  │              │      │
    │  └──────────────┘  └──────────────┘  └──────────────┘      │
    └──────────────────────────────────────────────────────────────┘
    
    Component Hierarchy:
    ════════════════════
    
    System
      ├── Power Supply (+5V, GND)
      ├── Clock Generator (8 MHz)
      ├── CPU Core
      │   ├── Register File (A, B, C, D, PC, SP, FLAGS)
      │   ├── ALU (ADD, SUB, AND, OR, XOR, SHL, SHR, NOT)
      │   ├── Control Unit (Instruction Decoder, Sequencer)
      │   └── Program Counter (PC) & Stack Pointer (SP)
      ├── Memory Subsystem
      │   ├── RAM (256 bytes) - Volatile
      │   ├── ROM (256 bytes) - Non-volatile
      │   ├── EEPROM (128 bytes) - Electrically Erasable
      │   └── CMOS (128 bytes) - Battery-backed settings
      ├── Storage Subsystem
      │   ├── Flash Memory (64KB) - Mass storage
      │   └── BIOS Firmware - Boot code
      ├── I/O Devices
      │   ├── Keyboard Input
      │   ├── Display Output (40x25 text)
      │   ├── Serial Port (UART)
      │   └── GPU (Graphics Processing)
      └── System Bus
          ├── Address Bus (8-bit, 256 locations)
          ├── Data Bus (8-bit)
          └── Control Signals (RD, WR, MREQ, IORQ, CS)
"""
    
    @staticmethod
    def signal_flow_diagram() -> str:
        """Data and signal flow"""
        return """
    Signal and Data Flow Diagram
    ==============================
    
    ┌──────────────────────────────────────────────────────────┐
    │                    FETCH CYCLE                           │
    └──────────────────────────────────────────────────────────┘
    
    1. PC → Address Bus
    ╔═══════════════════════════════════════════════════════════╗
    ║   ┌────────┐                                              ║
    ║   │   PC   │ ─────► MAR ─────► Address Bus ─────► Memory ║
    ║   └────────┘                                              ║
    ╚═══════════════════════════════════════════════════════════╝
    
    2. Memory → Data Bus → IR
    ╔═══════════════════════════════════════════════════════════╗
    ║   Memory ─────► Data Bus ─────► MDR ─────► IR            ║
    ╚═══════════════════════════════════════════════════════════╝
    
    3. IR → Instruction Decoder → Control Unit
    ╔═══════════════════════════════════════════════════════════╗
    ║   IR ─────► Decoder ─────► Control Unit ─────► Execute   ║
    ╚═══════════════════════════════════════════════════════════╝
    
    4. PC Increment
    ╔═══════════════════════════════════════════════════════════╗
    ║   PC ─────► ALU (+1) ─────► PC (updated)                 ║
    ╚═══════════════════════════════════════════════════════════╝
    
    ┌──────────────────────────────────────────────────────────┐
    │                   EXECUTE CYCLE                          │
    └──────────────────────────────────────────────────────────┘
    
    Example: ADD A, B
    
    1. Read operands
       ┌───────────┐
       │ Reg A     │ ───┐
       └───────────┘    │
                        ▼
       ┌───────────┐   ┌─────┐
       │ Reg B     │──►│ ALU │
       └───────────┘   └──┬──┘
                          │
    2. ALU Operation      │
       A + B = Result ←───┘
                          │
    3. Write back         ▼
                    ┌───────────┐
                    │  Reg A    │ (Result stored)
                    └───────────┘
    
    ┌──────────────────────────────────────────────────────────┐
    │                   INTERRUPT FLOW                         │
    └──────────────────────────────────────────────────────────┘
    
    External Event
         │
         ▼
    ┌────────────┐
    │ INT Signal │
    └─────┬──────┘
          │
          ▼
    ┌──────────────┐     Yes    ┌──────────────────┐
    │ INT Enabled? │────────────►│ Save PC to Stack │
    └──────┬───────┘            └────────┬─────────┘
           │ No                          │
           │                             ▼
           │                   ┌──────────────────┐
           │                   │ Load ISR Address │
           │                   └────────┬─────────┘
           │                            │
           │                            ▼
           │                   ┌──────────────────┐
           │                   │ Execute ISR      │
           │                   └────────┬─────────┘
           │                            │
           │                            ▼
           │                   ┌──────────────────┐
           │                   │ Restore PC       │
           │                   └────────┬─────────┘
           │                            │
           └────────────────────────────┴────► Continue
"""

# ============================================================================
# INTERACTIVE CIRCUIT BUILDER
# ============================================================================

class InteractiveCircuit:
    """Interactive circuit building system"""
    
    def __init__(self):
        self.canvas_width = 80
        self.canvas_height = 40
        self.canvas = [[' ' for _ in range(self.canvas_width)] 
                       for _ in range(self.canvas_height)]
        self.components: List[Dict] = []
    
    def clear_canvas(self):
        """Clear drawing canvas"""
        self.canvas = [[' ' for _ in range(self.canvas_width)] 
                       for _ in range(self.canvas_height)]
    
    def draw_wire(self, x1: int, y1: int, x2: int, y2: int):
        """Draw wire between two points"""
        if y1 == y2:  # Horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= x < self.canvas_width and 0 <= y1 < self.canvas_height:
                    self.canvas[y1][x] = '─'
        elif x1 == x2:  # Vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 <= x1 < self.canvas_width and 0 <= y < self.canvas_height:
                    self.canvas[y][x1] = '│'
    
    def place_component(self, comp_type: str, x: int, y: int):
        """Place component on canvas"""
        symbols = {
            'AND': '&',
            'OR': '≥1',
            'NOT': '¬',
            'NAND': '⊼',
            'NOR': '⊽',
            'XOR': '⊕',
            'RES': 'R',
            'LED': '◉'
        }
        
        symbol = symbols.get(comp_type, '?')
        if 0 <= x < self.canvas_width and 0 <= y < self.canvas_height:
            self.canvas[y][x] = symbol
            self.components.append({'type': comp_type, 'x': x, 'y': y})
    
    def render(self) -> str:
        """Render canvas to string"""
        border = '┌' + '─' * self.canvas_width + '┐\n'
        canvas_str = border
        for row in self.canvas:
            canvas_str += '│' + ''.join(row) + '│\n'
        canvas_str += '└' + '─' * self.canvas_width + '┘'
        return canvas_str
    
    def create_sample_circuit(self):
        """Create sample AND gate circuit"""
        self.clear_canvas()
        
        # Input A
        self.draw_wire(5, 10, 15, 10)
        self.place_component('AND', 20, 11)
        
        # Input B
        self.draw_wire(5, 12, 15, 12)
        
        # Connection to AND gate
        self.draw_wire(15, 10, 18, 11)
        self.draw_wire(15, 12, 18, 11)
        
        # Output
        self.draw_wire(22, 11, 35, 11)
        self.place_component('LED', 36, 11)
        
        # Labels
        for i, char in enumerate("A"):
            if 3 < self.canvas_width:
                self.canvas[10][3] = char
        for i, char in enumerate("B"):
            if 3 < self.canvas_width:
                self.canvas[12][3] = char

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_blueprints():
    """Demonstrate blueprint system"""
    
    print("=" * 80)
    print("FULL ADDER CIRCUIT SCHEMATIC")
    print("=" * 80)
    print(CircuitDrawer.draw_full_adder_circuit())
    input("\nPress Enter to continue...")
    
    print("\n" * 3)
    print("=" * 80)
    print("8-BIT ALU CIRCUIT")
    print("=" * 80)
    print(CircuitDrawer.draw_8bit_alu_circuit())
    input("\nPress Enter to continue...")
    
    print("\n" * 3)
    print("=" * 80)
    print("MEMORY CIRCUITS")
    print("=" * 80)
    print(CircuitDrawer.draw_memory_circuit())
    input("\nPress Enter to continue...")
    
    print("\n" * 3)
    print("=" * 80)
    print("CPU-MEMORY INTERCONNECTION")
    print("=" * 80)
    print(SystemMap.cpu_memory_interconnect())
    input("\nPress Enter to continue...")
    
    print("\n" * 3)
    print("=" * 80)
    print("COMPLETE SYSTEM MAP")
    print("=" * 80)
    print(SystemMap.complete_system_map())
    input("\nPress Enter to continue...")
    
    print("\n" * 3)
    print("=" * 80)
    print("SIGNAL FLOW DIAGRAM")
    print("=" * 80)
    print(SystemMap.signal_flow_diagram())
    input("\nPress Enter to continue...")
    
    print("\n" * 3)
    print("=" * 80)
    print("INTERACTIVE CIRCUIT BUILDER - Sample Circuit")
    print("=" * 80)
    circuit = InteractiveCircuit()
    circuit.create_sample_circuit()
    print(circuit.render())
    print("\nSample AND gate circuit with LED output")

if __name__ == "__main__":
    demonstrate_blueprints()
