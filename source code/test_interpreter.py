from interpreter.lex_analyzer import lex_le_analyzer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter
def show_text(text):
    print(text, end="")

def ask_user():
    return input("GIMMEH> ")




def run_lol(code):
    
    tokens = lex_le_analyzer(code)
    program = Parser(tokens).parse_program()
    interpreter = Interpreter(show_text, ask_user)
    table = interpreter.run(program)
    return table


code = """HAI
    WAZZUP
        BTW variable dec
        I HAS A monde
        I HAS A num ITZ 17
        I HAS A name ITZ "seventeen"
        I HAS A fnum ITZ 17.0
        I HAS A flag ITZ WIN
        
        I HAS A sum ITZ SUM OF num AN 13
        I HAS A diff ITZ DIFF OF sum AN 17
        I HAS A prod ITZ PRODUKT OF 3 AN 4
        I HAS A quo ITZ QUOSHUNT OF 4 AN 5
    BUHBYE

    BTW print literals and variables
    VISIBLE "declarations"
    VISIBLE monde BTW should be NOOB
    VISIBLE num
    VISIBLE name
    VISIBLE fnum
    VISIBLE flag

    VISIBLE sum
    VISIBLE diff
    VISIBLE prod
    VISIBLE quo

    BTW print expressions
    VISIBLE SUM OF PRODUKT OF 3 AN 5 AN BIGGR OF DIFF OF 17 AN 2 AN 5
    VISIBLE BIGGR OF PRODUKT OF 11 AN 2 AN QUOSHUNT OF SUM OF 3 AN 5 AN 2
KTHXBYE

"""

table = run_lol(code)
for name in table.variables:
    value = table.variables[name]
    print(name, value.type, value.value)