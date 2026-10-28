#This will contain all the tokens objects needed for the file.
from enum import Enum, auto

from dataclasses import dataclass

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

@dataclass
class Token:
    value: str
    type: TokenType
