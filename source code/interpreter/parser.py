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
    TokenType.MOD_OF
}

BOOLEAN_TYPES = {
    TokenType.BOTH_OF,
    TokenType.EITHER_OF,
    TokenType.WON_OF,
    TokenType.NOT
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ptr = 0
        self.remove_comments()

    #Before we parse any program we remove all comments from the system
    def remove_comments(self):
        filtered_tokens = []
        for token in self.tokens:
            if token.type not in (TokenType.BTW, TokenType.OBTW):
                filtered_tokens.append(token)

        self.tokens = filtered_tokens
    
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
        
        self.match(TokenType.KTHXBYE)
        return ASTNode(
            type=ASTType.PROGRAM,
            children=[var_ast]
        )
    
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
            #Check if there is comments in function declartion

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
        elif token.type in BOOLEAN_TYPES:
            value = self.parse_boolean_expr()
            return ASTNode(
                type=ASTType.BOOLEAN,
                value=token.type,
                children=value
            )

        raise SyntaxError(f"Invalid expression: {token}")

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

        # Expect AN
        self.match(TokenType.AN)

        # Parse right operand
        right = self.parse_expr()

        return [left, right]
"""
SUM OF <x> AN <y>             BTW + (add)
DIFF OF <x> AN <y>            BTW - (subtract)
PRODUKT OF <x> AN <y>         BTW * (multiply)
QUOSHUNT OF <x> AN <y>        BTW / (divide)
MOD OF <x> AN <y>             BTW % (modulo)
BIGGR OF <x> AN <y>           BTW max
SMALLR OF <x> AN <y>  
"""

