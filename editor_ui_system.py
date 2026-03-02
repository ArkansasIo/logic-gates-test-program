"""
EDITOR UI SYSTEM
================
RPG Maker MZ-style editor UI with windows, widgets, and menus
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum

# ============================================================================
# UI ENUMERATIONS
# ============================================================================

class TextAlign(Enum):
    """Text alignment options"""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

class WindowType(Enum):
    """Window types"""
    NORMAL = "normal"
    DIALOG = "dialog"
    DOCKABLE = "dockable"
    FLOATING = "floating"

# ============================================================================
# UI COMPONENTS
# ============================================================================

@dataclass
class UIRect:
    """Rectangle for UI components"""
    x: int
    y: int
    width: int
    height: int
    
    def contains_point(self, px: int, py: int) -> bool:
        return self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height

class UIWidget:
    """Base UI widget"""
    
    def __init__(self, name: str, rect: UIRect):
        self.name = name
        self.rect = rect
        self.visible = True
        self.enabled = True
        self.on_click: Optional[Callable] = None
        
    def render(self):
        """Render widget"""
        if self.visible:
            print(f"  [{self.name}@({self.rect.x},{self.rect.y}): {self.rect.width}x{self.rect.height}]")
    
    def on_mouse_click(self, x: int, y: int):
        """Handle mouse click"""
        if self.on_click and self.rect.contains_point(x, y):
            self.on_click()

class UILabel(UIWidget):
    """Text label widget"""
    
    def __init__(self, name: str, rect: UIRect, text: str = ""):
        super().__init__(name, rect)
        self.text = text
        self.text_align = TextAlign.LEFT
        self.text_color = "#000000"
        
    def render(self):
        if self.visible:
            print(f"  [Label] {self.text}")

class UIButton(UIWidget):
    """Button widget"""
    
    def __init__(self, name: str, rect: UIRect, text: str = ""):
        super().__init__(name, rect)
        self.text = text
        self.pressed = False
        
    def render(self):
        if self.visible:
            state = "PRESSED" if self.pressed else "NORMAL"
            print(f"  [Button:{state}] {self.text}")
    
    def on_mouse_click(self, x: int, y: int):
        if self.enabled and self.rect.contains_point(x, y):
            self.pressed = True
            if self.on_click:
                self.on_click()

class UITextBox(UIWidget):
    """Text input box"""
    
    def __init__(self, name: str, rect: UIRect):
        super().__init__(name, rect)
        self.text = ""
        self.cursor_pos = 0
        self.placeholder = "Enter text..."
        
    def render(self):
        if self.visible:
            display_text = self.text if self.text else self.placeholder
            print(f"  [TextBox] {display_text}")
    
    def input_char(self, char: str):
        """Input character"""
        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
        self.cursor_pos += 1

class UIDropdown(UIWidget):
    """Dropdown/Combo box"""
    
    def __init__(self, name: str, rect: UIRect, options: List[str]):
        super().__init__(name, rect)
        self.options = options
        self.selected_index = 0
        self.expanded = False
        
    def render(self):
        if self.visible:
            selected = self.options[self.selected_index] if self.options else "None"
            print(f"  [Dropdown] {selected}")
    
    def select_option(self, index: int):
        if 0 <= index < len(self.options):
            self.selected_index = index

class UIList(UIWidget):
    """List widget"""
    
    def __init__(self, name: str, rect: UIRect, items: List[str]):
        super().__init__(name, rect)
        self.items = items
        self.selected_index = -1
        self.scroll_offset = 0
        self.visible_items = 5
        
    def render(self):
        if self.visible:
            print(f"  [List] {len(self.items)} items")
            for i, item in enumerate(self.items[:self.visible_items]):
                marker = ">" if i == self.selected_index else " "
                print(f"    {marker} {item}")

class UIPanel(UIWidget):
    """Container panel for grouping widgets"""
    
    def __init__(self, name: str, rect: UIRect):
        super().__init__(name, rect)
        self.children: List[UIWidget] = []
        self.background_color = "#FFFFFF"
        self.border_color = "#000000"
        self.border_width = 1
        
    def add_widget(self, widget: UIWidget):
        """Add widget to panel"""
        self.children.append(widget)
        
    def render(self):
        if self.visible:
            print(f"  [Panel] {self.name} ({len(self.children)} widgets)")
            for child in self.children:
                child.render()

# ============================================================================
# WINDOWS
# ============================================================================

class UIWindow:
    """Editor window"""
    
    def __init__(self, title: str, rect: UIRect, window_type: WindowType = WindowType.NORMAL):
        self.title = title
        self.rect = rect
        self.window_type = window_type
        self.visible = True
        self.focused = False
        self.widgets: List[UIWidget] = []
        self.title_bar_height = 24
        self.menu_bar = None
        
    def add_widget(self, widget: UIWidget):
        """Add widget to window"""
        self.widgets.append(widget)
        
    def set_focus(self):
        """Set window focus"""
        self.focused = True
        print(f"📌 Window focused: {self.title}")
    
    def render(self):
        """Render window"""
        if not self.visible:
            return
        
        focus_indicator = "● " if self.focused else "○ "
        print(f"\n{focus_indicator}╔═══════════════════════════════════════════════════════════════╗")
        print(f"{' ' if not self.focused else '●'} ║ {self.title:<63} ║")
        print(f"  ╠═══════════════════════════════════════════════════════════════╣")
        
        for widget in self.widgets:
            widget.render()
        
        print(f"  ╚═══════════════════════════════════════════════════════════════╝")

# ============================================================================
# MENU SYSTEM
# ============================================================================

class MenuItem:
    """Menu item"""
    
    def __init__(self, label: str, action: Optional[Callable] = None, submenu: Optional['Menu'] = None):
        self.label = label
        self.action = action
        self.submenu = submenu
        self.shortcut = None
        self.separator = False
        
    def execute(self):
        if self.action:
            self.action()

class Menu:
    """Menu bar or submenu"""
    
    def __init__(self, name: str = ""):
        self.name = name
        self.items: List[MenuItem] = []
        self.parent = None
        
    def add_item(self, label: str, action: Optional[Callable] = None) -> MenuItem:
        item = MenuItem(label, action)
        self.items.append(item)
        return item
    
    def add_submenu(self, label: str) -> 'Menu':
        submenu = Menu(label)
        submenu.parent = self
        item = MenuItem(label, submenu=submenu)
        self.items.append(item)
        return submenu
    
    def add_separator(self):
        separator = MenuItem("---")
        separator.separator = True
        self.items.append(separator)
    
    def render(self, indent: int = 0):
        if indent == 0:
            # Main menu bar
            print("\n  Menu: ", end="")
            for item in self.items:
                if not item.separator:
                    print(f"[{item.label}]", end=" ")
            print()
        else:
            # Submenu
            print(f"\n{'  ' * indent}{self.name}:")
            for item in self.items:
                if item.separator:
                    print(f"{'  ' * (indent + 1)}{item.label}")
                else:
                    shortcut = f" ({item.shortcut})" if item.shortcut else ""
                    if item.submenu:
                        item.submenu.render(indent + 1)
                    else:
                        print(f"{'  ' * (indent + 1)}→ {item.label}{shortcut}")

# ============================================================================
# EDITOR UI LAYOUT
# ============================================================================

class EditorUILayout:
    """Editor UI layout manager"""
    
    def __init__(self):
        self.windows: Dict[str, UIWindow] = {}
        self.menus: Dict[str, Menu] = {}
        self.active_window: Optional[str] = None
        
    def create_window(self, name: str, title: str, rect: UIRect) -> UIWindow:
        """Create window"""
        window = UIWindow(title, rect)
        self.windows[name] = window
        if self.active_window is None:
            self.active_window = name
        return window
    
    def create_menu(self, name: str) -> Menu:
        """Create menu"""
        menu = Menu(name)
        self.menus[name] = menu
        return menu
    
    def get_window(self, name: str) -> Optional[UIWindow]:
        """Get window"""
        return self.windows.get(name)
    
    def set_active_window(self, name: str):
        """Set active window"""
        if name in self.windows:
            self.active_window = name
            self.windows[name].set_focus()
    
    def render_all(self):
        """Render entire UI"""
        print("\n" + "=" * 70)
        print("EDITOR UI LAYOUT")
        print("=" * 70)
        
        # Render menus
        for menu in self.menus.values():
            menu.render()
        
        # Render windows
        for window in self.windows.values():
            window.render()

# ============================================================================
# DEMONSTRATION FUNCTION
# ============================================================================

def demonstrate_editor_ui():
    """Demonstrate editor UI system"""
    print("\n" + "=" * 70)
    print("EDITOR UI SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Create layout
    layout = EditorUILayout()
    
    # Create main menu
    main_menu = layout.create_menu("Main")
    file_menu = main_menu.add_submenu("File")
    file_menu.add_item("New Project", lambda: print("  → Creating new project..."))
    file_menu.add_item("Open Project", lambda: print("  → Opening project..."))
    file_menu.add_separator()
    file_menu.add_item("Save", lambda: print("  → Saving..."))
    file_menu.add_item("Exit")
    
    edit_menu = main_menu.add_submenu("Edit")
    edit_menu.add_item("Undo")
    edit_menu.add_item("Redo")
    edit_menu.add_separator()
    edit_menu.add_item("Cut")
    edit_menu.add_item("Copy")
    edit_menu.add_item("Paste")
    
    tools_menu = main_menu.add_submenu("Tools")
    tools_menu.add_item("Debugger")
    tools_menu.add_item("Profiler")
    tools_menu.add_item("Memory Analyzer")
    
    # Create project explorer window
    project_win = layout.create_window("project", "Project Explorer", UIRect(0, 0, 300, 400))
    project_panel = UIPanel("project_root", UIRect(0, 0, 280, 380))
    project_list = UIList("files", UIRect(0, 0, 280, 380), [
        "📁 Source Code",
        "📁 Assets",
        "📁 Data",
        "📄 main.asm",
        "📄 engine.c",
        "📄 config.h",
        "📄 README.md"
    ])
    project_list.selected_index = 3
    project_panel.add_widget(project_list)
    project_win.add_widget(project_panel)
    
    # Create code editor window
    code_win = layout.create_window("editor", "Code Editor", UIRect(300, 0, 500, 400))
    code_label = UILabel("file_name", UIRect(0, 0, 480, 20), "main.asm - Assembly")
    code_panel = UIPanel("code_editor", UIRect(0, 20, 480, 360))
    code_panel.add_widget(code_label)
    code_win.add_widget(code_panel)
    
    # Create properties window
    props_win = layout.create_window("properties", "Properties", UIRect(800, 0, 200, 400))
    props_panel = UIPanel("props", UIRect(0, 0, 180, 380))
    props_label1 = UILabel("prop1", UIRect(0, 0, 180, 20), "Name: main.asm")
    props_label2 = UILabel("prop2", UIRect(0, 20, 180, 20), "Size: 1,024 bytes")
    props_label3 = UILabel("prop3", UIRect(0, 40, 180, 20), "Lines: 42")
    props_panel.add_widget(props_label1)
    props_panel.add_widget(props_label2)
    props_panel.add_widget(props_label3)
    props_win.add_widget(props_panel)
    
    # Render UI
    main_menu.render(0)
    layout.render_all()
    
    print("\n✅ Editor UI demonstration complete!")

if __name__ == "__main__":
    demonstrate_editor_ui()
