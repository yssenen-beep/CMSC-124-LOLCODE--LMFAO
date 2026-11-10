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

    # For GUI, returns a list of tuples containing variable names and their values.
    def get_rows(self):
        rows = []
        for name in self.variables:
            value = self.variables[name]
            if value.type == "NOOB":
                shown = "NOOB"
            elif value.type == "TROOF":
                if value.value == True:
                    shown = "WIN"
                else:
                    shown = "FAIL"
            else:
                shown = str(value.value)
            rows.append((name, shown))
        return rows