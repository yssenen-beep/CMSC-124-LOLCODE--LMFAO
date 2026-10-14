from lexemes import lex_regex
import re

tokens = [] # store tuple (lexeme/text extract, lexeme type)

with open("test.lol", "r", encoding="utf-8") as file:
    content = file.read()
    index = 0 # track/point to where to start regexing from the string
    while index < len(content):
        match = None
        for lex_type, regex in lex_regex.items(): # grep all possible lexeme types
            match = regex.match(content, index)
            if match:
                lex = match.group(0)
                index = match.end() # go to end of the match and start reading the text after the match
                if lex_type == "WHITESPACE": # if whitespace go next
                    break
                tokens.append((lex, lex_type)) # tuple (lexeme/text extract, lexeme type)
                break
        if not match:
            print("bruh")
            break

for token in tokens:
    print("Lexeme:", token[0], "- Type:", token[1])
    
