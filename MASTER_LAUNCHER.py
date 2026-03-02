"""
MASTER LAUNCHER - 8-Bit Logic Gates Computer System v2.0
==========================================================
Complete integration of all system components
Advanced multi-architecture support (8/16/32/64-bit)
Configuration, input, boot sequences, and tools
"""

import os
import sys
import time
from typing import Optional

# ============================================================================
# SYSTEM INTEGRATION
# ============================================================================

class MasterSystem:
    """Master system integration"""
    
    def __init__(self):
        self.system_name = "8-Bit Logic Gates Computer System"
        self.version = "2.2.0"
        self.modules_loaded = []
        self.config = None
        self.input_manager = None
    
    def clear_screen(self):
        """Clear terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        """Display system banner"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║           ⚡ 8-BIT LOGIC GATES COMPUTER SYSTEM ⚡                    ║
║                                                                       ║
║              Complete Computer Architecture Simulation                ║
║                        Version {self.version}                              ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

        """
        print(banner)
    
    def display_main_menu(self):
        """Display main menu"""
        menu = """
╔════════════════════════════════════════════════════════════════════════════╗
║                 8-BIT LOGIC GATES COMPUTER SYSTEM v2.2.0                   ║
║                      MAIN SYSTEM MENU (Extended Edition)                   ║
╠════════════════════════════════════════════════════════════════════════════╣

  MULTI-ARCHITECTURE SYSTEMS           CORE COMPONENTS
  ════════════════════════             ════════════════
  1.  Run 8-bit System                  6.  Logic Gates Demo
  2.  Run 16-bit System                 7.  Assembly Program
  3.  Run 32-bit System                 8.  Database Operations
  4.  Run 64-bit System                 9.  Advanced Calculator
  5.  Multi-System Comparison           10. Character Operations

  CONFIGURATION & SETTINGS              CODE GENERATION
  ════════════════════════             ══════════════════
  11. System Settings                   16. Generate C Code
  12. Display Options                   17. Generate C++17 Code
  13. Audio Settings                    18. Generate 8-bit ASM
  14. Input Configuration               19. Code Generator Manager
  15. Performance Settings              20. Compiler Options

  TOOLS & UTILITIES                     BOOT & INITIALIZATION
  ═════════════════════                ════════════════════
  21. Debugger                          31. Show Splash Screen
  22. Profiler                          32. Show Boot Screen
  23. Memory Analyzer                   33. Show Loading Screens
  24. Performance Monitor               34. Run Full Initialization
  25. System Diagnostics                35. Configure Boot Sequence

  INPUT TESTING                         VISUALIZATION & INTERFACES
  ════════════════                      ═══════════════════════════
  26. Keyboard Input Tester             36. Transistor Diagrams
  27. Mouse Input Tester                37. Flash Memory Tables
  28. Gamepad Input Tester              38. System Blueprints
  29. Input System Demo                 39. Circuit Builder
  30. Input Configuration               40. API Server

  DOCUMENTATION & HELP                  ADVANCED OPTIONS
  ════════════════════════             ═════════════════
  41. Complete Documentation            46. Export Configuration
  42. Quick Start Guide                 47. Import Configuration
  43. System Information                48. Reset to Defaults
  44. Configuration Info                49. About System
  45. Help & Support                    50. Exit Program

  GAMING SYSTEMS                        GAMING TOOLS & TESTS
  ══════════════════                    ════════════════════
  51. Game Boy Emulator                 56. Profile Game Performance
  52. NES Emulator                      57. Debug Game Execution
  53. Load & Play Custom ROM            58. Analyze Game Memory
  54. ROM Tester                        59. ROM Library Manager
  55. Integrated Games Menu             60. Test ROM Compatibility

  DEVELOPMENT SDK TOOLS                 PLUGIN SYSTEM TOOLS
  ═══════════════════════               ═══════════════════
  61. Create New Project                66. Load Plugin System
  62. Open Project                      67. List Available Plugins
  63. Save Project                      68. Enable Plugin
  64. Build Project                     69. Disable Plugin
  65. Project Settings                  70. Configure Plugins

  IDE DEVELOPMENT TOOLS                 RPG MAKER MZ TOOLS
  ══════════════════════                ══════════════════
  71. Integrated Editor UI              76. RPG Maker API
  72. Assembly (ASM) IDE                77. Create RPG Project
  73. C Language IDE                    78. RPG Game Database
  74. Code Compilation Test             79. Play Test Game
  75. Integrated Development Menu       80. Advanced RPG Tools

