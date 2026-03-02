"""
GAMES SYSTEM - UNIFIED GAMING PLATFORM
=======================================
Unified interface for Game Boy and NES emulation with all system tools
"""

from typing import Optional, List, Dict
from game_boy_emulator import GameBoyEmulator, GameBoyCartridge, demonstrate_gameboy_emulator
from nes_emulator import NESEmulator, NESCartridge, demonstrate_nes_emulator
from rom_manager import ROMTester, ROMLoader, ROMDetector, ROMLibrary
from configuration_system import ConfigurationManager
from tools_system import Debugger, Profiler, MemoryAnalyzer, PerformanceMonitor, SystemDiagnostics
import time

# ============================================================================
# GAMES SYSTEM
# ============================================================================

class GamesSystem:
    """Unified gaming platform with all system tools"""
    
    def __init__(self):
        self.config = ConfigurationManager()
        self.debugger = Debugger()
        self.profiler = Profiler()
        self.memory_analyzer = MemoryAnalyzer()
        self.performance_monitor = PerformanceMonitor()
        self.rom_tester = ROMTester()
        self.rom_library = ROMLibrary()
        
        self.current_emulator = None
        self.current_system = None
        self.is_running = False
        
    def launch_gameboy(self, cartridge: Optional[GameBoyCartridge] = None):
        """Launch Game Boy emulator"""
        print("\n🎮 Launching Game Boy...")
        
        if cartridge is None:
            cartridge = GameBoyCartridge()
        
        self.current_emulator = GameBoyEmulator(cartridge)
        self.current_system = 'Game Boy'
        self.current_emulator.initialize()
        
        print(f"✅ Game Boy launched: {cartridge.title}")
        return self.current_emulator
    
    def launch_nes(self, cartridge: Optional[NESCartridge] = None):
        """Launch NES emulator"""
        print("\n🎮 Launching NES...")
        
        if cartridge is None:
            cartridge = NESCartridge()
        
        self.current_emulator = NESEmulator(cartridge)
        self.current_system = 'NES'
        self.current_emulator.load_cartridge(cartridge)
        self.current_emulator.initialize()
        
        print(f"✅ NES launched: {cartridge.title}")
        return self.current_emulator
    
    def run_game(self, frames: int = 1):
        """Run currently loaded game for specified frames"""
        if self.current_emulator is None:
            print("❌ No emulator loaded")
            return False
        
        self.is_running = True
        self.current_emulator.running = True
        
        print(f"🎮 Running {self.current_system}...")
        
        for frame in range(frames):
            self.current_emulator.run_frame()
        
        self.is_running = False
        self.current_emulator.running = False
        
        print(f"✅ Ran {frames} frames")
        return True
    
    def profile_game(self, frames: int = 1):
        """Profile game execution"""
        if self.current_emulator is None:
            print("❌ No emulator loaded")
            return
        
        print(f"\n📊 Profiling {self.current_system}...")
        
        self.profiler.start_profile(f"{self.current_system}_game")
        self.run_game(frames)
        self.profiler.end_profile(f"{self.current_system}_game")
        
        self.profiler.display_report()
    
    def debug_game(self, breakpoint_addr: int = 0x0100):
        """Debug game with breakpoints"""
        if self.current_emulator is None:
            print("❌ No emulator loaded")
            return
        
        print(f"\n🔍 Debugging {self.current_system}...")
        print(f"Setting breakpoint at 0x{breakpoint_addr:04X}")
        
        self.debugger.set_breakpoint(breakpoint_addr, condition=None)
        self.debugger.add_watch_expression("PC", "program_counter")
        
        # Run for a few steps
        self.current_emulator.running = True
        for i in range(10):
            self.current_emulator.step()
            if self.debugger.check_breakpoint(self.current_emulator.cpu.registers.PC):
                print(f"⚠️  Breakpoint hit at 0x{self.current_emulator.cpu.registers.PC:04X}")
                break
        self.current_emulator.running = False
        
        self.debugger.display_status()
    
    def analyze_memory(self):
        """Analyze game memory"""
        if self.current_emulator is None:
            print("❌ No emulator loaded")
            return
        
        print(f"\n💾 Analyzing {self.current_system} memory...")
        
        # Mark memory regions
        if self.current_system == 'Game Boy':
            self.memory_analyzer.mark_region(0x0000, 0x3FFF, "Game Boy ROM")
            self.memory_analyzer.mark_region(0x4000, 0x7FFF, "Switchable ROM Bank")
            self.memory_analyzer.mark_region(0x8000, 0x9FFF, "Video RAM")
            self.memory_analyzer.mark_region(0xC000, 0xDFFF, "Internal RAM")
        else:  # NES
            self.memory_analyzer.mark_region(0x0000, 0x07FF, "NES RAM")
            self.memory_analyzer.mark_region(0x2000, 0x3FFF, "PPU Registers")
            self.memory_analyzer.mark_region(0x4000, 0x4017, "APU Registers")
            self.memory_analyzer.mark_region(0x8000, 0xFFFF, "PRG-ROM")
        
        self.memory_analyzer.display_memory_map()
    
    def monitor_performance(self, frames: int = 1):
        """Monitor game performance"""
        if self.current_emulator is None:
            print("❌ No emulator loaded")
            return
        
        print(f"\n📈 Monitoring {self.current_system} performance...")
        
        self.performance_monitor.start_monitoring()
        self.run_game(frames)
        self.performance_monitor.generate_report()
    
    def run_diagnostics(self):
        """Run full system diagnostics"""
        print(f"\n🔧 Running diagnostics for {self.current_system}...")
        
        diagnostics = SystemDiagnostics()
        diagnostics.run_diagnostics()
    
    def test_rom(self, rom_path: str):
        """Test ROM file"""
        print(f"\n🧪 Testing ROM: {rom_path}")
        
        system = ROMDetector.detect_system(rom_path)
        if system is None:
            print("❌ Could not detect ROM system")
            return
        
        result = self.rom_tester.test_rom(rom_path)
        if result:
            self.rom_tester.display_test_result(result)
    
    def display_status(self):
        """Display current system status"""
        print("\n" + "=" * 70)
        print("GAMES SYSTEM STATUS")
        print("=" * 70)
        
        if self.current_emulator is None:
            print("❌ No emulator currently loaded")
            return
        
        print(f"\n🎮 Current System: {self.current_system}")
        print(f"🏃 Running: {'Yes' if self.is_running else 'No'}")
        
        if self.current_system == 'Game Boy':
            emulator = self.current_emulator
            print(f"📦 Cartridge: {emulator.cartridge.title}")
            print(f"  PC: 0x{emulator.cpu.registers.PC:04X}")
            print(f"  A: 0x{emulator.cpu.registers.A:02X}")
            print(f"  Cycles: {emulator.cpu.clock_cycles}")
            print(f"  Frames: {emulator.frame_count}")
        else:  # NES
            emulator = self.current_emulator
            print(f"📦 Cartridge: {emulator.cartridge.title}")
            print(f"  Mapper: {emulator.cartridge.get_mapper_name()}")
            print(f"  PC: 0x{emulator.cpu.registers.PC:04X}")
            print(f"  SP: 0x{emulator.cpu.registers.SP:02X}")
            print(f"  Instructions: {emulator.cpu.instructions_executed}")
            print(f"  Frames: {emulator.frame_count}")
        
        print(f"\n🔍 Tools Active:")
        print(f"  • Debugger: Breakpoints configured")
        print(f"  • Profiler: Ready")
        print(f"  • Memory Analyzer: Ready")
        print(f"  • Performance Monitor: Ready")
    
    def display_menu(self):
        """Display games system menu"""
        menu = """
╔════════════════════════════════════════════════════════════════════════════╗
║                         GAMES SYSTEM MENU                                  ║
╠════════════════════════════════════════════════════════════════════════════╣

  EMULATORS                               GAMING
  ═════════                               ══════
  1.  Launch Game Boy Emulator            9.  Run Current Game
  2.  Launch NES Emulator                 10. Profile Game
  3.  Load Custom Cartridge               11. Debug Game
  
  TOOLS & UTILITIES                      ANALYSIS & TESTING
  ═════════════════════                  ══════════════════
  4.  Run Debugger                        12. Analyze Memory
  5.  Run Profiler                        13. Monitor Performance
  6.  Memory Analyzer                     14. Run Diagnostics
  7.  Performance Monitor                 15. Test ROM File
  8.  System Diagnostics                  
  
╚════════════════════════════════════════════════════════════════════════════╝
"""
        print(menu)

# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demonstrate_games_system():
    """Demonstrate integrated games system"""
    print("\n" + "=" * 70)
    print("INTEGRATED GAMES SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    games = GamesSystem()
    
    # Launch Game Boy
    print("\n1️⃣  Launching Game Boy...")
    gb_game = games.launch_gameboy()
    games.run_game(frames=1)
    games.display_status()
    
    # Launch NES
    print("\n2️⃣  Launching NES...")
    nes_game = games.launch_nes()
    games.run_game(frames=1)
    games.display_status()
    
    # Profile Game Boy
    print("\n3️⃣  Profiling Game Boy...")
    games.launch_gameboy()
    games.profile_game(frames=1)
    
    # Debug NES
    print("\n4️⃣  Debugging NES...")
    games.launch_nes()
    games.debug_game()
    
    # Analyze memory
    print("\n5️⃣  Analyzing Game Boy memory...")
    games.launch_gameboy()
    games.analyze_memory()
    
    print("\n✅ Games System demonstration complete!")

def run_interactive_games_menu():
    """Run interactive games system menu"""
    games = GamesSystem()
    
    while True:
        print("\n" + "=" * 70)
        games.display_menu()
        
        choice = input("\nEnter choice (1-15, 0 to exit): ").strip()
        
        if choice == '0':
            print("Exiting Games System...")
            break
        elif choice == '1':
            games.launch_gameboy()
        elif choice == '2':
            games.launch_nes()
        elif choice == '3':
            rom_path = input("Enter ROM path: ").strip()
            result = ROMLoader.load_rom(rom_path)
            if result:
                system, cartridge = result
                if system == 'Game Boy':
                    games.launch_gameboy(cartridge)
                else:
                    games.launch_nes(cartridge)
            else:
                print("❌ Could not load ROM")
        elif choice == '4':
            if games.current_emulator:
                bp_addr = int(input("Enter breakpoint address (hex): ").strip(), 16)
                games.debug_game(bp_addr)
            else:
                print("❌ No emulator loaded")
        elif choice == '5':
            if games.current_emulator:
                games.profile_game(1)
            else:
                print("❌ No emulator loaded")
        elif choice == '6':
            if games.current_emulator:
                games.analyze_memory()
            else:
                print("❌ No emulator loaded")
        elif choice == '7':
            if games.current_emulator:
                games.monitor_performance(1)
            else:
                print("❌ No emulator loaded")
        elif choice == '8':
            games.run_diagnostics()
        elif choice == '9':
            if games.current_emulator:
                frames = int(input("Number of frames to run: ") or "1")
                games.run_game(frames)
            else:
                print("❌ No emulator loaded")
        elif choice == '10':
            if games.current_emulator:
                frames = int(input("Number of frames to profile: ") or "1")
                games.profile_game(frames)
            else:
                print("❌ No emulator loaded")
        elif choice == '11':
            if games.current_emulator:
                bp_str = input("Breakpoint address (hex, or Enter for default): ").strip()
                bp_addr = int(bp_str, 16) if bp_str else 0x0100
                games.debug_game(bp_addr)
            else:
                print("❌ No emulator loaded")
        elif choice == '12':
            if games.current_emulator:
                games.analyze_memory()
            else:
                print("❌ No emulator loaded")
        elif choice == '13':
            if games.current_emulator:
                games.monitor_performance(1)
            else:
                print("❌ No emulator loaded")
        elif choice == '14':
            games.run_diagnostics()
        elif choice == '15':
            rom_path = input("Enter ROM path to test: ").strip()
            games.test_rom(rom_path)
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    demonstrate_games_system()
