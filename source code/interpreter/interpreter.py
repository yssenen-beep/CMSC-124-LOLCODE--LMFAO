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
        self.functions = {} # stores function definitions {func_name : ASTNode}

    def run(self, program):
        self.evaluate(program, self.symbol_table)
        return self.symbol_table

    def evaluate(self, node, symbol_table):
        if node == None: # if empty
            return None
        
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
        elif node.type == ASTType.TYPECAST: # typecasting
            return self.eval_typecast(node, symbol_table)

        # Statements
        elif node.type == ASTType.STATEMENT_BLOCK:
            return self.eval_block(node, symbol_table)
        elif node.type == ASTType.PRINT:
            return self.eval_print(node, symbol_table)
        elif node.type == ASTType.INPUT:
            return self.eval_input(node, symbol_table)
        elif node.type == ASTType.EXPRESSION: # added expressions
            val = self.evaluate(node.children[0], symbol_table)
            if val:
                symbol_table.set_it(val)
            return val
        elif node.type == ASTType.GTFO: # added GTFO
            return "GTFO"
        
        # Expressions
        elif node.type == ASTType.LITERAL:
            return self.eval_literal(node, symbol_table)
        elif node.type == ASTType.IDENTIFIER:
            return self.eval_identifier(node, symbol_table)
        elif node.type == ASTType.ARITHMETIC:
            return self.eval_arithmetic(node, symbol_table)
        # added more expressions
        elif node.type == ASTType.CONCATENATION:
            return self.eval_concatenation(node, symbol_table)
        elif node.type == ASTType.BOOLEAN_EXPRESSION:
            return self.eval_boolean(node, symbol_table)
        elif node.type == ASTType.COMPARISON:
            return self.eval_comparison(node, symbol_table)

        # Control flow
        elif node.type == ASTType.IF_ELSE:
            return self.eval_if_else(node, symbol_table)
        elif node.type == ASTType.ELSE_IF:
            return self.eval_else_if(node, symbol_table)
        elif node.type == ASTType.ELSE:
            return self.eval_else(node, symbol_table)
        elif node.type == ASTType.SWITCH_CASE:
            return self.eval_switch_case(node, symbol_table)
        elif node.type == ASTType.LOOP:
            return self.eval_loop(node, symbol_table)

        # Functions
        elif node.type == ASTType.FUNCTION_DECLARATION:
            return self.eval_func_decl(node, symbol_table)
        elif node.type == ASTType.FUNCTION_CALL:
            return self.eval_func_call(node, symbol_table)
        elif node.type == ASTType.RETURN:
            return self.eval_return(node, symbol_table)

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

        self.eval_statements(main_statements.children, symbol_table) # point to children list

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
    
    def eval_typecast(self, node, table): # typecasting AND recasting
        # MAEK <expr> A <type> (typecasting)
        if len(node.children) == 2:
            val = self.evaluate(node.children[0], table)
            type = node.children[1].value
            res = typecast.cast(val, type)
            return res
        # <IDENTIFIER> IS NOW A <type> (recasting)
        else:
            var_name = node.value
            type = node.children[0].value
            var_val = table.get_variable(var_name)
            var_val2 = typecast.cast(var_val, type)
            table.set_variable(var_name, var_val2)
            return None

    #------------------------------------------------
    # STATEMENTS SECTION 
    #------------------------------------------------
    def eval_block(self, block, table):
        return self.eval_statements(block.children, table)

    # Run statements one by one
    def eval_statements(self, statements, table):
        for statement in statements:
            result = self.evaluate(statement, table)
            if result == "GTFO" or result == "RETURN": # terminates loop/switch
                return "GTFO"
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
        text = self.input(node.value)
        val = MK_YARN(text)
        table.set_variable(node.value, val)
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
            res_val = MK_NUMBR(result)
        else:
            res_val = MK_NUMBAR(result)
        return res_val

    # more evaluations
    # Evaluates equality and inequality
    def eval_comparison(self, node, table):
        left = self.evaluate(node.children[0], table)
        right = self.evaluate(node.children[1], table)
        op = node.value

        if op == TokenType.BOTH_SAEM:
            res = (left.value == right.value)
        elif op == TokenType.DIFFRINT:
            res = (left.value != right.value)
        else:
            res = False

        res_val = MK_TROOF(res)
        return res_val

     # BOTH OF, EITHER OF, WON OF, NOT, ALL OF, ANY OF
    # If the operands are not TROOFs, they should be implicitly typecast
    def eval_boolean(self, node, table):

        # Turn every operand into a TROOF and store them into a list
        values = []
        for child in node.children:
            value = self.evaluate(child, table)
            values.append(typecast.to_troof(value).value)

        op = node.value

        # NOT(1 operand)
        if op == TokenType.NOT:
            result = not values[0]

        # BOTH OF(2 operands), EITHER OF(2 operands), WON OF(2 operands)
        elif op == TokenType.BOTH_OF:          
            result = values[0] and values[1]
        elif op == TokenType.EITHER_OF:        
            result = values[0] or values[1]
        elif op == TokenType.WON_OF:           
            result = values[0] != values[1]

        # ALL OF(infinite operands), ANY OF(infinite operands)
        elif op == TokenType.ALL_OF:
            result = all(values)
        elif op == TokenType.ANY_OF:
            result = any(values)
        else:
            result = False

        res_val = MK_TROOF(result)
        return res_val

    # SMOOSH a AN b AN c
    # If the operand evaluates to another data type, they are implicitly typecast 
    # to YARNs when given to SMOOSH
    def eval_concatenation(self, node, table):
        text = ""
        for child in node.children:
            value = self.evaluate(child, table)
            text = text + typecast.to_yarn(value, True).value

        res_val = MK_YARN(text)
        return res_val

    # ------------------------------------------------
    # CONTROL FLOW SECTION
    # ------------------------------------------------

    # IF-THEN STATEMENTS
    def eval_if_else(self, node, table):
        # node.children is [condition, YA RLY block, optional ELSE_IF or ELSE]
        condition_expr = node.children[0]
        ya_rly_block = node.children[1]

        # the condition expression's result is stored in IT
        value = self.evaluate(condition_expr, table)

        # If the IT variable can be cast to WIN, the if-clause executes. Otherwise, the else-clause executes.
        if typecast.to_troof(value).value == True:
            return self.eval_block(ya_rly_block, table)

        # If the if-clause is not executed, and there is an else-clause, it executes the else-clause or else-if clause.
        if len(node.children) == 3:
            return self.evaluate(node.children[2], table)

        return None

    # MEBBE 
    def eval_else_if(self, node, table):
        condition_expr = node.children[0]
        block = node.children[1]

        value = self.evaluate(condition_expr, table)

        if typecast.to_troof(value).value == True:
            return self.eval_block(block, table)

        if len(node.children) == 3:
            return self.evaluate(node.children[2], table)

        return None

    # NO WAI
    def eval_else(self, node, table):
        # node.children is [block]
        return self.eval_block(node.children[0], table)

    # WTF
    def eval_switch_case(self, node, table):
        it = table.get_it()
        isamatch = False

        # compare it to omg literals until gtfo or oic
        for case in node.children:
            if case.type == ASTType.CASE:
                if not isamatch:
                    case_val = self.evaluate(case.value, table)
                    if it.type == case_val.type and it.value == case_val.value: # bye 'true = 1'
                        isamatch = True

                if isamatch:
                    result = self.evaluate(case.children[0], table)
                    if result == "GTFO":
                        break
                    if result == "RETURN": # connecting returns
                        return "RETURN"

            elif case.type == ASTType.DEFAULT_CASE:
                if not isamatch:
                    isamatch = True
                result = self.evaluate(case.children[0], table)
                if result == "GTFO":
                    break
                if result == "RETURN":
                    return "RETURN"

        return None

    # IM IN YR loops
    def eval_loop(self, node, table):
        operation = node.children[0]
        TW_clause = node.children[1]
        code_block = node.children[2]

        var_name = operation.children[0].value
        UN_type = operation.value
        TW = TW_clause.value
        expression = TW_clause.children[0]

        while True:
            condition = self.evaluate(expression, table)
            is_win = typecast.to_troof(condition).value

            if TW == TokenType.TIL and is_win:
                break
            if TW == TokenType.WILE and not is_win:
                break

            result = self.eval_block(code_block, table)
            if result == "GTFO":
                break
            if result == "RETURN": # connecting returns
                return "RETURN"

            curr = typecast.to_numeric(table.get_variable(var_name)).value
            if UN_type == TokenType.UPPIN:
                new = curr + 1
            else:
                new = curr - 1

            table.set_variable(var_name, MK_NUMBR(new))

        return None

    # ------------------------------------------------
    # FUNCTIONS SECTION
    # ------------------------------------------------
    # Appends function definition ASTnodes
    def eval_func_decl(self, node, table):
        func_name = node.value
        self.functions[func_name] = node
        return None

    # Evaluates function call statemetns(I IZ)
    def eval_func_call(self, node, table):
        func_name = node.value

        if func_name not in self.functions:
            return MK_NOOB()

        function = self.functions[func_name]
        params = function.children[:-1] # all param nodes
        code_block = function.children[-1] # code block

        # each call, own symbol table
        ltable = SymbolTable()
        for i in range(len(params)):
            if i < len(node.children):
                val = self.evaluate(node.children[i], table)
            else:
                val = MK_NOOB()
            ltable.declare_variable(params[i].value, val)

        result = self.eval_block(code_block, ltable)

        if result == "GTFO":
            return MK_NOOB()

        # FOUND YR (or no return at all) leaves the answer in IT
        return ltable.get_it()

    # Evaluates return statements(FOUND YR)
    def eval_return(self, node, table):
        if node.value is None:
            table.set_it(MK_NOOB())
        else:
            table.set_it(self.evaluate(node.value, table))
        return "RETURN" # for stopping functions