#This will contain all the AST node objects needed for the file.
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

NODE_CLASSIFICATIONS = {
    # program structure
    "PROGRAM": "Program Block",
    "VARIABLE_SECTION": "Variable Declaration Section",
    "FUNCTION_SECTION": "Function Declaration Section",
    # variables
    "DECLARATION": "Variable Declaration",
    "ASSIGNMENT": "Variable Assignment",
    "RECAST": "Variable Recast",
    # statements
    "STATEMENT_BLOCK": "Statement Block",
    "PRINT": "Output Statement",
    "INPUT": "Input Statement",
    "GTFO": "Break / Return (no value)",
    # expressions
    "LITERAL": "Literal Value",
    "IDENTIFIER": "Identifier",
    "ARITHMETIC": "Arithmetic Expression",
    "COMPARISON": "Comparison Expression",
    "BOOLEAN_EXPRESSION": "Boolean Expression",
    "CONCATENATION": "Concatenation Expression",
    "TYPECAST": "Typecast Expression",
    "EXPRESSION": "Expression",
    # control flow
    "IF_ELSE": "If-Else Statement",
    "ELSE_IF": "Else-If Branch",
    "ELSE": "Else Branch",
    "SWITCH_CASE": "Switch-Case Statement",
    "CASE": "Switch Case",
    "DEFAULT_CASE": "Switch Default Case",
    "LOOP": "Loop Statement",
    "LOOP_OP": "Loop Operation",
    "LOOP_CONDITION": "Loop Condition",
    # functions
    "FUNCTION_DECLARATION": "Function Definition",
    "FUNCTION_CALL": "Function Call",
    "PARAMETER": "Function Parameter",
    "RETURN": "Function Return",
}

class ASTType(Enum):
    #PROGRAM STRUCTURE
    PROGRAM = auto()
    VARIABLE_SECTION = auto()
    FUNCTION_SECTION = auto()

    #VARIABLES
    DECLARATION = auto()
    ASSIGNMENT = auto()
    RECAST = auto()

    #STATEMENTS
    STATEMENT_BLOCK = auto()
    PRINT = auto()
    INPUT = auto()
    GTFO = auto()

    #EXPRESSIONS
    LITERAL = auto()
    IDENTIFIER = auto()
    ARITHMETIC = auto()
    COMPARISON = auto()
    BOOLEAN_EXPRESSION = auto()
    CONCATENATION = auto()
    TYPECAST = auto()
    EXPRESSION = auto()

    #CONTROL FLOW
    IF_ELSE = auto()
    ELSE_IF = auto()
    ELSE = auto()
    SWITCH_CASE = auto()
    CASE = auto()
    DEFAULT_CASE = auto()
    LOOP = auto()
    LOOP_OP = auto()
    LOOP_CONDITION = auto()

    #FUNCTIONS
    FUNCTION_DECLARATION = auto()
    FUNCTION_CALL = auto()
    PARAMETER = auto()
    RETURN = auto()

    @property
    def classification(self) -> str:
        return NODE_CLASSIFICATIONS.get(self.name, self.name.replace("_", " ").title())

@dataclass
class ASTNode:
    type: ASTType
    value: object = None
    children: list["ASTNode"] = field(default_factory=list)
