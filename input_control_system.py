"""
Input and Control System
Keyboard, mouse, and gamepad input handling
"""

from typing import Optional, List, Dict, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import sys

# ============================================================================
# INPUT ENUMS
# ============================================================================

class KeyCode(Enum):
    """Keyboard key codes"""
    # Function keys
    F1 = 0x3B
    F2 = 0x3C
    F3 = 0x3D
    F4 = 0x3E
    F5 = 0x3F
    F6 = 0x40
    F7 = 0x41
    F8 = 0x42
    F9 = 0x43
    F10 = 0x44
    F11 = 0x57
    F12 = 0x58
    
    # Navigation
    HOME = 0x47
    END = 0x4F
    PAGEUP = 0x49
    PAGEDOWN = 0x51
    UP = 0x48
    DOWN = 0x50
    LEFT = 0x4B
    RIGHT = 0x4D
    
    # Special
    ESCAPE = 0x01
    ENTER = 0x1C
    TAB = 0x0F
    BACKSPACE = 0x0E
    DELETE = 0x53
    INSERT = 0x52
    
    # Modifier
    SHIFT_LEFT = 0x2A
    SHIFT_RIGHT = 0x36
    CTRL_LEFT = 0x1D
    CTRL_RIGHT = 0x9D
    ALT_LEFT = 0x38
    ALT_RIGHT = 0xB8

class MouseButton(Enum):
    """Mouse button codes"""
    LEFT = 0x01
    RIGHT = 0x02
    MIDDLE = 0x04
    SCROLL_UP = 0x08
    SCROLL_DOWN = 0x10

class GamepadButton(Enum):
    """Gamepad button codes"""
    A = 0x8000
    B = 0x4000
    X = 0x2000
    Y = 0x1000
    LB = 0x0100
    RB = 0x0200
    LS = 0x0001
    RS = 0x0002
    BACK = 0x0020
    START = 0x0010
    UP = 0x0800
    DOWN = 0x1000
    LEFT = 0x0400
    RIGHT = 0x0200

# ============================================================================
# INPUT DATACLASSES
# ============================================================================

@dataclass
class KeyboardEvent:
    """Keyboard input event"""
    key_code: int
    char: Optional[str] = None
    shift: bool = False
    ctrl: bool = False
    alt: bool = False
    timestamp: float = 0
    
@dataclass
class MouseEvent:
    """Mouse input event"""
    x: int
    y: int
    button: Optional[int] = None
    delta_x: int = 0
    delta_y: int = 0
    scroll: int = 0
    timestamp: float = 0

@dataclass
class GamepadEvent:
    """Gamepad input event"""
    button: int = 0
    trigger_left: float = 0.0  # 0-1
    trigger_right: float = 0.0  # 0-1
    stick_left_x: float = 0.0  # -1 to 1
    stick_left_y: float = 0.0  # -1 to 1
    stick_right_x: float = 0.0  # -1 to 1
    stick_right_y: float = 0.0  # -1 to 1
    timestamp: float = 0

# ============================================================================
# INPUT HANDLERS
# ============================================================================

class KeyboardHandler:
    """Handle keyboard input"""
    
    def __init__(self):
        self.key_bindings: Dict[int, Callable] = {}
        self.last_key: Optional[KeyboardEvent] = None
        self.input_buffer: List[str] = []
    
    def bind_key(self, key_code: int, callback: Callable):
        """Bind key to callback"""
        self.key_bindings[key_code] = callback
    
    def unbind_key(self, key_code: int):
        """Unbind key"""
        if key_code in self.key_bindings:
            del self.key_bindings[key_code]
    
    def handle_key_press(self, event: KeyboardEvent):
        """Handle key press"""
        self.last_key = event
        
        if event.char:
            self.input_buffer.append(event.char)
        
        if event.key_code in self.key_bindings:
            self.key_bindings[event.key_code](event)
    
    def get_input_line(self) -> str:
        """Get complete input line"""
        line = ''.join(self.input_buffer)
        self.input_buffer.clear()
        return line
    
    def clear_input(self):
        """Clear input buffer"""
        self.input_buffer.clear()

