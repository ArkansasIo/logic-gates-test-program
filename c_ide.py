"""
C LANGUAGE IDE
==============
C language IDE with syntax highlighting, compilation, and debugging
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
import re

# ============================================================================
# C LANGUAGE ENUMERATIONS
# ============================================================================

class CDataType(Enum):
    """C data types"""
    INT = "int"
    CHAR = "char"
    FLOAT = "float"
    DOUBLE = "double"
    VOID = "void"
    SHORT = "short"
    LONG = "long"
    UNSIGNED = "unsigned"

class CKeywordType(Enum):
    """C keyword types"""
    DATA_TYPE = "data_type"
    CONTROL = "control"
    STORAGE = "storage"
    QUALIFIER = "qualifier"
    OPERATOR = "operator"

# ============================================================================
# C LANGUAGE DEFINITIONS
# ============================================================================

class CLanguageDef:
    """C language definition"""
    
    KEYWORDS = {
        # Data types
        "int": CKeywordType.DATA_TYPE,
        "char": CKeywordType.DATA_TYPE,
        "float": CKeywordType.DATA_TYPE,
        "double": CKeywordType.DATA_TYPE,
        "void": CKeywordType.DATA_TYPE,
        "short": CKeywordType.DATA_TYPE,
        "long": CKeywordType.DATA_TYPE,
        "unsigned": CKeywordType.DATA_TYPE,
        "signed": CKeywordType.DATA_TYPE,
        "struct": CKeywordType.DATA_TYPE,
        "union": CKeywordType.DATA_TYPE,
        "enum": CKeywordType.DATA_TYPE,
        
        # Control flow
        "if": CKeywordType.CONTROL,
        "else": CKeywordType.CONTROL,
        "while": CKeywordType.CONTROL,
        "for": CKeywordType.CONTROL,
        "do": CKeywordType.CONTROL,
        "break": CKeywordType.CONTROL,
        "continue": CKeywordType.CONTROL,
        "switch": CKeywordType.CONTROL,
        "case": CKeywordType.CONTROL,
        "default": CKeywordType.CONTROL,
        "return": CKeywordType.CONTROL,
        "goto": CKeywordType.CONTROL,
        
        # Storage class
        "static": CKeywordType.STORAGE,
        "extern": CKeywordType.STORAGE,
        "auto": CKeywordType.STORAGE,
        "register": CKeywordType.STORAGE,
        "typedef": CKeywordType.STORAGE,
        
        # Type qualifiers
        "const": CKeywordType.QUALIFIER,
        "volatile": CKeywordType.QUALIFIER,
        "restrict": CKeywordType.QUALIFIER,
    }
    
    STANDARD_FUNCTIONS = {
        # I/O
        "printf": ("int", ["const char*"], "Print formatted output"),
        "scanf": ("int", ["const char*"], "Read formatted input"),
        "puts": ("int", ["const char*"], "Print string with newline"),
        "gets": ("char*", [], "Read string (deprecated)"),
        
        # String
        "strlen": ("int", ["const char*"], "String length"),
        "strcpy": ("char*", ["char*", "const char*"], "String copy"),
        "strcmp": ("int", ["const char*", "const char*"], "String compare"),
        "strcat": ("char*", ["char*", "const char*"], "String concatenate"),
        
        # Memory
        "malloc": ("void*", ["int"], "Allocate memory"),
        "calloc": ("void*", ["int", "int"], "Allocate zeroed memory"),
        "free": ("void", ["void*"], "Free memory"),
        "realloc": ("void*", ["void*", "int"], "Reallocate memory"),
        
        # Math
        "abs": ("int", ["int"], "Absolute value"),
        "sqrt": ("double", ["double"], "Square root"),
        "pow": ("double", ["double", "double"], "Power"),
        "sin": ("double", ["double"], "Sine"),
        "cos": ("double", ["double"], "Cosine"),
        
        # General
        "exit": ("void", ["int"], "Exit program"),
        "rand": ("int", [], "Random number"),
        "srand": ("void", ["int"], "Seed random"),
    }

# ============================================================================
# C TOKENS & LEXER
# ============================================================================

@dataclass
class CToken:
    """Token from C code"""
    type: str
    value: str
    line: int
    column: int

class CLexer:
    """C language lexer"""
    
    TOKEN_PATTERNS = [
        ("string", r'"([^"\\\\]|\\\\.)*"'),
        ("char", r"'([^'\\\\]|\\\\.)*'"),
        ("number", r'\b\d+(\.\d+)?([eE][+-]?\d+)?\b'),
        ("comment_line", r'//[^\n]*'),
        ("comment_block", r'/\*[\s\S]*?\*/'),
        ("preproc", r'#\s*\w+'),
        ("identifier", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ("operator", r'(\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%<>=!&|^~?:]+)'),
        ("bracket", r'[{}\[\]()]'),
        ("semicolon", r';'),
        ("comma", r','),
        ("whitespace", r'\s+'),
    ]
    
    def tokenize(self, code: str) -> List[CToken]:
        """Tokenize C code"""
        tokens = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines):
            col = 0
            while col < len(line):
                matched = False
                for token_type, pattern in self.TOKEN_PATTERNS:
                    regex = re.compile(pattern)
                    match = regex.match(line, col)
                    if match:
                        value = match.group(0)
                        if token_type != "whitespace":
                            tokens.append(CToken(token_type, value, line_num, col))
                        col = match.end()
                        matched = True
                        break
                
                if not matched:
                    col += 1
        
        return tokens

# ============================================================================
# SYMBOL TABLE & ANALYSIS
# ============================================================================

@dataclass
class CVariable:
    """C variable"""
    name: str
    data_type: str
    is_pointer: bool = False
    is_array: bool = False
    array_size: int = 0
    scope: str = "global"
    line: int = 0

@dataclass
class CFunction:
    """C function"""
    name: str
    return_type: str
    parameters: List[CVariable] = field(default_factory=list)
    line: int = 0
    is_defined: bool = False

class CSymbolTable:
    """Symbol table for C code"""
    
    def __init__(self):
        self.variables: Dict[str, CVariable] = {}
        self.functions: Dict[str, CFunction] = {}
        
    def add_variable(self, var: CVariable):
        """Add variable to table"""
        self.variables[var.name] = var
    
    def add_function(self, func: CFunction):
        """Add function to table"""
        self.functions[func.name] = func
    
    def get_variable(self, name: str) -> Optional[CVariable]:
        return self.variables.get(name)
    
    def get_function(self, name: str) -> Optional[CFunction]:
        return self.functions.get(name)

# ============================================================================
# C EDITOR
# ============================================================================

class CEditor:
    """C language IDE"""
    
    def __init__(self):
        self.filename = ""
        self.code = ""
        self.tokens: List[CToken] = []
        self.lexer = CLexer()
        self.symbol_table = CSymbolTable()
        self.errors: List[Tuple[int, str]] = []
        self.warnings: List[Tuple[int, str]] = []
        self.breakpoints: Set[int] = set()
        self.watch_variables: Set[str] = set()
        
    def open_file(self, filename: str, code: str = ""):
        """Open/create file"""
        self.filename = filename
        self.code = code
        print(f"📄 Opened: {filename}")
    
    def analyze_syntax(self) -> bool:
        """Analyze C syntax"""
        self.errors.clear()
        self.warnings.clear()
        self.tokens = self.lexer.tokenize(self.code)
        
        # Check for matching brackets
        bracket_stack = []
        bracket_pairs = {'(': ')', '[': ']', '{': '}'}
        
        for token in self.tokens:
            if token.type == "bracket":
                if token.value in '({[':
                    bracket_stack.append((token.value, token.line))
                else:
                    if not bracket_stack:
                        self.errors.append((token.line + 1, f"Unmatched closing bracket: {token.value}"))
                    else:
                        open_bracket, _ = bracket_stack.pop()
                        if bracket_pairs[open_bracket] != token.value:
                            self.errors.append((token.line + 1, "Bracket mismatch"))
        
        if bracket_stack:
            for bracket, line in bracket_stack:
                self.errors.append((line + 1, f"Unclosed bracket: {bracket}"))
        
        # Analyze tokens
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            # Check for function calls
            if token.type == "identifier" and i + 1 < len(self.tokens):
                next_token = self.tokens[i + 1]
                if next_token.type == "bracket" and next_token.value == "(":
                    func_name = token.value
                    if func_name in CLanguageDef.STANDARD_FUNCTIONS:
                        # Standard function - OK
                        pass
                    else:
                        # User-defined function
                        if func_name not in self.symbol_table.functions:
                            self.warnings.append((token.line + 1, f"Undefined function: {func_name}"))
            
            # Check for undefined variables
            if token.type == "identifier" and i > 0:
                prev_token = self.tokens[i - 1]
                if prev_token.type != "preproc" and not self._is_declaration_context(i):
                    if token.value not in self.symbol_table.variables:
                        # Might be undefined
                        pass
            
            i += 1
        
        return len(self.errors) == 0
    
    def _is_declaration_context(self, token_index: int) -> bool:
        """Check if token is in declaration context"""
        if token_index == 0:
            return False
        prev_token = self.tokens[token_index - 1]
        return (prev_token.type == "identifier" or 
                prev_token.value in CLanguageDef.KEYWORDS)
    
    def syntax_highlight(self) -> Dict[str, List[str]]:
        """Generate syntax highlighting information"""
        highlighted = {
            "keywords": [],
            "functions": [],
            "strings": [],
            "comments": [],
            "numbers": [],
            "identifiers": [],
            "operators": [],
            "errors": [],
            "warnings": []
        }
        
        for token in self.tokens:
            if token.type == "identifier":
                if token.value in CLanguageDef.KEYWORDS:
                    kw_type = CLanguageDef.KEYWORDS[token.value]
                    highlighted["keywords"].append(f"{token.value} ({kw_type.value})")
                elif token.value in CLanguageDef.STANDARD_FUNCTIONS:
                    highlighted["functions"].append(f"{token.value}() (std lib)")
                else:
                    highlighted["identifiers"].append(f"{token.value} (line {token.line + 1})")
            elif token.type == "string":
                highlighted["strings"].append(f"{token.value[:30]}... (line {token.line + 1})")
            elif token.type in ["comment_line", "comment_block"]:
                highlighted["comments"].append(f"{token.value[:30]}... (line {token.line + 1})")
            elif token.type == "number":
                highlighted["numbers"].append(f"{token.value} (line {token.line + 1})")
            elif token.type == "operator":
                highlighted["operators"].append(f"{token.value}")
        
        for line, error in self.errors:
            highlighted["errors"].append(f"Line {line}: {error}")
        
        for line, warning in self.warnings:
            highlighted["warnings"].append(f"Line {line}: {warning}")
        
        return highlighted
    
    def set_breakpoint(self, line: int):
        """Set breakpoint"""
        self.breakpoints.add(line)
        print(f"🔴 Breakpoint set at line {line}")
    
    def remove_breakpoint(self, line: int):
        """Remove breakpoint"""
        self.breakpoints.discard(line)
        print(f"⚪ Breakpoint removed from line {line}")
    
    def add_watch(self, variable: str):
        """Add variable to watch list"""
        self.watch_variables.add(variable)
        print(f"👁️  Watching: {variable}")
    
    def simulate_compile(self) -> bool:
        """Simulate compilation"""
        print("\n🔨 Compiling...")
        if not self.analyze_syntax():
            print("  ❌ Compilation failed")
            return False
        
        print("  ✅ Compilation successful")
        return True
    
    def get_statistics(self) -> Dict:
        """Get code statistics"""
        lines = self.code.count('\n') + 1
        keywords = sum(1 for t in self.tokens if t.type == "identifier" and t.value in CLanguageDef.KEYWORDS)
        functions = sum(1 for t in self.tokens if t.type == "identifier" and t.value in CLanguageDef.STANDARD_FUNCTIONS)
        comments = sum(1 for t in self.tokens if t.type.startswith("comment"))
        
        return {
            "total_lines": lines,
            "total_tokens": len(self.tokens),
            "keywords": keywords,
            "functions": functions,
            "comments": comments,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
        }

# ============================================================================
# DEMONSTRATION FUNCTION
# ============================================================================

def demonstrate_c_ide():
    """Demonstrate C IDE"""
    print("\n" + "=" * 70)
    print("C LANGUAGE IDE DEMONSTRATION")
    print("=" * 70)
    
    # Create editor
    editor = CEditor()
    
    # Sample C code
    sample_code = """
