from interpreter.tokens import Token, TokenType
from interpreter.lexemes import lex_regex

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ptr = 0
    
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
        return {
            "type": "PROGRAM_ROOT",
            "variable_block": var_ast,
        }
    
    def parse_var_section(self):
        # epsilon case
        if not self.current_token or self.current_token.type != TokenType.WAZZUP:
            return {
                "type": "VARIABLE_SECTION",
                "declarations": []  # Empty section block
            }
            
        self.match(TokenType.WAZZUP)
        self.match(TokenType.LINEBREAK)
        declarations_list = self.parse_declarations()
        
        self.match(TokenType.BUHBYE)
        self.match(TokenType.LINEBREAK)
        
        return {
            "type": "VARIABLE_SECTION",
            "declarations": declarations_list
        }
    
    def parse_declarations(self):
        declarations = []
        
        while self.current_token and self.current_token.type == TokenType.I_HAS_A:
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
            return("DECLARATION_WITH_INIT", ident.value, expr_dec)
            
        return("DECLARATION", ident.value)
    
    def parse_expr(self):
        self.ptr += 1
        return("EXPRESSION", 67) # testing lang po
