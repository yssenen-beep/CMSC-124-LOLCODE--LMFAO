#This will contain all the tokens objects needed for the file.
from enum import Enum, auto

from dataclasses import dataclass

TOKEN_CLASSIFICATIONS = {
    # literals
    "NUMBAR": "Float Literal",
    "NUMBR": "Integer Literal",
    "YARN": "String Literal",
    "TROOF": "Boolean Literal",
    "TYPE": "Type Literal",
    # delimiters
    "HAI": "Program Start",
    "KTHXBYE": "Program End",
    "WAZZUP": "Variable Block Start",
    "BUHBYE": "Variable Block End",
    "BTW": "Single-Line Comment",
    "OBTW": "Multi-Line Comment",
    # variables
    "I_HAS_A": "Variable Declaration",
    "ITZ": "Variable Initialization",
    "R": "Variable Assignment",
    "MAEK": "Typecast Operator",
    "A": "Typecast Connector",
    "IS_NOW_A": "Recast Operator",
    # operators
    "SUM_OF": "Arithmetic Operator",
    "DIFF_OF": "Arithmetic Operator",
    "PRODUKT_OF": "Arithmetic Operator",
    "QUOSHUNT_OF": "Arithmetic Operator",
    "MOD_OF": "Arithmetic Operator",
    "BIGGR_OF": "Arithmetic Operator",
    "SMALLR_OF": "Arithmetic Operator",
    "SMOOSH": "Concatenation Operator",
    # bool operators
    "BOTH_OF": "Boolean Operator",
    "EITHER_OF": "Boolean Operator",
    "WON_OF": "Boolean Operator",
    "NOT": "Boolean Operator",
    "ANY_OF": "Infinite Boolean Operator",
    "ALL_OF": "Infinite Boolean Operator",
    "BOTH_SAEM": "Boolean Operator",
    "DIFFRINT": "Boolean Operator",
    "AN": "Operand Separator",
    "MKAY": "Expression Delimiter",
    # input output
    "VISIBLE": "Output Keyword",
    "GIMMEH": "Input Keyword",
    # conditional statements
    "O_RLY": "If-Else Start",
    "YA_RLY": "If Branch",
    "MEBBE": "Else-If Branch",
    "NO_WAI": "Else Branch",
    "WTF": "Switch Start",
    "OMG": "Switch Case",
    "OMGWTF": "Switch Default Case",
    "OIC": "Block End",
    # loops
    "IM_IN_YR": "Loop Start",
    "UPPIN": "Increment Operation",
    "NERFIN": "Decrement Operation",
    "YR": "Parameter",
    "TIL": "Until Condition",
    "WILE": "While Condition",
    "IM_OUTTA_YR": "Loop End",
    # functions
    "HOW_IZ_I": "Function Definition Start",
    "IF_U_SAY_SO": "Function Definition End",
    "FOUND_YR": "Function Return",
    "I_IZ": "Function Call",
    "GTFO": "Function Return (no return)",
    # misc
    "IDENTIFIER": "Identifier",
    "PLUS": "Print Concatenation Symbol",
    "LINEBREAK": "Line Break",
    "WHITESPACE": "Whitespace",
    "EOF": "End of File",
}

class TokenType(Enum):
    #LITERALS
    NUMBAR = auto()
    NUMBR = auto()
    YARN = auto()
    TROOF = auto()
    TYPE = auto()

    #KEYWORDS
    AN = auto()
    HAI = auto()
    KTHXBYE = auto()
    WAZZUP = auto()
    BUHBYE = auto()
    BTW = auto()
    OBTW = auto()
    TLDR = auto()
    I_HAS_A = auto()
    ITZ = auto()
    R = auto()
    SUM_OF = auto()
    DIFF_OF = auto()
    PRODUKT_OF = auto()
    QUOSHUNT_OF = auto()
    MOD_OF = auto()
    BIGGR_OF = auto()
    SMALLR_OF = auto()
    BOTH_OF = auto()
    EITHER_OF = auto()
    WON_OF = auto()
    NOT = auto()
    ANY_OF = auto()
    ALL_OF = auto()
    BOTH_SAEM = auto()
    DIFFRINT = auto()
    SMOOSH = auto()
    MAEK = auto()
    A = auto()
    IS_NOW_A = auto()
    VISIBLE = auto()
    GIMMEH = auto()
    O_RLY = auto()
    YA_RLY = auto()
    MEBBE = auto()
    NO_WAI = auto()
    OIC = auto()
    WTF = auto()
    OMG = auto()
    OMGWTF = auto()
    IM_IN_YR = auto()
    UPPIN = auto()
    NERFIN = auto()
    YR = auto()
    TIL = auto()
    WILE = auto()
    IM_OUTTA_YR = auto()
    HOW_IZ_I = auto()
    IF_U_SAY_SO = auto()
    GTFO = auto()
    FOUND_YR = auto()
    I_IZ = auto()
    MKAY = auto()

    #IDENTIFIERS
    IDENTIFIER= auto()

    #WHITESPACE RULE
    LINEBREAK = auto()
    WHITESPACE = auto()

    #SYMBOLS
    PLUS = auto()
    
    EOF = auto()
    
    @property
    def classification(self) -> str:
        return TOKEN_CLASSIFICATIONS.get(self.name, self.name.replace("_", " ").title())

@dataclass
class Token:
    value: str
    type: TokenType