╚════════════════════════════════════════════════════════════════════════════╝
"""
        print(menu)
    
    def run_logic_gates(self):
        """Run logic gates demonstration"""
        print("\n🔌 Loading Logic Gates Module...")
        try:
            import logic_gates
            print("✅ Module loaded successfully!\n")
            
            # Quick demo
            print("=" * 70)
            print("LOGIC GATES QUICK DEMONSTRATION")
            print("=" * 70)
            
            print("\nBasic Gates:")
            print(f"AND(1, 1) = {logic_gates.AND(1, 1)}")
            print(f"OR(1, 0) = {logic_gates.OR(1, 0)}")
            print(f"XOR(1, 1) = {logic_gates.XOR(1, 1)}")
            print(f"NOT(1) = {logic_gates.NOT(1)}")
            
            print("\nCompound Gates:")
            sum_bit, carry = logic_gates.CompoundGates.HALF_ADDER(1, 1)
            print(f"HALF_ADDER(1, 1) = Sum:{sum_bit}, Carry:{carry}")
            
            a = [0, 0, 0, 0, 0, 1, 0, 1]  # 5
            b = [0, 0, 0, 0, 0, 0, 1, 1]  # 3
            result = logic_gates.BinaryOperations.add_8bit(a, b)
            print(f"8-bit ADD: 5 + 3 = {logic_gates.BinaryOperations.bit_to_int(result)}")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            print("Make sure logic_gates.py is in the same directory.")
            input("\nPress Enter to continue...")
    
    def run_computer(self):
        """Run 8-bit computer"""
        print("\n💾 Loading Computer Components...")
        try:
            import computer_components
            print("✅ Module loaded successfully!\n")
            
            print("=" * 70)
            print("8-BIT COMPUTER DEMONSTRATION")
            print("=" * 70)
            
            # Initialize components
            ram = computer_components.RAM()
            cpu = computer_components.CPU(ram)
            bios = computer_components.BIOS(ram, cpu)
            
            print("\n📋 Running BIOS POST...")
            bios.power_on_self_test()
            
            print(f"\n📊 CPU Status:")
            print(f"Register A: {cpu.registers.A:08b} ({cpu.registers.A})")
            print(f"Register B: {cpu.registers.B:08b} ({cpu.registers.B})")
            print(f"Program Counter: {cpu.registers.PC:08b} ({cpu.registers.PC})")
            print(f"Stack Pointer: {cpu.registers.SP:08b} ({cpu.registers.SP})")
            
            # Simple program: Add 5 + 3
            print("\n📝 Executing simple program: 5 + 3")
            ram.write(0x10, 0x01)  # MOV A, 5
            ram.write(0x11, 5)
            ram.write(0x12, 0x01)  # MOV B, 3
            ram.write(0x13, 3)
            ram.write(0x14, 0x02)  # ADD A, B
            
            cpu.registers.PC = 0x10
            for _ in range(5):
                cpu.step()
            
            print(f"Result in Register A: {cpu.registers.A}")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_assembly(self):
        """Run assembly language"""
        print("\n📝 Loading Assembly Language Module...")
        try:
            import assembly_language
            print("✅ Module loaded successfully!\n")
            
            print("=" * 70)
            print("ASSEMBLY LANGUAGE DEMONSTRATION")
            print("=" * 70)
            
            assembler = assembly_language.Assembler()
            
            # Show sample programs
            print("\n📚 Available Sample Programs:")
            programs = assembly_language.SamplePrograms.get_all_programs()
            for i, (name, _) in enumerate(programs.items(), 1):
                print(f"{i}. {name}")
            
            print("\n📄 Example: Hello World Program")
            hello_program = assembly_language.SamplePrograms.hello_world()
            print(hello_program)
            
            print("\n🔧 Assembling code...")
            machine_code = assembler.assemble(hello_program)
            print(f"Generated {len(machine_code)} bytes of machine code")
            print(f"Machine code (hex): {' '.join(f'{b:02X}' for b in machine_code[:16])}...")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_calculators(self):
        """Run calculators"""
        print("\n🔢 Loading Calculator Module...")
        try:
            import math_calculator
            print("✅ Module loaded successfully!\n")
            
            print("=" * 70)
            print("CALCULATOR DEMONSTRATIONS")
            print("=" * 70)
            
            # Scientific calculator
            print("\n🔬 Scientific Calculator:")
            calc = math_calculator.ScientificCalculator()
            print(f"2^8 = {calc.power(2, 8)}")
            print(f"√16 = {calc.square_root(16)}")
            print(f"5! = {calc.factorial(5)}")
            
            # Programmer calculator
            print("\n💻 Programmer Calculator:")
            prog = math_calculator.ProgrammerCalculator()
            bits = [0, 0, 0, 0, 1, 0, 1, 0]  # 10
            result = prog.shift_left(bits, 1)  # Should be 20
            print(f"10 << 1 = {math_calculator.BinaryOperations.binary_to_decimal(result)}")
            print(f"Bit count of 0b10101010: {prog.count_bits([1,0,1,0,1,0,1,0])}")
            
            # Statistical calculator
            print("\n📊 Statistical Calculator:")
            stats = math_calculator.StatisticalCalculator()
            data = [10, 20, 30, 40, 50]
            print(f"Mean of {data}: {stats.mean(data)}")
            print(f"Median of {data}: {stats.median(data)}")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_character_ops(self):
        """Run character operations"""
        print("\n🔤 Loading Character Logic Operations...")
        try:
            import character_logic_gates
            print("✅ Module loaded successfully!\n")
            
            print("=" * 70)
            print("CHARACTER LOGIC OPERATIONS")
            print("=" * 70)
            
            char_ops = character_logic_gates.CharacterLogicOperations()
            
            print("\n📝 Character Mappings:")
            print(f"'A' → {char_ops.char_to_binary('A')} (binary)")
            print(f"'Z' → {char_ops.char_to_binary('Z')} (binary)")
            print(f"'0' → {char_ops.char_to_binary('0')} (binary)")
            print(f"'9' → {char_ops.char_to_binary('9')} (binary)")
            
            print("\n⚡ Logic Operations on Characters:")
            print(f"'A' AND 'B' = '{char_ops.and_operation('A', 'B')}'")
            print(f"'1' XOR '0' = '{char_ops.xor_operation('1', '0')}'")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def generate_c_code(self):
        """Generate C code"""
        print("\n🔧 Loading Code Generator...")
        try:
            import code_generator
            print("✅ Module loaded successfully!\n")
            
            manager = code_generator.CodeGeneratorManager()
            header, impl = manager.generate_c_code()
            
            # Save files
            with open('logic_gates.h', 'w') as f:
                f.write(header)
            with open('logic_gates.c', 'w') as f:
                f.write(impl)
            
            print("✅ Generated C code files:")
            print("   - logic_gates.h")
            print("   - logic_gates.c")
            print(f"\nHeader file size: {len(header)} bytes")
            print(f"Implementation file size: {len(impl)} bytes")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def generate_cpp_code(self):
        """Generate C++17 code"""
        print("\n🔧 Loading Code Generator...")
        try:
            import code_generator
            print("✅ Module loaded successfully!\n")
            
            manager = code_generator.CodeGeneratorManager()
            header, impl = manager.generate_cpp17_code()
            
            # Save files
            with open('logic_gates.hpp', 'w') as f:
                f.write(header)
            with open('logic_gates_cpp17.cpp', 'w') as f:
                f.write(impl)
            
            print("✅ Generated C++17 code files:")
            print("   - logic_gates.hpp")
            print("   - logic_gates_cpp17.cpp")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def generate_asm_code(self):
        """Generate assembly code"""
        print("\n🔧 Loading Code Generator...")
        try:
            import code_generator
            print("✅ Module loaded successfully!\n")
            
            manager = code_generator.CodeGeneratorManager()
            asm_code = manager.generate_asm8bit_code()
            
            # Save file
            with open('logic_gates.asm', 'w') as f:
                f.write(asm_code)
            
            print("✅ Generated 8-bit Assembly file:")
            print("   - logic_gates.asm")
            print(f"\nFile size: {len(asm_code)} bytes")
            
            input("\nPress Enter to return to main menu...")
            
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_gui(self):
        """Run GUI system"""
        print("\n🖥️  Loading GUI/UI System...")
        try:
            import gui_ui_system
            print("✅ Module loaded successfully!\n")
            gui_ui_system.demonstrate_ui()
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def open_web_interface(self):
        """Open web interface"""
        print("\n🌐 Opening Web Interface...")
        import webbrowser
        try:
            webbrowser.open('web_interface.html')
            print("✅ Web interface opened in browser!")
            input("\nPress Enter to return to main menu...")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please open 'web_interface.html' manually in your browser.")
            input("\nPress Enter to continue...")
    
    def run_api_server(self):
        """Run API server"""
        print("\n🔌 Loading API Server...")
        try:
            import api_server
            print("✅ Module loaded successfully!\n")
            print("Running API demonstration...")
            api_server.demonstrate_api()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def show_transistors(self):
        """Show transistor diagrams"""
        print("\n⚙️  Loading Transistor Diagrams...")
        try:
            import gui_ui_system
            ui = gui_ui_system.LogicGatesUI()
            ui.show_transistor_diagrams()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def show_flash_tables(self):
        """Show flash tables"""
        print("\n💾 Loading Flash Memory Tables...")
        try:
            import gui_ui_system
            ui = gui_ui_system.LogicGatesUI()
            ui.show_flash_tables()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def show_blueprints(self):
        """Show system blueprints"""
        print("\n📐 Loading Interactive Blueprints...")
        try:
            import interactive_blueprints
            print("✅ Module loaded successfully!\n")
            interactive_blueprints.demonstrate_blueprints()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def show_circuit_builder(self):
        """Show interactive circuit builder"""
        print("\n🔧 Loading Circuit Builder...")
        try:
            import interactive_blueprints
            circuit = interactive_blueprints.InteractiveCircuit()
            circuit.create_sample_circuit()
            self.clear_screen()
            print("=" * 70)
            print("INTERACTIVE CIRCUIT BUILDER - Sample Circuit")
            print("=" * 70)
            print(circuit.render())
            print("\nSample AND gate circuit with LED output")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def show_documentation(self):
        """Show complete documentation"""
        print("\n📚 Opening Complete Documentation...")
        try:
            with open('COMPLETE_DOCUMENTATION.md', 'r') as f:
                content = f.read()
            
            # Show first 50 lines
            lines = content.split('\n')
            for line in lines[:50]:
                print(line)
            
            print("\n... (truncated, see COMPLETE_DOCUMENTATION.md for full content)")
            input("\nPress Enter to return to main menu...")
        except FileNotFoundError:
            print("❌ Documentation file not found.")
            input("\nPress Enter to continue...")
    
    def show_quickstart(self):
        """Show quick start guide"""
        print("\n🚀 Loading Quick Start Guide...")
        try:
            import QUICKSTART
            input("\nPress Enter to return to main menu...")
        except ImportError:
            print("❌ Quick start file not found.")
            input("\nPress Enter to continue...")
    
    def show_status(self):
        """Show system status"""
        self.clear_screen()
        print("=" * 70)
        print("SYSTEM STATUS & INFORMATION")
        print("=" * 70)
        
        print(f"\n📦 System Name: {self.system_name}")
        print(f"📌 Version: {self.version}")
        print(f"🐍 Python Version: {sys.version.split()[0]}")
        
        print("\n✅ Available Modules:")
        modules = [
            'logic_gates.py',
            'computer_components.py',
            'assembly_language.py',
            'database_manager.py',
            'character_logic_gates.py',
            'math_calculator.py',
            'code_generator.py',
            'api_server.py',
            'gui_ui_system.py',
            'interactive_blueprints.py',
            'multi_bit_systems.py',
            'configuration_system.py',
            'input_control_system.py',
            'boot_splash_system.py',
            'tools_system.py',
            'game_boy_emulator.py',
            'nes_emulator.py',
            'rom_manager.py',
            'games_system.py',
            'web_interface.html',
            'COMPLETE_DOCUMENTATION.md'
        ]
        
        for module in modules:
            exists = os.path.exists(module)
            status = "✅" if exists else "❌"
            print(f"{status} {module}")
        
        print("\n📊 System Capabilities:")
        print("  • Logic Gates: 8 types (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUFFER)")
        print("  • Multi-Architecture: 8, 16, 32, 64-bit systems with full instruction sets")
        print("  • Computer: 8-bit CPU with 256B RAM, 256B ROM")
        print("  • Assembly: 20+ instructions with assembler")
        print("  • Calculators: 5 types (Basic, Scientific, Programmer, Algebraic, Statistical)")
        print("  • Code Generation: C, C++17, 8-bit Assembly")
        print("  • Configuration: JSON-based settings with 7+ categories")
        print("  • Input: Keyboard, Mouse, Gamepad support with callbacks")
        print("  • Boot System: Splash, Boot, Loading screens with animations")
        print("  • Tools: Debugger, Profiler, Memory Analyzer, Performance Monitor, Diagnostics")
        print("  • Gaming: Game Boy & NES emulators with ROM testing & profiling")
        print("  • Interfaces: Text UI, Web UI, REST API")
        print("  • Visualizations: Transistors, circuits, blueprints")
        
        input("\nPress Enter to return to main menu...")
    
    # ===== NEW MULTI-ARCHITECTURE SYSTEMS =====
    
    def run_16bit_system(self):
        """Run 16-bit computer system"""
        print("\n🖥️  Loading 16-bit System...")
        try:
            from multi_bit_systems import System16Bit
            print("✅ 16-bit System loaded successfully!\n")
            
            system = System16Bit()
            print("=" * 70)
            print("16-BIT COMPUTER SYSTEM DEMONSTRATION")
            print("=" * 70)
            
            print("\n📋 System Specifications:")
            print(f"  Architecture: 16-bit")
            print(f"  Address Space: 64 KB")
            print(f"  Registers: 8")
            print(f"  Cache: 512 B L1")
            
            print("\n🧮 Test: ADD Operation (0x1000 + 0x2000)")
            result = system.execute_instruction(0x02, [0x1000, 0x2000])
            print(f"  Result: {hex(result)}")
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_32bit_system(self):
        """Run 32-bit computer system"""
        print("\n🖥️  Loading 32-bit System...")
        try:
            from multi_bit_systems import System32Bit
            print("✅ 32-bit System loaded successfully!\n")
            
            system = System32Bit()
            print("=" * 70)
            print("32-BIT COMPUTER SYSTEM DEMONSTRATION")
            print("=" * 70)
            
            print("\n📋 System Specifications:")
            print(f"  Architecture: 32-bit")
            print(f"  Address Space: 4 GB (simulated to 1 MB)")
            print(f"  Registers: 10")
            print(f"  Cache: 8 KB L1 + 256 KB L2")
            
            print("\n🧮 Test: ADD Operation (0x100000 + 0x200000)")
            result = system.execute_instruction(0x02, [0x100000, 0x200000])
            print(f"  Result: {hex(result)}")
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_64bit_system(self):
        """Run 64-bit computer system"""
        print("\n🖥️  Loading 64-bit System...")
        try:
            from multi_bit_systems import System64Bit
            print("✅ 64-bit System loaded successfully!\n")
            
            system = System64Bit()
            print("=" * 70)
            print("64-BIT COMPUTER SYSTEM DEMONSTRATION")
            print("=" * 70)
            
            print("\n📋 System Specifications:")
            print(f"  Architecture: 64-bit")
            print(f"  Address Space: 16 EB (simulated to 2 MB)")
            print(f"  Registers: 18")
            print(f"  Cache: 32 KB L1 + 256 KB L2 + 8 MB L3")
            
            print("\n🧮 Test: ADD Operation (0x1000000000 + 0x2000000000)")
            result = system.execute_instruction(0x02, [0x1000000000, 0x2000000000])
            print(f"  Result: {hex(result)}")
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def compare_architectures(self):
        """Compare all architectures"""
        print("\n📊 Loading Architecture Comparison...")
        try:
            from multi_bit_systems import MultiSystemManager
            print("✅ Multi-System Manager loaded!\n")
            
            manager = MultiSystemManager()
            manager.display_comparison_table()
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    # ===== CONFIGURATION SYSTEM =====
    
    def run_configuration(self):
        """Run configuration manager"""
        print("\n⚙️  Loading Configuration System...")
        try:
            from configuration_system import ConfigurationManager
            print("✅ Configuration System loaded!\n")
            
            config = ConfigurationManager()
            config.display_settings()
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_display_settings(self):
        """Run display settings"""
        print("\n🎨 Display Settings")
        try:
            from configuration_system import ConfigurationManager
            config = ConfigurationManager()
            config.display_settings()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_audio_settings(self):
        """Run audio settings"""
        print("\n🔊 Audio Settings")
        try:
            from configuration_system import ConfigurationManager
            config = ConfigurationManager()
            settings = config.get_setting('audio')
            for key, value in settings.__dict__.items():
                print(f"  {key}: {value}")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_performance_settings(self):
        """Run performance settings"""
        print("\n⚡ Performance Settings")
        try:
            from configuration_system import ConfigurationManager
            config = ConfigurationManager()
            settings = config.get_setting('performance')
            for key, value in settings.__dict__.items():
                print(f"  {key}: {value}")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_input_settings(self):
        """Run input settings"""
        print("\n⌨️  Input Settings")
        try:
            from configuration_system import ConfigurationManager
            config = ConfigurationManager()
            settings = config.get_setting('input')
            for key, value in settings.__dict__.items():
                print(f"  {key}: {value}")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    # ===== BOOT/SPLASH/LOADING SCREENS =====
    
    def show_splash_screen(self):
        """Show splash screen"""
        print("\n🎬 Loading Splash Screen...")
        try:
            from boot_splash_system import SplashScreen
            splash = SplashScreen()
            splash.animated_splash(duration=3.0)
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def show_boot_screen(self):
        """Show boot screen"""
        print("\n⚙️  Loading Boot Screen...")
        try:
            from boot_splash_system import BootScreen
            boot = BootScreen()
            boot.show_boot_sequence(show_animation=True)
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def show_loading_screens(self):
        """Show loading screen examples"""
        print("\n📊 Loading Screen Demonstrations...")
        try:
            from boot_splash_system import LoadingScreen
            loading = LoadingScreen()
            
            print("\n1️⃣  Progress Bar Example:")
            loading.show_progress_bar("Loading System", duration=2)
            
            input("\nPress Enter for next demo...")
            
            print("\n2️⃣  Spinner Example:")
            loading.show_spinner("Initializing", duration=2)
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_full_initialization(self):
        """Run full system initialization"""
        print("\n🚀 Full System Initialization...")
        try:
            from boot_splash_system import SplashScreen, BootScreen, LoadingScreen
            
            splash = SplashScreen()
            boot = BootScreen()
            loading = LoadingScreen()
            
            print("Starting initialization sequence...\n")
            
            splash.animated_splash(duration=2)
            boot.show_boot_sequence(show_animation=False)
            loading.show_progress_bar("Final Initialization", duration=1)
            
            print("\n✅ System initialized successfully!")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def configure_boot_sequence(self):
        """Configure boot sequence settings"""
        print("\n⚙️  Boot Sequence Configuration")
        try:
            from configuration_system import ConfigurationManager
            config = ConfigurationManager()
            settings = config.get_setting('user_preferences')
            print(f"  Show Boot Screens: {settings.show_boot_screens}")
            print(f"  Show Splash: {settings.show_splash_screen}")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    # ===== INPUT SYSTEM =====
    
    def test_keyboard(self):
        """Test keyboard input"""
        print("\n⌨️  Keyboard Input Tester")
        try:
            from input_control_system import InputTester
            tester = InputTester()
            tester.test_keyboard()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def test_mouse(self):
        """Test mouse input"""
        print("\n🖱️  Mouse Input Tester")
        try:
            from input_control_system import InputTester
            tester = InputTester()
            tester.test_mouse()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def test_gamepad(self):
        """Test gamepad input"""
        print("\n🎮 Gamepad Input Tester")
        try:
            from input_control_system import InputTester
            tester = InputTester()
            tester.test_gamepad()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def test_input_demo(self):
        """Run input system demo"""
        print("\n🎯 Input System Demo")
        try:
            from input_control_system import InputManager
            manager = InputManager()
            print("Input system initialized with keyboard mode")
            print("Available modes: 'keyboard', 'mouse', 'gamepad'")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def configure_input(self):
        """Configure input settings"""
        print("\n⚙️  Input Configuration")
        try:
            from configuration_system import ConfigurationManager
            config = ConfigurationManager()
            settings = config.get_setting('input')
            print("  Keyboard Layout: US")
            print(f"  Mouse Sensitivity: {settings.mouse_sensitivity}%")
            print(f"  Gamepad Sensitivity: {settings.gamepad_sensitivity}%")
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    # ===== TOOLS SYSTEM =====
    
    def run_debugger(self):
        """Run debugger"""
        print("\n🔍 Debugger")
        try:
            from tools_system import Debugger
            debugger = Debugger()
            debugger.set_breakpoint(0x1000, enabled=True)
            debugger.add_watch_expression("A", "register_a.value")
            debugger.display_status()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_profiler(self):
        """Run profiler"""
        print("\n⏱️  Profiler")
        try:
            from tools_system import Profiler
            import time
            
            profiler = Profiler()
            
            profiler.start_profile("test_function")
            time.sleep(0.1)
            profiler.end_profile("test_function")
            
            profiler.display_report()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_memory_analyzer(self):
        """Run memory analyzer"""
        print("\n💾 Memory Analyzer")
        try:
            from tools_system import MemoryAnalyzer
            analyzer = MemoryAnalyzer()
            analyzer.mark_region(0x0000, 0x00FF, "BIOS")
            analyzer.mark_region(0x0100, 0x01FF, "System Data")
            analyzer.display_memory_map()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_performance_monitor(self):
        """Run performance monitor"""
        print("\n📊 Performance Monitor")
        try:
            from tools_system import PerformanceMonitor, PerformanceMetrics
            monitor = PerformanceMonitor()
            
            metrics = PerformanceMetrics(
                cpu_usage=45.2, memory_used=256, clock_cycles=1000000,
                instructions_executed=500000, cache_hits=450000, cache_misses=50000
            )
            monitor.record_metrics(metrics)
            monitor.generate_report()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_system_diagnostics(self):
        """Run system diagnostics"""
        print("\n🔧 System Diagnostics")
        try:
            from tools_system import SystemDiagnostics
            diagnostics = SystemDiagnostics()
            diagnostics.run_diagnostics()
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    # ===== GAMING SYSTEMS =====
    
    def run_gameboy_emulator(self):
        """Run Game Boy emulator"""
        print("\n🎮 Game Boy Emulator")
        try:
            from games_system import GamesSystem
            games = GamesSystem()
            emulator = games.launch_gameboy()
            
            games.run_game(frames=3)
            emulator.display_status()
            emulator.graphics.display_screen()
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_nes_emulator(self):
        """Run NES emulator"""
        print("\n🎮 NES Emulator")
        try:
            from games_system import GamesSystem
            games = GamesSystem()
            emulator = games.launch_nes()
            
            games.run_game(frames=3)
            emulator.display_status()
            emulator.ppu.display_screen()
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def load_and_play_rom(self):
        """Load and play custom ROM"""
        print("\n📦 Load & Play Custom ROM")
        try:
            from rom_manager import ROMLoader
            from games_system import GamesSystem
            
            rom_path = input("Enter ROM file path: ").strip()
            
            result = ROMLoader.load_rom(rom_path)
            if result:
                system, cartridge = result
                games = GamesSystem()
                
                if system == 'Game Boy':
                    emulator = games.launch_gameboy(cartridge)
                else:
                    emulator = games.launch_nes(cartridge)
                
                print("\nRunning game...")
                games.run_game(frames=5)
                emulator.display_status()
                
                if system == 'Game Boy':
                    emulator.graphics.display_screen()
                else:
                    emulator.ppu.display_screen()
            else:
                print("❌ Could not load ROM")
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_rom_tester(self):
        """Run ROM tester"""
        print("\n🧪 ROM Tester")
        try:
            from rom_manager import ROMTester
            
            rom_path = input("Enter ROM file path: ").strip()
            
            tester = ROMTester()
            result = tester.test_rom(rom_path)
            
            if result:
                tester.display_test_result(result)
            else:
                print("❌ Could not test ROM")
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run_games_menu(self):
        """Run integrated games menu"""
        print("\n🎮 Integrated Games System")
        try:
            from games_system import run_interactive_games_menu
            run_interactive_games_menu()
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def profile_game_performance(self):
        """Profile game performance"""
        print("\n📊 Profile Game Performance")
        try:
            from games_system import GamesSystem
            from rom_manager import ROMLoader
            
            rom_path = input("Enter ROM file path (or press Enter for test game): ").strip()
            
            games = GamesSystem()
            
            if rom_path:
                result = ROMLoader.load_rom(rom_path)
                if result:
                    system, cartridge = result
                    if system == 'Game Boy':
                        games.launch_gameboy(cartridge)
                    else:
                        games.launch_nes(cartridge)
            else:
                # Use test game
                games.launch_gameboy()
            
            frames = int(input("Frames to profile (default 5): ") or "5")
            games.profile_game(frames)
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def debug_game_execution(self):
        """Debug game execution"""
        print("\n🔍 Debug Game Execution")
        try:
            from games_system import GamesSystem
            
            games = GamesSystem()
            games.launch_gameboy()
            
            bp_input = input("Breakpoint address in hex (default 0x0100): ").strip()
            bp_addr = int(bp_input, 16) if bp_input else 0x0100
            
            games.debug_game(bp_addr)
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def analyze_game_memory(self):
        """Analyze game memory"""
        print("\n💾 Analyze Game Memory")
        try:
            from games_system import GamesSystem
            
            games = GamesSystem()
            games.launch_gameboy()
            games.analyze_memory()
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def manage_rom_library(self):
        """Manage ROM library"""
        print("\n📚 ROM Library Manager")
        try:
            from rom_manager import ROMLibrary
            
            library = ROMLibrary()
            library.display_library()
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def test_rom_compatibility(self):
        """Test ROM compatibility"""
        print("\n🧪 Test ROM Compatibility")
        try:
            from rom_manager import ROMTester
            
            rom_path = input("Enter ROM file path: ").strip()
            
            tester = ROMTester()
            results = tester.test_rom_compatibility(rom_path)
            
            print(f"\nROM: {results['rom_path']}")
            print(f"Detected System: {results['detected_system']}")
            
            tester.display_test_result(results['gameboy_test'])
            tester.display_test_result(results['nes_test'])
            
            input("\nPress Enter to return to main menu...")
        except ImportError as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")
    
    def run(self):
        """Main execution loop"""
        while True:
            self.clear_screen()
            self.display_banner()
            self.display_main_menu()
            
            choice = input("Enter your choice (1-60, 0 to exit): ").strip()
            
            if choice == '0':
                self.clear_screen()
                print("\n" + "=" * 70)
                print("Shutting down 8-Bit Logic Gates Computer System...")
                print("Thank you for using the system!")
                print("=" * 70 + "\n")
                break
            # Multi-Architecture Systems (1-5)
            elif choice == '1':
                self.run_logic_gates()
            elif choice == '2':
                self.run_16bit_system()
            elif choice == '3':
                self.run_32bit_system()
            elif choice == '4':
                self.run_64bit_system()
            elif choice == '5':
                self.compare_architectures()
            # Core Components (6-10)
            elif choice == '6':
                self.run_logic_gates()
            elif choice == '7':
                self.run_assembly()
            elif choice == '8':
                self.run_computer()
            elif choice == '9':
                self.run_calculators()
            elif choice == '10':
                self.run_character_ops()
            # Configuration & Settings (11-15)
            elif choice == '11':
                self.run_configuration()
            elif choice == '12':
                self.run_display_settings()
            elif choice == '13':
                self.run_audio_settings()
            elif choice == '14':
                self.run_input_settings()
            elif choice == '15':
                self.run_performance_settings()
            # Code Generation (16-20)
            elif choice == '16':
                self.generate_c_code()
            elif choice == '17':
                self.generate_cpp_code()
            elif choice == '18':
                self.generate_asm_code()
            elif choice == '19':
                print("\n📋 Code Generator Manager")
                try:
                    import code_generator
                    manager = code_generator.CodeGeneratorManager()
                    print("Generator loaded with support for C, C++17, and 8-bit Assembly")
                    input("\nPress Enter to return to main menu...")
                except ImportError:
                    print("❌ Code generator module not found")
                    input("\nPress Enter to continue...")
            elif choice == '20':
                print("\n⚙️  Compiler Options")
                print("Optimization Level: O2")
                print("Debug Symbols: Enabled")
                print("Warning Level: All")
                input("\nPress Enter to return to main menu...")
            # Tools & Utilities (21-25)
            elif choice == '21':
                self.run_debugger()
            elif choice == '22':
                self.run_profiler()
            elif choice == '23':
                self.run_memory_analyzer()
            elif choice == '24':
                self.run_performance_monitor()
            elif choice == '25':
                self.run_system_diagnostics()
            # Input Testing (26-30)
            elif choice == '26':
                self.test_keyboard()
            elif choice == '27':
                self.test_mouse()
            elif choice == '28':
                self.test_gamepad()
            elif choice == '29':
                self.test_input_demo()
            elif choice == '30':
                self.configure_input()
            # Boot & Initialization (31-35)
            elif choice == '31':
                self.show_splash_screen()
            elif choice == '32':
                self.show_boot_screen()
            elif choice == '33':
                self.show_loading_screens()
            elif choice == '34':
                self.run_full_initialization()
            elif choice == '35':
                self.configure_boot_sequence()
            # Visualization & Interfaces (36-40)
            elif choice == '36':
                self.show_transistors()
            elif choice == '37':
                self.show_flash_tables()
            elif choice == '38':
                self.show_blueprints()
            elif choice == '39':
                self.show_circuit_builder()
            elif choice == '40':
                self.run_api_server()
            # Documentation & Help (41-45)
            elif choice == '41':
                self.show_documentation()
            elif choice == '42':
                self.show_quickstart()
            elif choice == '43':
                self.show_status()
            elif choice == '44':
                try:
                    from configuration_system import ConfigurationManager
                    config = ConfigurationManager()
                    print("\n⚙️  Configuration Information")
                    config.display_settings()
                except ImportError:
                    print("❌ Configuration module not found")
                    input("\nPress Enter to continue...")
            elif choice == '45':
                print("\n❓ Help & Support")
                print("""
