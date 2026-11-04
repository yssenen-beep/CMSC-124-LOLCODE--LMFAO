from interpreter.tokens import Token, TokenType
from interpreter.lexemes import lex_regex
from interpreter.ast_nodes import ASTNode, ASTType

LITERAL_TYPES = {
    TokenType.NUMBR,
    TokenType.NUMBAR,
    TokenType.YARN,
    TokenType.TROOF
}

ARITHMETIC_TYPES = {
    TokenType.SUM_OF,
    TokenType.DIFF_OF,
    TokenType.PRODUKT_OF,
    TokenType.QUOSHUNT_OF,
    TokenType.MOD_OF,
    TokenType.BIGGR_OF,
    TokenType.SMALLR_OF
}

BOOLEAN_TYPES = {
    TokenType.BOTH_OF,
    TokenType.EITHER_OF,
    TokenType.WON_OF,
    TokenType.NOT,
    TokenType.ALL_OF,
    TokenType.ANY_OF
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ptr = 0
        self.remove_comments()

    def remove_comments(self):
        filtered = []
        for token in self.tokens:
            if token.type in (TokenType.BTW, TokenType.OBTW):
                continue

            if token.type == TokenType.LINEBREAK:
                if not filtered or filtered[-1].type == TokenType.LINEBREAK:
                    continue

            filtered.append(token)
        self.tokens = filtered
    
    def is_not_eof(self):
        if self.tokens[self.ptr].type != TokenType.EOF:
            return True
        else:
            return False

    @property
    def current_token(self):
        if self.is_not_eof():
            return self.tokens[self.ptr]
        return None
    
    def match(self, expected_type):
        token = self.current_token
        if token and token.type == expected_type:
            self.ptr += 1
            return token
        
        raise SyntaxError(f"Expected {expected_type}, got {token}")
    
    def parse_program(self):
        func_ast = self.parse_func_section()
        
        self.match(TokenType.HAI)
        self.match(TokenType.LINEBREAK)
        
        var_ast = self.parse_var_section()
        code_ast = self.parse_code_section()

        self.match(TokenType.KTHXBYE)
        
        return ASTNode(
            type=ASTType.PROGRAM,
            children=[func_ast, var_ast, code_ast]
        )

        
    def parse_code_section(self):
        statements = []
        while self.current_token:
            if self.current_token.type == TokenType.KTHXBYE:
                break

            new_statement = self.parse_statement()
            statements.append(new_statement)
            
            self.match(TokenType.LINEBREAK)

        return statements

    def parse_statement(self):
        token = self.current_token

        if not token:
            raise SyntaxError("Unexpected end of input")
        
        if token.type == TokenType.VISIBLE:
            self.ptr += 1
            value = self.parse_print()
            return ASTNode(
                type=ASTType.PRINT,
                value=token.type,
                children = value
            )

        elif token.type == TokenType.GIMMEH:
            self.ptr += 1
            value = self.current_token
            self.ptr += 1
            return ASTNode(
                type=ASTType.INPUT,
                value=value.value
            )

        elif token.type == TokenType.IDENTIFIER:
            self.ptr+=1
            if self.current_token and self.current_token.type == TokenType.R:
                self.match(TokenType.R)
                expr = self.parse_expr()
                return ASTNode(
                    type=ASTType.ASSIGNMENT,
                    value=token.value,
                    children=[expr]
                )

            elif self.current_token and self.current_token.type == TokenType.IS_NOW_A:
                self.match(TokenType.IS_NOW_A)
                type_token = self.match(TokenType.TYPE)
                return ASTNode(
                    type=ASTType.TYPECAST,
                    value=token.value,
                    children=[ASTNode(type=ASTType.LITERAL, value=type_token.value)]
                )
            self.ptr-=1
            
        elif token.type == TokenType.IM_IN_YR:
            return self.parse_loop()
        
        elif token.type == TokenType.WTF:
            return self.parse_switch()
            
        is_if_else = False
        lookahead_ptr = self.ptr
        while lookahead_ptr < len(self.tokens):
            if self.tokens[lookahead_ptr].type == TokenType.LINEBREAK:
                if lookahead_ptr + 1 < len(self.tokens) and self.tokens[lookahead_ptr + 1].type == TokenType.O_RLY:
                    is_if_else = True
                break
            lookahead_ptr += 1

        #For if else
        if is_if_else:
            condition = self.parse_expr()
            return self.parse_if_else_block(condition)

        #For reading bare expressions
        if self.current_token and self.current_token.type != TokenType.LINEBREAK:
            expr = self.parse_expr()
            return ASTNode(type=ASTType.EXPRESSION, children=[expr])


        raise SyntaxError(f"Invalid expression: {token}, {self.tokens[self.ptr+1]}")

    def parse_print(self):
        operands = [self.parse_expr()]

        while self.current_token and self.current_token.type == TokenType.PLUS:
            self.match(TokenType.PLUS)
            operands.append(self.parse_expr())

        return operands

    
    def parse_var_section(self):
        # epsilon case
        if not self.current_token or self.current_token.type != TokenType.WAZZUP:
            return ASTNode(
                type=ASTType.VARIABLE_SECTION
            )
        self.match(TokenType.WAZZUP)
        self.match(TokenType.LINEBREAK)
        declarations_list = self.parse_declarations()
        
        self.match(TokenType.BUHBYE)
        self.match(TokenType.LINEBREAK)
        
        return ASTNode(
            type=ASTType.VARIABLE_SECTION,
            children=declarations_list
        )
    
    def parse_declarations(self):
        declarations = []

        while self.current_token:
            if self.current_token.type != TokenType.I_HAS_A:
                break
        
            dec = self.parse_declaration()
            declarations.append(dec)
            
            self.match(TokenType.LINEBREAK)
        return declarations
        
    def parse_declaration(self):
        self.match(TokenType.I_HAS_A)
        ident = self.match(TokenType.IDENTIFIER)
        
        if self.current_token and self.current_token.type == TokenType.ITZ:
            self.match(TokenType.ITZ)
            expr_dec = self.parse_expr()
            return ASTNode(
                type=ASTType.DECLARATION,
                value=ident.value,
                children=[expr_dec]
            )
            
        return ASTNode(
            type=ASTType.DECLARATION,
            value=ident.value
        )
    
    def parse_func_section(self):
        functions = []
        
        while self.current_token and self.current_token.type == TokenType.HOW_IZ_I:
            functions.append(self.parse_func_dec())
            self.match(TokenType.LINEBREAK)
        
        return ASTNode(
            type=ASTType.FUNCTION_SECTION,
            children=functions
        )
        
        while self.current_token and self.current_token.type not in (TokenType.IF_U_SAY_SO, TokenType.FOUND_YR):
            statements.append(self.parse_statement())
            self.match(TokenType.LINEBREAK)
                
        return_node = self.parse_return()
        
        self.match(TokenType.IF_U_SAY_SO)
        
        return ASTNode(
            type=ASTType.FUNCTION_DECLARATION,
            value=ident.value,
            children=params + statements + ([return_node] if return_node else [])
        )
    
    def parse_func_dec(self):
        self.match(TokenType.HOW_IZ_I)
        ident = self.match(TokenType.IDENTIFIER)
        params = self.parse_params_line()
        self.match(TokenType.LINEBREAK)
        
        statements = []
        return_node = None
        
        while self.current_token and self.current_token.type != TokenType.IF_U_SAY_SO:
            if self.current_token.type == TokenType.FOUND_YR:
                return_node = self.parse_return()
                break
            elif self.current_token.type == TokenType.GTFO:
                # GTFO inside a function acts as a return with no value (returns NOOB)
                self.match(TokenType.GTFO)
                return_node = ASTNode(type=ASTType.RETURN, value=None)
                break
            
            statements.append(self.parse_statement())
            self.match(TokenType.LINEBREAK)
                
        if self.current_token and self.current_token.type == TokenType.LINEBREAK:
            self.match(TokenType.LINEBREAK)

        self.match(TokenType.IF_U_SAY_SO)
        
        statements_node = ASTNode(
            type=ASTType.STATEMENT_BLOCK,
            children=statements
        )
        
        children = [statements_node]
        if params:
            children = params + children
        if return_node:
            children.append(return_node)
            
        return ASTNode(
            type=ASTType.FUNCTION_DECLARATION,
            value=ident.value,
            children=children
        )
    
    def parse_params_line(self):
        if not self.current_token or self.current_token.type != TokenType.YR:
            return []
        return self.parse_parameters()
    
    def parse_parameters(self):
        params = [self.parse_param()]
        while self.current_token and self.current_token.type == TokenType.AN:
            self.match(TokenType.AN)
            params.append(self.parse_param())
        return params
    
    def parse_param(self):
        self.match(TokenType.YR)
        ident = self.match(TokenType.IDENTIFIER)
        return ASTNode(
            type=ASTType.PARAMETER,
            value=ident
        )
    
    def parse_return(self):
        if self.current_token and self.current_token.type == TokenType.GTFO:
            return ASTNode(
                type=ASTType.RETURN
            )
        self.match(TokenType.FOUND_YR)
        expr = self.parse_expr()
        self.match(TokenType.LINEBREAK)
        
        return ASTNode(
            type=ASTType.RETURN,
            value=expr
        )
    
    def parse_if_else_block(self, condition_expr):
        self.match(TokenType.LINEBREAK)
        self.match(TokenType.O_RLY)
        self.match(TokenType.LINEBREAK)
        
        # ya rly
        self.match(TokenType.YA_RLY)
        self.match(TokenType.LINEBREAK)
        
        ya_rly_statements = []
        while self.current_token and self.current_token.type not in (TokenType.MEBBE, TokenType.NO_WAI, TokenType.OIC):
            ya_rly_statements.append(self.parse_statement())
            self.match(TokenType.LINEBREAK)
        
        ya_rly_block = ASTNode(
            type=ASTType.STATEMENT_BLOCK,
            children=ya_rly_statements
        )
        
        else_block = self.parse_else_block()
        
        self.match(TokenType.OIC)
        
        children = [condition_expr, ya_rly_block]
        if else_block:
            children.append(else_block)
            
        return ASTNode(
            type=ASTType.IF_ELSE,
            children=children
        )
    
    def parse_else_block(self):
        if not self.current_token:
            return None # no else statement
        
        if self.current_token.type == TokenType.MEBBE:
            return self.parse_else_if()
        elif self.current_token.type == TokenType.NO_WAI:
            return self.parse_else()
        
        return None
    
    def parse_else_if(self):
        self.match(TokenType.MEBBE)
        condition = self.parse_expr()
        self.match(TokenType.LINEBREAK)
        
        statements = []
        while self.current_token and self.current_token.type not in (TokenType.MEBBE, TokenType.NO_WAI, TokenType.OIC):
            statements.append(self.parse_statement())
            self.match(TokenType.LINEBREAK)
                
        statements_block = ASTNode(
            type=ASTType.STATEMENT_BLOCK,
            children=statements
        )
        
        next_else = self.parse_else_block() # check for subsequent else
        
        children = [condition, statements_block]
        if next_else:
            children.append(next_else)
            
        return ASTNode(
            type=ASTType.ELSE_IF,
            children=children
        )
        
    def parse_else(self):
        self.match(TokenType.NO_WAI)
        self.match(TokenType.LINEBREAK)
        
        statements = []
        while self.current_token and self.current_token.type != TokenType.OIC:
            statements.append(self.parse_statement())
            self.match(TokenType.LINEBREAK)
                
        statements_block = ASTNode(
            type=ASTType.STATEMENT_BLOCK,
            children=statements
        )
        
        return ASTNode(
            type=ASTType.ELSE,
            children=[statements_block]
        )
    
    def parse_switch(self):
        self.match(TokenType.WTF)
        self.match(TokenType.LINEBREAK)
        
        cases = []
        default_case = None
        
        while self.current_token and self.current_token.type != TokenType.OIC:
            if self.current_token.type == TokenType.OMG:
                cases.append(self.parse_case())
            elif self.current_token.type == TokenType.OMGWTF:
                default_case = self.parse_default_case()
                break
            else:
                raise SyntaxError(f"Expected OMG or OMGWTF in switch block, got {self.current_token}")
        self.match(TokenType.OIC)
        
        children = list(cases)
        if default_case:
            children.append(default_case)
        
        return ASTNode(
            type=ASTType.SWITCH_CASE,
            children=children
        )
    
    def parse_case(self):
        self.match(TokenType.OMG)
        expr = self.parse_expr()
        self.match(TokenType.LINEBREAK)
        
        statements = []
        while self.current_token and self.current_token.type not in (TokenType.OMG, TokenType.OMGWTF, TokenType.OIC):
            if self.current_token.type == TokenType.GTFO:
                self.match(TokenType.GTFO)
                statements.append(ASTNode(type=ASTType.GTFO, value=TokenType.GTFO))
                if self.current_token and self.current_token.type == TokenType.LINEBREAK:
                    self.match(TokenType.LINEBREAK)
                break
                
            statements.append(self.parse_statement())
            if self.current_token and self.current_token.type == TokenType.LINEBREAK:
                self.match(TokenType.LINEBREAK)
                
        statements_block = ASTNode(
            type=ASTType.STATEMENT_BLOCK,
            children=statements
        )
        
        return ASTNode(
            type=ASTType.CASE,
            value=expr,
            children=[statements_block]
        )
    
    def parse_default_case(self):
        self.match(TokenType.OMGWTF)
        self.match(TokenType.LINEBREAK)
        
        statements = []
        while self.current_token and self.current_token.type != TokenType.OIC:
            if self.current_token.type == TokenType.GTFO:
                self.match(TokenType.GTFO)
                statements.append(ASTNode(type=ASTType.GTFO, value=TokenType.GTFO))
                if self.current_token and self.current_token.type == TokenType.LINEBREAK:
                    self.match(TokenType.LINEBREAK)
                break

            statements.append(self.parse_statement())
            if self.current_token and self.current_token.type == TokenType.LINEBREAK:
                self.match(TokenType.LINEBREAK)
                
        statements_block = ASTNode(
            type=ASTType.STATEMENT_BLOCK,
            children=statements
        )
        
        return ASTNode(
            type=ASTType.DEFAULT_CASE,
            children=[statements_block]
        )
        
    
    def parse_loop(self):
        self.match(TokenType.IM_IN_YR)
        label = self.match(TokenType.IDENTIFIER)
        
        # operation type
        op_token = self.current_token
        if op_token and op_token.type in (TokenType.UPPIN, TokenType.NERFIN):
            self.ptr += 1
        else:
            raise SyntaxError(f"Expected UPPIN or NERFIN in loop header, got {op_token}")
        self.match(TokenType.YR)
        var = self.match(TokenType.IDENTIFIER)
        loop_operation = ASTNode(
            type=ASTType.LOOP_OP,
            value=op_token.type,
            children=[ASTNode(type=ASTType.IDENTIFIER, value=var.value)]
        )
        
        cond_token = self.current_token
        if cond_token and cond_token.type in (TokenType.TIL, TokenType.WILE):
            self.ptr += 1
        else:
            raise SyntaxError(f"Expected TIL or WILE in loop header, got {cond_token}")
            
        expr = self.parse_expr()
        loop_condition = ASTNode(
            type=ASTType.LOOP_CONDITION,
            value=cond_token.type,
            children=[expr]
        )
        
        self.match(TokenType.LINEBREAK)
        
        # parse the body
        statements = []
        while self.current_token:
            if self.current_token.type == TokenType.IM_OUTTA_YR:
                break
            statements.append(self.parse_statement())
            self.match(TokenType.LINEBREAK)

        statements_block = ASTNode(
            type=ASTType.STATEMENT_BLOCK,
            children=statements
        )

        # parse end
        self.match(TokenType.IM_OUTTA_YR)
        end_label = self.match(TokenType.IDENTIFIER)
        
        if end_label.value != label.value:
            raise SyntaxError(f"Loop label mismatch: expected '{label.value}', got '{end_label.value}'")

        return ASTNode(
            type=ASTType.LOOP,
            value=label.value,
            children=[loop_operation, loop_condition, statements_block]
        )

    def parse_expr(self):
        token = self.current_token
        self.ptr += 1

        if not token:
            raise SyntaxError("Unexpected end of input")
        
        #Parses literal types into AST nodes
        if token.type in LITERAL_TYPES:
            return ASTNode(
                type=ASTType.LITERAL,
                value=token.value
            )

        #Parses variables
        elif token.type == TokenType.IDENTIFIER:
            return ASTNode(
                type=ASTType.IDENTIFIER,
                value=token.value
            )

        #Parses Arthmetic Expressions
        elif token.type in ARITHMETIC_TYPES:
            value = self.parse_arithmetic_expr()
            return ASTNode(
                type=ASTType.ARITHMETIC,
                value=token.type,
                children=value
            )
        
        #Parses CONCATENATION expression
        elif token.type == TokenType.SMOOSH:
            value = self.parse_concatenation_expr()
            return ASTNode(
                type=ASTType.CONCATENATION,
                value=token.type,
                children=value
            )

        #Parse Boolean operations
        elif token.type in BOOLEAN_TYPES:
            if(token.type == TokenType.ALL_OF or token.type == TokenType.ANY_OF):
                value = self.parse_boolean_expr_all_any()
            elif(token.type == TokenType.NOT):
                value = [self.parse_expr()]
            else:
                value = self.parse_boolean_expr()
            return ASTNode(
                type=ASTType.BOOLEAN_EXPRESSION,
                value=token.type,
                children=value
            )
        
        #Parse comprison operation
        elif token.type in [TokenType.BOTH_SAEM, TokenType.DIFFRINT]:
            value = self.parse_comparison_expr()
            return ASTNode(
                type=ASTType.COMPARISON,
                value=token.type,
                children=value
            )

        #Parse the maek expression
        elif token.type == TokenType.MAEK:
            value = self.parse_maek_expr()
            return ASTNode(
                type=ASTType.TYPECAST,
                value=token.type,
                children=value
            )
        
        #Parse function calls
        elif token.type == TokenType.I_IZ:
            ident = self.match(TokenType.IDENTIFIER)
            args = []
            if self.current_token and self.current_token.type == TokenType.YR:
                self.match(TokenType.YR)
                args.append(self.parse_expr())
                while self.current_token and self.current_token.type == TokenType.AN:
                    self.match(TokenType.AN)
                    self.match(TokenType.YR)
                    args.append(self.parse_expr())
            if self.current_token and self.current_token.type == TokenType.MKAY:
                self.match(TokenType.MKAY)      # MKAY is optional in your tests
            return ASTNode(
                type=ASTType.FUNCTION_CALL,
                value=ident.value,
                children=args
            )

        raise SyntaxError(f"Invalid expression: {token}")

    #Function helper
    def parse_maek_expr(self):
        operand = self.parse_expr()
        type_token = self.match(TokenType.TYPE)
        return [
            operand,
            ASTNode(type=ASTType.LITERAL, value=type_token.value)
        ]
   
    def parse_comparison_expr(self):
        left = self.parse_expr()

        self.match(TokenType.AN)

        right = self.parse_expr()

        return [left, right]
        
    #Parses the rest of the boolean expressions
    def parse_boolean_expr(self):
         # Parse left operand
        left = self.parse_expr()

        # CONSUME the An
        self.match(TokenType.AN)

        # Parse right operand
        right = self.parse_expr()
        return [left, right]
    
    #Parses the infinity arity stuff
    def parse_boolean_expr_all_any(self):
        operands = []

        # Parse first operand
        operands.append(self.parse_expr())

        # Parse remaining operands
        while self.current_token and self.current_token.type == TokenType.AN:
            self.match(TokenType.AN)
            operands.append(self.parse_expr())

        # Consume MKAY
        self.match(TokenType.MKAY)
        return operands

    def parse_concatenation_expr(self):
        operands = [self.parse_expr()]
        while self.current_token and self.current_token.type == TokenType.AN:
            self.match(TokenType.AN)
            operands.append(self.parse_expr())
        return operands

    def parse_arithmetic_expr(self):
        # Parse left operand
        left = self.parse_expr()

        # CONSUME the An
        self.match(TokenType.AN)

        # Parse right operand
        right = self.parse_expr()

        return [left, right]

