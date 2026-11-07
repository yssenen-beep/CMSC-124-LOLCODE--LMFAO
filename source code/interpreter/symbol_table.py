"""
Symbol table for storing variables and their values
"""
from interpreter.values import MK_NOOB

class SymbolTable:
    def __init__(self):
        self.variables = {}
        #NOOB is the default value for unitialized variables
        self.variables["IT"] = MK_NOOB()

    def declare_variable(self, name, value):
        if name in self.variables:
            raise Exception(f"Variable '{name}' already declared.")
        self.variables[name] = value
    
    def get_variable(self, name):
        if name not in self.variables:
            raise Exception(f"Variable '{name}' is not declared.")
        return self.variables[name]

    def set_variable(self, name, value):
        if name not in self.variables:
            raise Exception(f"Variable '{name}' is not declared.")
        self.variables[name] = value

    def get_it(self):
        return self.variables["IT"]

    def set_it(self, value):
        self.variables["IT"] = value