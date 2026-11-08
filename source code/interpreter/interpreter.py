from interpreter.ast_nodes import ASTType
from interpreter.tokens import TokenType
from interpreter.symbol_table import SymbolTable
from interpreter.values import MK_NOOB, MK_NUMBR, MK_NUMBAR, MK_YARN, MK_TROOF


class Interpreter:
    
    def __init__(self,):
        self.symbol_table = SymbolTable()

    def run(self, program):
        self.evaluate(program, self.symbol_table)
        return self.symbol_table

    def evaluate(self, node, symbol_table):
        
        #Program structure
        if node.type == ASTType.PROGRAM:
            return self.eval_program(node,symbol_table)
        elif node.type == ASTType.VARIABLE_SECTION:
            return self.eval_variable_section(node, symbol_table)
        elif node.type == ASTType.FUNCTION_SECTION:
            return self.eval_function_section(node, symbol_table)
        
        #Variables
        elif node.type == ASTType.DECLARATION:
            return self.eval_declaration(node, symbol_table)
        elif node.type == ASTType.ASSIGNMENT:
            return self.eval_assignment(node, symbol_table)

        #Statements
        elif node.type == ASTType.STATEMENT_BLOCK:
            return self.eval_block(node, symbol_table)
        
        #Expressions
        elif node.type == ASTType.LITERAL:
            return self.eval_literal(node, symbol_table)
        elif node.type == ASTType.IDENTIFIER:
            return self.eval_identifier(node, symbol_table)

        else:
            raise Exception(f"Unknown AST node type: {node.type}")

        
    #------------------------------------------------
    #PROGRAM STRUCTURE SECTION 
    #------------------------------------------------
    
    def eval_program(self, program, symbol_table):
        #parser returns a node with children=[func_ast, var_ast, code_ast]
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
    #STATEMENTS SECTION 
    #------------------------------------------------
    def eval_block(self, block, table):
        return self.eval_statements(block.children, table)

    def eval_statements(self, statements, table):
        for statement in statements:
            self.evaluate(statement, table)
        return None
   
    #------------------------------------------------
    #EXPRESSIONS SECTION 
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
        
    #Gets a current value of a variable from the symbol table.
    def eval_identifier(self, node, table):
        if node.value == "IT":
            return table.get_it()
        return table.get_variable(node.value)
    