#include <stdio.h>

// Calculate factorial
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int number = 5;
    printf("Factorial of %d = %d\\n", number, factorial(number));
    
    for (int i = 1; i <= 10; i++) {
        printf("%d ", i);
    }
    printf("\\n");
    
    return 0;
}
"""
    
    editor.open_file("factorial.c", sample_code)
    
    print("\n📋 Code:")
    for i, line in enumerate(sample_code.strip().split('\n'), 1):
        marker = "🔴" if i in [5, 12] else " "
        print(f"  {marker} {i:2d}: {line}")
    
    # Set breakpoints
    editor.set_breakpoint(5)
    editor.set_breakpoint(12)
    
    # Add watches
    editor.add_watch("number")
    editor.add_watch("i")
    
    # Analyze syntax
    print("\n📝 Syntax Analysis:")
    if editor.analyze_syntax():
        print("  ✅ Syntax OK - No errors found")
    
    if editor.warnings:
        print("  ⚠️  Warnings:")
        for line, warning in editor.warnings:
            print(f"     Line {line}: {warning}")
    
    # Syntax highlighting
    print("\n🎨 Syntax Highlighting:")
    highlighted = editor.syntax_highlight()
    for category in ["keywords", "functions", "comments", "strings"]:
        if highlighted[category]:
            print(f"  {category.upper()}:")
            items = highlighted[category]
            for item in items[:3]:
                print(f"    • {item}")
            if len(items) > 3:
                print(f"    ... and {len(items) - 3} more")
    
    # Compile
    if editor.simulate_compile():
        print("\n📊 Code Statistics:")
        stats = editor.get_statistics()
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Show standard functions
    print("\n📚 Standard C Functions Available:")
    for func_name, (ret_type, params, desc) in list(CLanguageDef.STANDARD_FUNCTIONS.items())[:6]:
        param_str = ", ".join(params) if params else "void"
        print(f"  {ret_type} {func_name}({param_str}) - {desc}")
    print(f"  ... and {len(CLanguageDef.STANDARD_FUNCTIONS) - 6} more")
    
    print("\n✅ C IDE demonstration complete!")

if __name__ == "__main__":
    demonstrate_c_ide()
