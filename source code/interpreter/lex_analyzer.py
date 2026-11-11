import re
from interpreter.tokens import Token, TokenType
from interpreter.lexemes import lex_regex

def lex_le_analyzer(content: str): # upd: made to dynamically handle every content
    tokens = [] # store tuple (lexeme/text extract, lexeme type)
    index = 0 # track/point to where to start regexing from the string
    error = None

    while index < len(content) and error == None:
        foundmatch = False
        for token_type, regex in lex_regex.items(): # grep all possible lexeme types
            match = regex.match(content, index)
            if match and match.end() > index:
                foundmatch = True
                lex = match.group(0)
                index = match.end() # go to end of the match and start reading the text after the match                
                if token_type == TokenType.WHITESPACE: # if whitespace go next
                    break                    

                # if token_type == TokenType.OBTW:
                #     lines = lex.strip().split("\n")
                    
                # # TLDR no OBTW or OBTW no TLDR
                # elif token_type == TokenType.TLDR or (token_type == TokenType.IDENTIFIER and lex == "OBTW"):
                #     error = True

                tok = Token(value=lex, type=token_type)
                tokens.append(tok)
                break
        # no match, so it is unknown text
        if foundmatch == False:
            error = True

    if error == True:
        tokens.append(Token(value="SYNTAX ERROR", type=None))

    tokens.append(Token(value="EOF", type=TokenType.EOF))
    return tokens
