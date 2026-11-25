from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

class ASTType(Enum):

    #Program structure
    PROGRAM = auto()
    VARIABLE_SECTION = auto()
    FUNCTION_SECTION = auto()

    # Variables
    DECLARATION = auto()
    ASSIGNMENT = auto()
    RECAST = auto()

    # Statements
    STATEMENT_BLOCK = auto()
    PRINT = auto()
    INPUT = auto()
    GTFO = auto()

    # Expressions
    LITERAL = auto()
    IDENTIFIER = auto()
    ARITHMETIC = auto()
    COMPARISON = auto()
    BOOLEAN_EXPRESSION = auto()
    CONCATENATION = auto()
    TYPECAST = auto()
    EXPRESSION = auto()

    # Control Flow
    IF_ELSE = auto()
    ELSE_IF = auto()
    ELSE = auto()
    SWITCH_CASE = auto()
    CASE = auto()
    DEFAULT_CASE = auto()
    LOOP = auto()
    LOOP_OP = auto()
    LOOP_CONDITION = auto()

    # Functions
    FUNCTION_DECLARATION = auto()
    FUNCTION_CALL = auto()
    PARAMETER = auto()
    RETURN = auto()

NODE_CLASSIFICATIONS = {
    # Program structure
    "PROGRAM": "Represents the entire program block",
    "VARIABLE_SECTION": "Holds variable declarations",
    "FUNCTION_SECTION": "Holds function declarations",

    # Variables
    "DECLARATION": "Declares a variable to the symbol table",
    "ASSIGNMENT": "Assigns a value to a variable",
    "RECAST": "Recasts a variable to a different type",

    # Statements
    "STATEMENT_BLOCK": "Holds a sequence of statements",
    "PRINT": "Outputs one or more expressions to the console",
    "INPUT": "Reads user input from terminal into a variable",
    "GTFO": "Breaks out of a loop, switch-case, or function",

    # Expressions
    "LITERAL": "A datatype basically",
    "IDENTIFIER": "A reference to a variable by name",
    "ARITHMETIC": "Performs an arithmetic operation on two operands",
    "COMPARISON": "Compares two operands and yields a TROOF",
    "BOOLEAN_EXPRESSION": "Performs a boolean operation and output TROOF",
    "CONCATENATION": "Joins multiple operands into one YARN",
    "TYPECAST": "Converts an expression to a different type",
    "EXPRESSION": "A generic expression wrapper node",

    # Control flow
    "IF_ELSE": "Conditional block (O RLY? YA RLY ... NO WAI ... OIC)",
    "ELSE_IF": "Additional conditional branch (MEBBE)",
    "ELSE": "Fallback branch when the condition is false (NO WAI)",
    "SWITCH_CASE": "Multi-way branch on the value of IT (WTF? ... OIC)",
    "CASE": "A single case in a switch-case (OMG)",
    "DEFAULT_CASE": "Fallback case in a switch-case (OMGWTF)",
    "LOOP": "Loop block (IM IN YR ... IM OUTTA YR)",
    "LOOP_OP": "Loop update operation",
    "LOOP_CONDITION": "Loop continuation condition",

    # Functions
    "FUNCTION_DECLARATION": "Defines a function",
    "FUNCTION_CALL": "Calls a function (I IZ)",
    "PARAMETER": "A named parameter of a function (YR)",
    "RETURN": "Returns a value from a function (FOUND YR)",
}

@dataclass
class ASTNode:
    type: ASTType
    value: object = None
    children: list["ASTNode"] = field(default_factory=list)
