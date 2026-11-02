from dataclasses import dataclass
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

    # Control Flow
    IF_ELSE = auto()
    ELSE_IF = auto()
    ELSE = auto()
    SWITCH_CASE = auto()
    CASE = auto()
    DEFAULT_CASE = auto()
    LOOP = auto()

    # Functions
    FUNCTION_DECLARATION = auto()
    FUNCTION_CALL = auto()
    PARAMETER = auto()
    RETURN = auto()

@dataclass
class ASTNode:
    type: ASTType
    value: Optional[object] = None
    children: Optional[list] = None


