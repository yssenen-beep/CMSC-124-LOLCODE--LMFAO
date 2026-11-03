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
        self.match(TokenType.HAI)
        self.match(TokenType.LINEBREAK)
        
        var_ast = self.parse_var_section()
        code_ast = self.parse_code_section()

        self.match(TokenType.KTHXBYE)
        
        return ASTNode(
            type=ASTType.PROGRAM,
            children=[var_ast, code_ast]
        )

        
    def parse_code_section(self):
        statements = []
        while self.current_token:
            if self.current_token.type == TokenType.KTHXBYE:
                break

            new_statement = self.parse_statement()
            statements.append(new_statement)
            print(new_statement)
            
            self.match(TokenType.LINEBREAK)

        return statements

    def parse_statement(self):
        token = self.current_token
        self.ptr += 1

        if not token:
            raise SyntaxError("Unexpected end of input")

        if token.type == TokenType.VISIBLE:
            value = self.parse_print()
            return ASTNode(
                type=ASTType.PRINT,
                value=token.type,
                children = value
            )

        elif token.type == TokenType.GIMMEH:
            value = self.current_token
            self.ptr += 1
            return ASTNode(
                type=ASTType.INPUT,
                value=value
            )

        elif token.type == TokenType.IDENTIFIER:
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

        raise SyntaxError(f"Invalid expression: {token}")

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
        #Get the currrent token
        token = self.current_token
        self.ptr += 1

        #Check if the next token is a linebreak if so return base case
        if (self.current_token.type == TokenType.LINEBREAK):
            return token

        #consume AN
        self.match(TokenType.AN) 

        #Call parse parse_concatenation_expr
        return [token, self.parse_concatenation_expr()]

    def parse_arithmetic_expr(self):
        # Parse left operand
        left = self.parse_expr()

        # CONSUME the An
        self.match(TokenType.AN)

        # Parse right operand
        right = self.parse_expr()

        return [left, right]

