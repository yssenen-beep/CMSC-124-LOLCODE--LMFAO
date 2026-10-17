from lexemes import *
import re

tokens = [] # store tuple (lexeme/text extract, lexeme type)

with open("test_cases/test.lol", "r", encoding="utf-8") as file:
    content = file.read()
    index = 0 # track/point to where to start regexing from the string
    while index < len(content):
        match = None
        for token_type, regex in lex_regex.items(): # grep all possible lexeme types
            match = regex.match(content, index)
            if match:
                lex = match.group(0)
                index = match.end() # go to end of the match and start reading the text after the match
                if  token_type == TokenType.WHITESPACE: # if whitespace go next
                    break
                tokens.append(Token(value=lex, type=token_type)) # tuple (lexeme/text extract, lexeme type)
                break
        if not match:
            print("bruh")
            break

for token in tokens:
    print("Lexeme:", token.value, "- Type:", token.type)
    
