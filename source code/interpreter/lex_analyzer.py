import re
from interpreter.tokens import Token, TokenType
from interpreter.lexemes import lex_regex

def lex_le_analyzer(content: str): # upd: made to dynamically handle every content
    tokens = [] # store tuple (lexeme/text extract, lexeme type)
    index = 0 # track/point to where to start regexing from the string
    line_tokens = []

    while index < len(content):
        match = None
        for token_type, regex in lex_regex.items(): # grep all possible lexeme types
            match = regex.match(content, index)
            if match and match.end() > index:
                lex = match.group(0)
                index = match.end() # go to end of the match and start reading the text after the match                
                if token_type == TokenType.WHITESPACE: # if whitespace go next
                    break                    

                tok = Token(value=lex, type=token_type)
                
                # Check if a line is valid
                if token_type == TokenType.LINEBREAK:
                    validate_multilines(line_tokens)
                    line_tokens = []
                else:
                    line_tokens.append(tok)

                tokens.append(tok)
                break
                
        if not match:
            tokens.append(Token(value="SYNTAX ERROR", type=None))
            break
    if line_tokens:
        validate_multilines(line_tokens)

    tokens.append(Token(value="EOF", type=TokenType.EOF))
    return tokens

def validate_multilines(line_tokens):
    # check if OBTW and TLDR in their own lines (!)

    return None