from interpreter.ast_nodes import ASTType
from interpreter.tokens import TokenType
from interpreter.symbol_table import SymbolTable
from interpreter.values import MK_NOOB, MK_NUMBR, MK_NUMBAR, MK_YARN, MK_TROOF
from interpreter import typecast 

class Interpreter:
    
    def __init__(self,output_func,input_func):
        self.output = output_func
        self.input = input_func
        self.symbol_table = SymbolTable()

    def run(self, program):
        self.evaluate(program, self.symbol_table)
        return self.symbol_table

    def evaluate(self, node, symbol_table):
        
        # Program structure
        if node.type == ASTType.PROGRAM:
            return self.eval_program(node,symbol_table)
        elif node.type == ASTType.VARIABLE_SECTION:
            return self.eval_variable_section(node, symbol_table)
        elif node.type == ASTType.FUNCTION_SECTION:
            return self.eval_function_section(node, symbol_table)
        
        # Variables
        elif node.type == ASTType.DECLARATION:
            return self.eval_declaration(node, symbol_table)
        elif node.type == ASTType.ASSIGNMENT:
            return self.eval_assignment(node, symbol_table)

        # Statements
        elif node.type == ASTType.STATEMENT_BLOCK:
            return self.eval_block(node, symbol_table)
        elif node.type == ASTType.PRINT:
            return self.eval_print(node, symbol_table)
        elif node.type == ASTType.INPUT:
            return self.eval_input(node, symbol_table)
        
        # Expressions
        elif node.type == ASTType.LITERAL:
            return self.eval_literal(node, symbol_table)
        elif node.type == ASTType.IDENTIFIER:
            return self.eval_identifier(node, symbol_table)
        elif node.type == ASTType.ARITHMETIC:
            return self.eval_arithmetic(node, symbol_table)

        else:
            raise Exception(f"Unknown AST node type: {node.type}")

        
    #------------------------------------------------
    #PROGRAM STRUCTURE SECTION 
    #------------------------------------------------
    
    def eval_program(self, program, symbol_table):
        # parser returns a node with children=[func_ast, var_ast, code_ast]
        function_section = program.children[0]
        variable_section = program.children[1]
        main_statements = program.children[2] 

        self.evaluate(function_section, symbol_table)      
        self.evaluate(variable_section, symbol_table)    

        result = self.eval_statements(main_statements, symbol_table)

        return None
    
    def eval_function_section(self, node, table):
        for function_node in node.children:
            self.evaluate(function_node, table)
        return None
    
    def eval_variable_section(self, node, table):
        for declaration in node.children:
            self.evaluate(declaration, table)
        return None

    #------------------------------------------------
    # VARIABLES SECTION
    #------------------------------------------------

    def eval_declaration(self, node, table):
        # if node.children is empty(Unitialized value:Ex. I HAS A name)
        if len(node.children) == 0:
            value = MK_NOOB()
        else:
            value = self.evaluate(node.children[0], table)
        
        table.declare_variable(node.value, value)
        return None
    
    def eval_assignment(self, node, table):
        value = self.evaluate(node.children[0], table)
        table.set_variable(node.value, value)
        return None
    
    def eval_recast(self, node, table):
        return None



    #------------------------------------------------
    # STATEMENTS SECTION 
    #------------------------------------------------
    def eval_block(self, block, table):
        return self.eval_statements(block.children, table)

    # Run statements one by one
    def eval_statements(self, statements, table):
        for statement in statements:
            self.evaluate(statement, table)
        return None
    
    # VISIBLE a + b + c + ... :
    # Casts all operands into yarn, and concatenates them into a single string, 
    # then prints the string to the console.
    def eval_print(self, node, table):
        text = ""
        for child in node.children:
            value = self.evaluate(child, table)
 
            if value.type == "NOOB":
                text = text + "NOOB"     
            else:
                text = text + typecast.to_yarn(value).value
 
        self.output(text + "\n")
        return None
    
    # GIMMEH:
    # Reads a line of input from the console, 
    # and assigns it to the variable of the GIMMEH statement.
    def eval_input(self, node, table):
        text = self.input()
        table.set_variable(node.value, MK_YARN(text))
        return None
    #------------------------------------------------
    # EXPRESSIONS SECTION 
    #------------------------------------------------
    
    # Evaluates a literal node and returns an object that has the type and value of the literal(see values.py). 
    def eval_literal(self, node, table):
        text = node.value
        if text.startswith('"'):
            return MK_YARN(text[1:-1]) #remove the quotes
        elif text == "WIN":
            return MK_TROOF(True)
        elif text == "FAIL":
            return MK_TROOF(False)
        elif "." in text:
            return MK_NUMBAR(float(text))
        else:
            return MK_NUMBR(int(text))
        
    # Gets a current value of a variable from the symbol table.
    def eval_identifier(self, node, table):
        if node.value == "IT":
            return table.get_it()
        return table.get_variable(node.value)
    
    # SUM OF, DIFF OF, PRODUKT OF, QUOSHUNT OF, MOD OF, BIGGR OF, SMALLR OF:
    # values will be typecasted to a NUMBR or NUMBAR, if type is already NUMBR or NUMBAR, it will be used as is.
    def eval_arithmetic(self, node, table):
       
        left = typecast.to_numeric(self.evaluate(node.children[0], table))
        right = typecast.to_numeric(self.evaluate(node.children[1], table))
        a = left.value
        b = right.value
        op = node.value
 
        # Division by zero check for QUOSHUNT OF and MOD OF
        if op == TokenType.QUOSHUNT_OF and b == 0:
            raise Exception("Division by zero.")
        if op == TokenType.MOD_OF and b == 0:
            raise Exception("Division by zero.")

        # Check if both operands are NUMBRs or if at least one is a NUMBAR
        if left.type == "NUMBR" and right.type == "NUMBR":
            both_numbr = True
        else:
            both_numbr = False

        if op == TokenType.SUM_OF:
            result = a + b
        elif op == TokenType.DIFF_OF:
            result = a - b
        elif op == TokenType.PRODUKT_OF:
            result = a * b
        elif op == TokenType.QUOSHUNT_OF:
            if both_numbr:
                result = int(a / b)      
            else:
                result = a / b
        elif op == TokenType.MOD_OF:
            result = a % b
        elif op == TokenType.BIGGR_OF:
            if a > b:
                result = a
            else:
                result = b
        else:  
            if a < b:
                result = a
            else:
                result = b
 
        # If both operands evaluate to a NUMBR, the result of the operation is a NUMBR.
        # If at least one operand is a NUMBAR, the result of the operation is a NUMBAR.
        if both_numbr:
            return MK_NUMBR(result)
        return MK_NUMBAR(result)