This is a comprehensive 8-bit logic gates computer system with multi-architecture support.

KEY FEATURES:
• Logic Gates Module: Basic digital logic operations
• Multi-Architecture: 8, 16, 32, 64-bit systems
• Configuration: Persistent JSON-based settings
• Input System: Keyboard, mouse, gamepad support
• Boot Sequences: Animated splash, boot, and loading screens
• Tools: Debugger, profiler, analyzer, monitor, diagnostics
• Code Generation: C, C++17, Assembly code output
• Visualization: Transistor diagrams, blueprints, circuit builder
• Web Interface: REST API and HTML-based UI

For more information, see COMPLETE_DOCUMENTATION.md
                """)
                input("\nPress Enter to return to main menu...")
            # Advanced Options (46-50)
            elif choice == '46':
                print("\n💾 Export Configuration")
                try:
                    from configuration_system import ConfigurationManager
                    config = ConfigurationManager()
                    config.save_configuration()
                    print("✅ Configuration exported successfully")
                except ImportError:
                    print("❌ Configuration module not found")
                input("\nPress Enter to continue...")
            elif choice == '47':
                print("\n📥 Import Configuration")
                try:
                    from configuration_system import ConfigurationManager
                    config = ConfigurationManager()
                    config.load_configuration()
                    print("✅ Configuration imported successfully")
                except ImportError:
                    print("❌ Configuration module not found")
                input("\nPress Enter to continue...")
            elif choice == '48':
                print("\n🔄 Reset to Defaults")
                try:
                    from configuration_system import ConfigurationManager
                    config = ConfigurationManager()
                    config.reset_to_defaults()
                    print("✅ Configuration reset to defaults")
                except ImportError:
                    print("❌ Configuration module not found")
                input("\nPress Enter to continue...")
            elif choice == '49':
                print("\n" + "=" * 70)
                print("About 8-Bit Logic Gates Computer System")
                print("=" * 70)
                print(f"\nSystem Name: {self.system_name}")
                print(f"Version: {self.version}")
                print("Type: Complete computer architecture simulation")
                print("Architecture Support: 8, 16, 32, 64-bit")
                print("Module Count: 22 files")
                print("Code Lines: 5000+")
                print("\nFeatures:")
                print("  ✓ Logic gates and digital circuits")
                print("  ✓ Multi-architecture CPU simulation")
                print("  ✓ Configuration management system")
                print("  ✓ Input handling (keyboard/mouse/gamepad)")
                print("  ✓ Boot/splash/loading screens")
                print("  ✓ Debugging and profiling tools")
                print("  ✓ Code generation (C/C++/Assembly)")
                print("  ✓ Web interface and REST API")
                print("\n" + "=" * 70)
                input("\nPress Enter to return to main menu...")
            elif choice == '50':
                self.run_gui()
            # Gaming Systems (51-60)
            elif choice == '51':
                self.run_gameboy_emulator()
            elif choice == '52':
                self.run_nes_emulator()
            elif choice == '53':
                self.load_and_play_rom()
            elif choice == '54':
                self.run_rom_tester()
            elif choice == '55':
                self.run_games_menu()
            elif choice == '56':
                self.profile_game_performance()
            elif choice == '57':
                self.debug_game_execution()
            elif choice == '58':
                self.analyze_game_memory()
            elif choice == '59':
                self.manage_rom_library()
            elif choice == '60':
                self.test_rom_compatibility()
            # Development SDK Tools (61-65)
            elif choice == '61':
                self.sdk_create_project()
            elif choice == '62':
                self.sdk_open_project()
            elif choice == '63':
                self.sdk_save_project()
            elif choice == '64':
                self.sdk_build_project()
            elif choice == '65':
                self.sdk_project_settings()
            # Plugin System Tools (66-70)
            elif choice == '66':
                self.plugin_load_system()
            elif choice == '67':
                self.plugin_list_available()
            elif choice == '68':
                self.plugin_enable()
            elif choice == '69':
                self.plugin_disable()
            elif choice == '70':
                self.plugin_configure()
            # IDE Development Tools (71-75)
            elif choice == '71':
                self.editor_ui_launch()
            elif choice == '72':
                self.asm_ide_launch()
            elif choice == '73':
                self.c_ide_launch()
            elif choice == '74':
                self.compilation_test()
            elif choice == '75':
                self.integrated_dev_menu()
            # RPG Maker MZ Tools (76-80)
            elif choice == '76':
                self.rpg_maker_api_demo()
            elif choice == '77':
                self.rpg_create_project()
            elif choice == '78':
                self.rpg_database_editor()
            elif choice == '79':
                self.rpg_play_test()
            elif choice == '80':
                self.rpg_advanced_tools()
            else:
                print("\n❌ Invalid choice. Please enter a number between 1-80 or 0 to exit.")
                input("Press Enter to continue...")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("Initializing 8-Bit Logic Gates Computer System...")
    system = MasterSystem()
    system.run()
