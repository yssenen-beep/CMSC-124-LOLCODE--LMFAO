import re
from interpreter.tokens import *


def _word(pattern: str) -> re.Pattern:
    return re.compile(rf"(?<![a-zA-Z0-9_]){pattern}\b")


lex_regex = {
    # LITERALS
    TokenType.NUMBAR: re.compile(r"-?[0-9]+\.[0-9]+\b"),
    TokenType.NUMBR: re.compile(r"-?[0-9]+\b"),
    TokenType.YARN: re.compile(r'".*?"'),
    TokenType.TROOF: _word(r"(?:WIN|FAIL)"),
    TokenType.TYPE: _word(r"(?:NUMBR|NUMBAR|YARN|TROOF|NOOB)"),

    # KEYWORDS
    TokenType.AN: _word(r"AN"),
    TokenType.HAI: _word(r"HAI"),
    TokenType.KTHXBYE: _word(r"KTHXBYE"),
    TokenType.WAZZUP: _word(r"WAZZUP"),
    TokenType.BUHBYE: _word(r"BUHBYE"),
    TokenType.BTW: re.compile(r"\bBTW[^\r\n]*"),
    TokenType.OBTW: re.compile(r"\bOBTW[\s\S]*?\bTLDR\b\n"),
    TokenType.TLDR: _word(r"TLDR"),
    TokenType.I_HAS_A: _word(r"I HAS A"),
    TokenType.ITZ: _word(r"ITZ"),
    TokenType.R: _word(r"R"),
    TokenType.SUM_OF: _word(r"SUM OF"),
    TokenType.DIFF_OF: _word(r"DIFF OF"),
    TokenType.PRODUKT_OF: _word(r"PRODUKT OF"),
    TokenType.QUOSHUNT_OF: _word(r"QUOSHUNT OF"),
    TokenType.MOD_OF: _word(r"MOD OF"),
    TokenType.BIGGR_OF: _word(r"BIGGR OF"),
    TokenType.SMALLR_OF: _word(r"SMALLR OF"),
    TokenType.BOTH_OF: _word(r"BOTH OF"),
    TokenType.EITHER_OF: _word(r"EITHER OF"),
    TokenType.WON_OF: _word(r"WON OF"),
    TokenType.NOT: _word(r"NOT"),
    TokenType.ANY_OF: _word(r"ANY OF"),
    TokenType.ALL_OF: _word(r"ALL OF"),
    TokenType.BOTH_SAEM: _word(r"BOTH SAEM"),
    TokenType.DIFFRINT: _word(r"DIFFRINT"),
    TokenType.SMOOSH: _word(r"SMOOSH"),
    TokenType.MAEK: _word(r"MAEK"),
    TokenType.A: _word(r"A"),
    TokenType.IS_NOW_A: _word(r"IS NOW A"),
    TokenType.VISIBLE: _word(r"VISIBLE"),
    TokenType.GIMMEH: _word(r"GIMMEH"),
    TokenType.O_RLY: re.compile(r"\bO RLY\b\??"),
    TokenType.YA_RLY: _word(r"YA RLY"),
    TokenType.MEBBE: _word(r"MEBBE"),
    TokenType.NO_WAI: _word(r"NO WAI"),
    TokenType.OIC: _word(r"OIC"),
    TokenType.WTF: re.compile(r"\bWTF\b\?"),
    TokenType.OMGWTF: _word(r"OMGWTF"),
    TokenType.OMG: _word(r"OMG"),
    TokenType.IM_IN_YR: _word(r"IM IN YR"),
    TokenType.UPPIN: _word(r"UPPIN"),
    TokenType.NERFIN: _word(r"NERFIN"),
    TokenType.YR: _word(r"YR"),
    TokenType.TIL: _word(r"TIL"),
    TokenType.WILE: _word(r"WILE"),
    TokenType.IM_OUTTA_YR: _word(r"IM OUTTA YR"),
    TokenType.HOW_IZ_I: _word(r"HOW IZ I"),
    TokenType.IF_U_SAY_SO: _word(r"IF U SAY SO"),
    TokenType.GTFO: _word(r"GTFO"),
    TokenType.FOUND_YR: _word(r"FOUND YR"),
    TokenType.I_IZ: _word(r"I IZ"),
    TokenType.MKAY: _word(r"MKAY"),

    # SYMBOLS
    TokenType.PLUS: re.compile(r"\+"),

    # IDENTIFIERS
    TokenType.IDENTIFIER: re.compile(r"\b[a-zA-Z][a-zA-Z0-9_]*\b"),

    # WHITESPACE RULE
    TokenType.LINEBREAK: re.compile(r"[\n]+"),
    TokenType.WHITESPACE: re.compile(r"[ \t]+"),
}