class MouseHandler:
    """Handle mouse input"""
    
    def __init__(self):
        self.position: Tuple[int, int] = (0, 0)
        self.last_position: Tuple[int, int] = (0, 0)
        self.button_status: Dict[int, bool] = {}
        self.callbacks: Dict[str, List[Callable]] = {
            'click': [],
            'move': [],
            'scroll': []
        }
    
    def bind_callback(self, event_type: str, callback: Callable):
        """Bind mouse event callback"""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def handle_mouse_event(self, event: MouseEvent):
        """Handle mouse event"""
        self.last_position = self.position
        self.position = (event.x, event.y)
        
        if event.button:
            self.button_status[event.button] = True
            for callback in self.callbacks['click']:
                callback(event)
        
        if event.delta_x != 0 or event.delta_y != 0:
            for callback in self.callbacks['move']:
                callback(event)
        
        if event.scroll != 0:
            for callback in self.callbacks['scroll']:
                callback(event)
    
    def get_position(self) -> Tuple[int, int]:
        """Get mouse position"""
        return self.position
    
    def is_button_pressed(self, button: int) -> bool:
        """Check if button is pressed"""
        return self.button_status.get(button, False)

class GamepadHandler:
    """Handle gamepad input"""
    
    def __init__(self):
        self.button_status: Dict[int, bool] = {}
        self.trigger_left: float = 0.0
        self.trigger_right: float = 0.0
        self.stick_left: Tuple[float, float] = (0.0, 0.0)
        self.stick_right: Tuple[float, float] = (0.0, 0.0)
        self.callbacks: Dict[str, List[Callable]] = {
            'button_press': [],
            'button_release': [],
            'trigger': [],
            'stick': []
        }
        self.deadzone: float = 0.15  # Deadzone for sticks
    
    def bind_callback(self, event_type: str, callback: Callable):
        """Bind gamepad event callback"""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def handle_gamepad_event(self, event: GamepadEvent):
        """Handle gamepad event"""
        # Button events
        for button, is_down in [(event.button & mask, bool(event.button & mask)) 
                                for mask in [0x8000, 0x4000, 0x2000, 0x1000, 
                                           0x0100, 0x0200, 0x0001, 0x0002,
                                           0x0020, 0x0010, 0x0800, 0x1000, 
                                           0x0400, 0x0200]]:
            old_state = self.button_status.get(button, False)
            self.button_status[button] = is_down
            
            if is_down and not old_state:
                for callback in self.callbacks['button_press']:
                    callback(button)
            elif not is_down and old_state:
                for callback in self.callbacks['button_release']:
                    callback(button)
        
        # Trigger events
        self.trigger_left = event.trigger_left
        self.trigger_right = event.trigger_right
        for callback in self.callbacks['trigger']:
            callback(event.trigger_left, event.trigger_right)
        
        # Stick events
        self.stick_left = (event.stick_left_x, event.stick_left_y)
        self.stick_right = (event.stick_right_x, event.stick_right_y)
        for callback in self.callbacks['stick']:
            callback(self.stick_left, self.stick_right)
    
    def get_stick_position(self, stick: str = 'left') -> Tuple[float, float]:
        """Get stick position"""
        if stick == 'left':
            return self.stick_left
        else:
            return self.stick_right
    
    def get_trigger_value(self, trigger: str = 'left') -> float:
        """Get trigger value"""
        if trigger == 'left':
            return self.trigger_left
        else:
            return self.trigger_right
    
    def is_button_pressed(self, button: int) -> bool:
        """Check if button is pressed"""
        return self.button_status.get(button, False)

# ============================================================================
# INPUT MANAGER
# ============================================================================

