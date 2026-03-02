"""
PLUGIN SYSTEM
=============
Plugin architecture, management, and lifecycle handling
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
import json
from abc import ABC, abstractmethod

# ============================================================================
# PLUGIN ENUMS
# ============================================================================

class PluginStatus(Enum):
    """Plugin lifecycle states"""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    DISABLED = "disabled"
    ERROR = "error"

class PluginType(Enum):
    """Types of plugins"""
    LANGUAGE = "language"
    TOOL = "tool"
    UI = "ui"
    BUILD = "build"
    DEBUG = "debug"
    EXTENSION = "extension"

# ============================================================================
# PLUGIN INTERFACE
# ============================================================================

@dataclass
class PluginManifest:
    """Plugin metadata and configuration"""
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    entry_point: str
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    enabled: bool = True
    priority: int = 0

class IPlugin(ABC):
    """Base plugin interface"""
    
    def __init__(self, manifest: PluginManifest):
        self.manifest = manifest
        self.status = PluginStatus.UNLOADED
        self.hooks: Dict[str, List[Callable]] = {}
        
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize plugin"""
        pass
    
    @abstractmethod
    def execute(self) -> bool:
        """Execute plugin functionality"""
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """Shutdown plugin"""
        pass
    
    def register_hook(self, hook_name: str, callback: Callable):
        """Register hook callback"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
    
    def call_hook(self, hook_name: str, *args, **kwargs):
        """Call registered hooks"""
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                callback(*args, **kwargs)

# ============================================================================
# STANDARD PLUGINS
# ============================================================================

class LanguagePlugin(IPlugin):
    """Language support plugin"""
    
    def __init__(self, name: str, language: str):
        manifest = PluginManifest(
            name=name,
            version="1.0.0",
            description=f"Support for {language} language",
            author="SDK Team",
            plugin_type=PluginType.LANGUAGE,
            entry_point="LanguagePlugin"
        )
        super().__init__(manifest)
        self.language = language
        
    def initialize(self) -> bool:
        self.status = PluginStatus.INITIALIZED
        print(f"✓ {self.language} language plugin initialized")
        return True
    
    def execute(self) -> bool:
        self.status = PluginStatus.ACTIVE
        print(f"✓ {self.language} language support loaded")
        return True
    
    def shutdown(self) -> bool:
        self.status = PluginStatus.UNLOADED
        return True

class DebuggerPlugin(IPlugin):
    """Debugger plugin"""
    
    def __init__(self):
        manifest = PluginManifest(
            name="Advanced Debugger",
            version="1.2.0",
            description="Integrated debugging support",
            author="SDK Team",
            plugin_type=PluginType.DEBUG,
            entry_point="DebuggerPlugin"
        )
        super().__init__(manifest)
        self.breakpoints: Dict[str, int] = {}
        
    def initialize(self) -> bool:
        self.status = PluginStatus.INITIALIZED
        print("✓ Debugger plugin initialized")
        return True
    
    def execute(self) -> bool:
        self.status = PluginStatus.ACTIVE
        print("✓ Debugger activated")
        return True
    
    def shutdown(self) -> bool:
        self.status = PluginStatus.UNLOADED
        return True
    
    def set_breakpoint(self, filename: str, line: int):
        """Set breakpoint"""
        self.breakpoints[filename] = line
        print(f"  Breakpoint set at {filename}:{line}")
    
    def get_breakpoints(self) -> Dict[str, int]:
        """Get all breakpoints"""
        return self.breakpoints

class BuildToolPlugin(IPlugin):
    """Build tool plugin"""
    
    def __init__(self, tool_name: str):
        manifest = PluginManifest(
            name=f"{tool_name} Build Tool",
            version="1.0.0",
            description=f"Build support for {tool_name}",
            author="SDK Team",
            plugin_type=PluginType.BUILD,
            entry_point="BuildToolPlugin"
        )
        super().__init__(manifest)
        self.tool_name = tool_name
        
    def initialize(self) -> bool:
        self.status = PluginStatus.INITIALIZED
        return True
    
    def execute(self) -> bool:
        self.status = PluginStatus.ACTIVE
        print(f"✓ {self.tool_name} build system activated")
        return True
    
    def shutdown(self) -> bool:
        self.status = PluginStatus.UNLOADED
        return True

# ============================================================================
# PLUGIN MANAGER
# ============================================================================

class PluginManager:
    """Manage plugin lifecycle and execution"""
    
    def __init__(self):
        self.plugins: Dict[str, IPlugin] = {}
        self.plugin_registry: Dict[str, PluginManifest] = {}
        self.enabled_plugins: List[str] = []
        self.disabled_plugins: List[str] = []
        
    def register_plugin(self, manifest: PluginManifest):
        """Register plugin manifest"""
        self.plugin_registry[manifest.name] = manifest
        print(f"📋 Plugin registered: {manifest.name} ({manifest.version})")
    
    def load_plugin(self, plugin_name: str, plugin: IPlugin) -> bool:
        """Load plugin instance"""
        if plugin_name in self.plugins:
            print(f"⚠️  Plugin already loaded: {plugin_name}")
            return False
        
        print(f"📥 Loading plugin: {plugin_name}")
        self.plugins[plugin_name] = plugin
        plugin.status = PluginStatus.LOADING
        
        if plugin.initialize():
            self.enabled_plugins.append(plugin_name)
            print(f"✅ Plugin loaded: {plugin_name}")
            return True
        else:
            plugin.status = PluginStatus.ERROR
            print(f"❌ Failed to load plugin: {plugin_name}")
            return False
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable plugin"""
        if plugin_name not in self.plugins:
            print(f"⚠️  Plugin not found: {plugin_name}")
            return False
        
        plugin = self.plugins[plugin_name]
        if plugin.execute():
            if plugin_name not in self.enabled_plugins:
                self.enabled_plugins.append(plugin_name)
            if plugin_name in self.disabled_plugins:
                self.disabled_plugins.remove(plugin_name)
            print(f"✅ Plugin enabled: {plugin_name}")
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable plugin"""
        if plugin_name not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_name]
        if plugin_name in self.enabled_plugins:
            self.enabled_plugins.remove(plugin_name)
        if plugin_name not in self.disabled_plugins:
            self.disabled_plugins.append(plugin_name)
        
        print(f"🔇 Plugin disabled: {plugin_name}")
        return True
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload plugin"""
        if plugin_name not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_name]
        if plugin.shutdown():
            del self.plugins[plugin_name]
            if plugin_name in self.enabled_plugins:
                self.enabled_plugins.remove(plugin_name)
            print(f"📤 Plugin unloaded: {plugin_name}")
            return True
        return False
    
    def get_plugin(self, plugin_name: str) -> Optional[IPlugin]:
        """Get plugin instance"""
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> Dict[str, str]:
        """List all loaded plugins with status"""
        return {name: plugin.status.value for name, plugin in self.plugins.items()}
    
    def display_plugin_status(self):
        """Display plugin status"""
        print("\n" + "=" * 70)
        print("PLUGIN MANAGER STATUS")
        print("=" * 70)
        
        print(f"\n📊 Registered Plugins: {len(self.plugin_registry)}")
        for name, manifest in self.plugin_registry.items():
            print(f"  • {name} ({manifest.version}): {manifest.description}")
        
        print(f"\n✅ Enabled Plugins: {len(self.enabled_plugins)}")
        for name in self.enabled_plugins:
            plugin = self.plugins.get(name)
            if plugin:
                print(f"  ✓ {name} - {plugin.status.value}")
        
        print(f"\n❌ Disabled Plugins: {len(self.disabled_plugins)}")
        for name in self.disabled_plugins:
            print(f"  ✗ {name}")

# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demonstrate_plugin_system():
    """Demonstrate plugin system"""
    print("\n" + "=" * 70)
    print("PLUGIN SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Create plugin manager
    pm = PluginManager()
    
    # Create and register plugins
    print("\n1️⃣  Creating plugins...")
    
    c_plugin = LanguagePlugin("C Language Support", "C")
    asm_plugin = LanguagePlugin("Assembly Support", "Assembly")
    debugger_plugin = DebuggerPlugin()
    gcc_plugin = BuildToolPlugin("GCC")
    
    # Register plugins
    print("\n2️⃣  Registering plugins...")
    pm.register_plugin(c_plugin.manifest)
    pm.register_plugin(asm_plugin.manifest)
    pm.register_plugin(debugger_plugin.manifest)
    pm.register_plugin(gcc_plugin.manifest)
    
    # Load plugins
    print("\n3️⃣  Loading plugins...")
    pm.load_plugin("C Language", c_plugin)
    pm.load_plugin("Assembly Language", asm_plugin)
    pm.load_plugin("Debugger", debugger_plugin)
    pm.load_plugin("GCC Build", gcc_plugin)
    
    # Enable plugins
    print("\n4️⃣  Enabling plugins...")
    pm.enable_plugin("C Language")
    pm.enable_plugin("Assembly Language")
    pm.enable_plugin("Debugger")
    pm.enable_plugin("GCC Build")
    
    # Display status
    pm.display_plugin_status()
    
    # Test debugger
    print("\n5️⃣  Testing debugger plugin...")
    debugger = pm.get_plugin("Debugger")
    if debugger:
        debugger.set_breakpoint("main.c", 42)
        debugger.set_breakpoint("engine.c", 128)
        print(f"  Breakpoints: {debugger.get_breakpoints()}")
    
    print("\n✅ Plugin system demonstration complete!")

if __name__ == "__main__":
    demonstrate_plugin_system()
