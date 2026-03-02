"""
Configuration and Settings System
Global configuration, preferences, and options management
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path

# ============================================================================
# CONFIGURATION ENUMS
# ============================================================================

class Theme(Enum):
    """UI Themes"""
    DARK = "dark"
    LIGHT = "light"
    NEON = "neon"
    RETRO = "retro"

class Architecture(Enum):
    """System architectures"""
    BIT_8 = "8-bit"
    BIT_16 = "16-bit"
    BIT_32 = "32-bit"
    BIT_64 = "64-bit"

class InputMode(Enum):
    """Input methods"""
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    GAMEPAD = "gamepad"

class DebugLevel(Enum):
    """Debug output levels"""
    OFF = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5

# ============================================================================
# CONFIGURATION DATACLASSES
# ============================================================================

@dataclass
class DisplaySettings:
    """Display configuration"""
    width: int = 80
    height: int = 30
    theme: str = "dark"
    enable_colors: bool = True
    enable_animations: bool = True
    fps: int = 60
    fullscreen: bool = False

@dataclass
class AudioSettings:
    """Audio configuration"""
    enabled: bool = True
    volume: int = 100  # 0-100
    master_volume: int = 100
    sound_effects: bool = True
    background_music: bool = True

@dataclass
class PerformanceSettings:
    """Performance configuration"""
    cpu_throttle: bool = False
    memory_limit: int = 512  # MB
    cache_enabled: bool = True
    cache_size: int = 32  # KB
    optimize_memory: bool = True
    preload_modules: bool = False

@dataclass
class InputSettings:
    """Input configuration"""
    primary_input: str = "keyboard"
    mouse_enabled: bool = True
    gamepad_enabled: bool = True
    keyboard_layout: str = "qwerty"
    mouse_sensitivity: int = 50
    gamepad_sensitivity: int = 50
    enable_macros: bool = False

@dataclass
class SystemSettings:
    """System configuration"""
    default_architecture: str = "32-bit"
    enable_history: bool = True
    max_history: int = 1000
    auto_save: bool = True
    save_interval: int = 300  # seconds
    enable_logging: bool = True
    log_level: int = 3  # INFO

@dataclass
class DebugSettings:
    """Debug configuration"""
    debug_enabled: bool = False
    debug_level: int = 0  # OFF
    debug_console: bool = False
    memory_debug: bool = False
    instruction_trace: bool = False
    breakpoints_enabled: bool = True

@dataclass
class UserPreferences:
    """User preferences"""
    startup_menu: str = "main"
    default_calculator: str = "scientific"
    auto_boot: bool = False
    show_splash_screen: bool = True
    show_boot_screen: bool = True
    compact_mode: bool = False
    language: str = "english"
    timezone: str = "UTC"

@dataclass
class Configuration:
    """Master configuration"""
    version: str = "1.0.0"
    display: DisplaySettings = field(default_factory=DisplaySettings)
    audio: AudioSettings = field(default_factory=AudioSettings)
    performance: PerformanceSettings = field(default_factory=PerformanceSettings)
    input: InputSettings = field(default_factory=InputSettings)
    system: SystemSettings = field(default_factory=SystemSettings)
    debug: DebugSettings = field(default_factory=DebugSettings)
    user: UserPreferences = field(default_factory=UserPreferences)

# ============================================================================
# CONFIGURATION MANAGER
# ============================================================================

class ConfigurationManager:
    """Manage system configuration"""
    
    CONFIG_DIR = Path.home() / ".logic_gates_system"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    DEFAULT_CONFIG_FILE = CONFIG_DIR / "config_default.json"
    
    def __init__(self):
        self.config = Configuration()
        self.config_path = self.CONFIG_FILE
        self._ensure_config_dir()
        self.load_configuration()
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    def save_configuration(self) -> bool:
        """Save configuration to file"""
        try:
            config_dict = {
                'version': self.config.version,
                'display': asdict(self.config.display),
                'audio': asdict(self.config.audio),
                'performance': asdict(self.config.performance),
                'input': asdict(self.config.input),
                'system': asdict(self.config.system),
                'debug': asdict(self.config.debug),
                'user': asdict(self.config.user)
            }
            
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_dict, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def load_configuration(self) -> bool:
        """Load configuration from file"""
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r') as f:
                    config_dict = json.load(f)
                
                self.config.display = DisplaySettings(**config_dict.get('display', {}))
                self.config.audio = AudioSettings(**config_dict.get('audio', {}))
                self.config.performance = PerformanceSettings(**config_dict.get('performance', {}))
                self.config.input = InputSettings(**config_dict.get('input', {}))
                self.config.system = SystemSettings(**config_dict.get('system', {}))
                self.config.debug = DebugSettings(**config_dict.get('debug', {}))
                self.config.user = UserPreferences(**config_dict.get('user', {}))
                
                return True
        except Exception as e:
            print(f"Error loading configuration: {e}")
        
        return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults"""
        try:
            self.config = Configuration()
            return self.save_configuration()
        except Exception as e:
            print(f"Error resetting configuration: {e}")
            return False
    
    def get_setting(self, path: str) -> Any:
        """Get setting by path (e.g., 'display.theme')"""
        parts = path.split('.')
        value = self.config
        
        for part in parts:
            if hasattr(value, part):
                value = getattr(value, part)
            else:
                return None
        
        return value
    
    def set_setting(self, path: str, value: Any) -> bool:
        """Set setting by path"""
        try:
            parts = path.split('.')
            obj = self.config
            
            for part in parts[:-1]:
                obj = getattr(obj, part)
            
            setattr(obj, parts[-1], value)
            return self.save_configuration()
        except Exception as e:
            print(f"Error setting configuration: {e}")
            return False
    
    def export_configuration(self, filepath: str) -> bool:
        """Export configuration to file"""
        try:
            config_dict = {
                'version': self.config.version,
                'display': asdict(self.config.display),
                'audio': asdict(self.config.audio),
                'performance': asdict(self.config.performance),
                'input': asdict(self.config.input),
                'system': asdict(self.config.system),
                'debug': asdict(self.config.debug),
                'user': asdict(self.config.user)
            }
            
            with open(filepath, 'w') as f:
                json.dump(config_dict, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error exporting configuration: {e}")
            return False
    
    def import_configuration(self, filepath: str) -> bool:
        """Import configuration from file"""
        try:
            with open(filepath, 'r') as f:
                config_dict = json.load(f)
            
            self.config.display = DisplaySettings(**config_dict.get('display', {}))
            self.config.audio = AudioSettings(**config_dict.get('audio', {}))
            self.config.performance = PerformanceSettings(**config_dict.get('performance', {}))
            self.config.input = InputSettings(**config_dict.get('input', {}))
            self.config.system = SystemSettings(**config_dict.get('system', {}))
            self.config.debug = DebugSettings(**config_dict.get('debug', {}))
            self.config.user = UserPreferences(**config_dict.get('user', {}))
            
            return self.save_configuration()
        except Exception as e:
            print(f"Error importing configuration: {e}")
            return False
    
    def display_settings(self) -> str:
        """Display current settings"""
        output = """
╔════════════════════════════════════════════════════════════════════════════╗
║                      CURRENT CONFIGURATION SETTINGS                        ║
╠════════════════════════════════════════════════════════════════════════════╣

Display Settings:
  Width:              {width} characters
  Height:             {height} lines
  Theme:              {theme}
  Colors Enabled:     {colors}
  Animations:         {animations}
  FPS:                {fps}
  Fullscreen:         {fullscreen}

Audio Settings:
  Enabled:            {audio_enabled}
  Master Volume:      {master_vol}%
  Effects Volume:     {effects_vol}%
  Sound Effects:      {effects}
  Background Music:   {music}

Performance Settings:
  CPU Throttle:       {cpu_throttle}
  Memory Limit:       {mem_limit}MB
  Cache Enabled:      {cache_enabled}
  Cache Size:         {cache_size}KB
  Memory Optimization:{mem_opt}
  Preload Modules:    {preload}

Input Settings:
  Primary Input:      {primary_input}
  Mouse Enabled:      {mouse}
  Gamepad Enabled:    {gamepad}
  Keyboard Layout:    {kbd_layout}
  Mouse Sensitivity:  {mouse_sens}
  Gamepad Sensitivity:{gamepad_sens}

System Settings:
  Default Architecture: {arch}
  History Enabled:    {history}
  Max History:        {max_hist} entries
  Auto Save:          {auto_save}
  Save Interval:      {save_int}s
  Logging Enabled:    {logging}

Debug Settings:
  Debug Enabled:      {debug_enabled}
  Debug Level:        {debug_level}
  Memory Debug:       {mem_debug}
  Instruction Trace:  {instr_trace}

User Preferences:
  Startup Menu:       {startup}
  Default Calculator: {calc}
  Auto Boot:          {boot}
  Show Splash:        {splash}
  Show Boot Screen:   {boot_screen}
  Compact Mode:       {compact}
  Language:           {language}

╚════════════════════════════════════════════════════════════════════════════╝
""".format(
            width=self.config.display.width,
            height=self.config.display.height,
            theme=self.config.display.theme,
            colors="Yes" if self.config.display.enable_colors else "No",
            animations="Yes" if self.config.display.enable_animations else "No",
            fps=self.config.display.fps,
            fullscreen="Yes" if self.config.display.fullscreen else "No",
            audio_enabled="Yes" if self.config.audio.enabled else "No",
            master_vol=self.config.audio.master_volume,
            effects_vol=self.config.audio.volume,
            effects="Yes" if self.config.audio.sound_effects else "No",
            music="Yes" if self.config.audio.background_music else "No",
            cpu_throttle="Yes" if self.config.performance.cpu_throttle else "No",
            mem_limit=self.config.performance.memory_limit,
            cache_enabled="Yes" if self.config.performance.cache_enabled else "No",
            cache_size=self.config.performance.cache_size,
            mem_opt="Yes" if self.config.performance.optimize_memory else "No",
            preload="Yes" if self.config.performance.preload_modules else "No",
            primary_input=self.config.input.primary_input,
            mouse="Yes" if self.config.input.mouse_enabled else "No",
            gamepad="Yes" if self.config.input.gamepad_enabled else "No",
            kbd_layout=self.config.input.keyboard_layout,
            mouse_sens=self.config.input.mouse_sensitivity,
            gamepad_sens=self.config.input.gamepad_sensitivity,
            arch=self.config.system.default_architecture,
            history="Yes" if self.config.system.enable_history else "No",
            max_hist=self.config.system.max_history,
            auto_save="Yes" if self.config.system.auto_save else "No",
            save_int=self.config.system.save_interval,
            logging="Yes" if self.config.system.enable_logging else "No",
            debug_enabled="Yes" if self.config.debug.debug_enabled else "No",
            debug_level=self.config.debug.debug_level,
            mem_debug="Yes" if self.config.debug.memory_debug else "No",
            instr_trace="Yes" if self.config.debug.instruction_trace else "No",
            startup=self.config.user.startup_menu,
            calc=self.config.user.default_calculator,
            boot="Yes" if self.config.user.auto_boot else "No",
            splash="Yes" if self.config.user.show_splash_screen else "No",
            boot_screen="Yes" if self.config.user.show_boot_screen else "No",
            compact="Yes" if self.config.user.compact_mode else "No",
            language=self.config.user.language
        )
        return output

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_configuration():
    """Demonstrate configuration system"""
    manager = ConfigurationManager()
    
    print("\n" + "="*80)
    print("CONFIGURATION SYSTEM DEMONSTRATION")
    print("="*80)
    
    print(manager.display_settings())
    
    print("\nModifying settings...")
    manager.set_setting('display.theme', 'neon')
    manager.set_setting('audio.volume', 75)
    manager.set_setting('system.default_architecture', '64-bit')
    manager.set_setting('debug.debug_enabled', True)
    print("✓ Settings updated")
    
    print("\nSaving configuration...")
    if manager.save_configuration():
        print("✓ Configuration saved successfully")
        print(f"  Location: {manager.CONFIG_FILE}")

if __name__ == "__main__":
    demonstrate_configuration()
