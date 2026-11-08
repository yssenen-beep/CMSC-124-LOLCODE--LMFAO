from interpreter.lex_analyzer import lex_le_analyzer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter


def run_lol(code):
    
    tokens = lex_le_analyzer(code)
    program = Parser(tokens).parse_program()
    interpreter = Interpreter()
    table = interpreter.run(program)
    return table


code = """HAI
WAZZUP
I HAS A x ITZ 17
I HAS A y ITZ "hello"
I HAS A z
I HAS A copy ITZ x
BUHBYE
z R WIN
KTHXBYE
"""

table = run_lol(code)
for name in table.variables:
    value = table.variables[name]
    print(name, value.type, value.value)