class InputManager:
    """Unified input management"""
    
    def __init__(self):
        self.keyboard = KeyboardHandler()
        self.mouse = MouseHandler()
        self.gamepad = GamepadHandler()
        self.active_input_mode = "keyboard"
    
    def set_input_mode(self, mode: str):
        """Set active input mode"""
        if mode in ['keyboard', 'mouse', 'gamepad']:
            self.active_input_mode = mode
    
    def process_input(self, input_type: str, event) -> bool:
        """Process input event"""
        if input_type == 'keyboard':
            self.keyboard.handle_key_press(event)
            return True
        elif input_type == 'mouse':
            self.mouse.handle_mouse_event(event)
            return True
        elif input_type == 'gamepad':
            self.gamepad.handle_gamepad_event(event)
            return True
        return False
    
    def display_input_status(self) -> str:
        """Display current input status"""
        kb_buf = ''.join(self.keyboard.input_buffer)
        mouse_pos = self.mouse.get_position()
        gamepad_left = self.gamepad.get_stick_position('left')
        
        status = f"""
Input Status:
  Active Mode:     {self.active_input_mode.upper()}
  Keyboard Buffer: {kb_buf or "(empty)"}
  Mouse Position:  ({mouse_pos[0]}, {mouse_pos[1]})
  Gamepad L-Stick: ({gamepad_left[0]:.2f}, {gamepad_left[1]:.2f})
"""
        return status

# ============================================================================
# INPUT TESTER
# ============================================================================

class InputTester:
    """Test input systems"""
    
    @staticmethod
    def test_keyboard():
        """Test keyboard input"""
        print("\n" + "="*80)
        print("KEYBOARD INPUT TEST")
        print("="*80)
        print("\nSimulated keyboard events:")
        
        handler = KeyboardHandler()
        
        # Simulate key presses
        events = [
            KeyboardEvent(ord('A'), 'A', shift=True),
            KeyboardEvent(ord('b'), 'b'),
            KeyboardEvent(KeyCode.ENTER.value, '\n'),
        ]
        
        for event in events:
            handler.handle_key_press(event)
            print(f"Key: {event.char if event.char else f'0x{event.key_code:02X}'} "
                  f"(Shift: {event.shift}, Ctrl: {event.ctrl})")
        
        print(f"\nInput Buffer: {handler.get_input_line()}")
    
    @staticmethod
    def test_mouse():
        """Test mouse input"""
        print("\n" + "="*80)
        print("MOUSE INPUT TEST")
        print("="*80)
        print("\nSimulated mouse events:")
        
        handler = MouseHandler()
        
        # Simulate mouse events
        events = [
            MouseEvent(100, 50, button=MouseButton.LEFT.value),
            MouseEvent(150, 75, delta_x=50, delta_y=25),
            MouseEvent(150, 80, scroll=3),
        ]
        
        for event in events:
            handler.handle_mouse_event(event)
            if event.button:
                print(f"Click at ({event.x}, {event.y}) Button: {event.button}")
            elif event.delta_x or event.delta_y:
                print(f"Move to ({event.x}, {event.y}) Delta: ({event.delta_x}, {event.delta_y})")
            elif event.scroll:
                print(f"Scroll: {event.scroll}")
        
        print(f"\nFinal Position: {handler.get_position()}")
    
    @staticmethod
    def test_gamepad():
        """Test gamepad input"""
        print("\n" + "="*80)
        print("GAMEPAD INPUT TEST")
        print("="*80)
        print("\nSimulated gamepad events:")
        
        handler = GamepadHandler()
        
        # Simulate gamepad events
        event = GamepadEvent(
            button=GamepadButton.A.value,
            trigger_left=0.75,
            trigger_right=0.25,
            stick_left_x=0.5,
            stick_left_y=0.8,
            stick_right_x=-0.3,
            stick_right_y=-0.6
        )
        
        handler.handle_gamepad_event(event)
        
        print(f"Button A Pressed: {handler.is_button_pressed(GamepadButton.A.value)}")
        print(f"Left Trigger: {handler.get_trigger_value('left')}")
        print(f"Right Trigger: {handler.get_trigger_value('right')}")
        print(f"Left Stick: {handler.get_stick_position('left')}")
        print(f"Right Stick: {handler.get_stick_position('right')}")

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_input_system():
    """Demonstrate input system"""
    print("\n" + "="*80)
    print("INPUT AND CONTROL SYSTEM DEMONSTRATION")
    print("="*80)
    
    InputTester.test_keyboard()
    InputTester.test_mouse()
    InputTester.test_gamepad()
    
    print("\n" + "="*80)
    print("UNIFIED INPUT MANAGER TEST")
    print("="*80)
    
    manager = InputManager()
    manager.set_input_mode('keyboard')
    print(manager.display_input_status())

if __name__ == "__main__":
    demonstrate_input_system()
