import re
from interpreter.tokens import Token, TokenType
from interpreter.lexemes import lex_regex

def lex_le_analyzer(content: str): # upd: made to dynamically handle every content
    tokens = [] # store tuple (lexeme/text extract, lexeme type)
    index = 0 # track/point to where to start regexing from the string
    
    while index < len(content):
        match = None
        for token_type, regex in lex_regex.items(): # grep all possible lexeme types
            match = regex.match(content, index)
            if match and match.end() > index:
                lex = match.group(0)
                index = match.end() # go to end of the match and start reading the text after the match                
                if token_type == TokenType.WHITESPACE: # if whitespace go next
                    break                    
                tokens.append(Token(value=lex, type=token_type)) # tuple (lexeme/text extract, lexeme type)
                break
                
        if not match:
            tokens.append(Token(value="SYNTAX ERROR", type=None))
            break
    tokens.append(Token(value="EOF", type=TokenType.EOF))
    return tokens
