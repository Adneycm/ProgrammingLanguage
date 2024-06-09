class SymbolTable:
    def __init__(self):
        self.mapped_variables = {}

    def create_variable(self, variable):
        if variable in self.mapped_variables.keys():
            raise ValueError(f"ERROR: Variable {variable} already setted")
        self.mapped_variables[variable] = (None, None)

    def set_variable(self, variable, value):
        if variable not in self.mapped_variables.keys():
            raise ValueError(f"ERROR: Not possible to set a variable {variable} without creating it first")
        self.mapped_variables[variable] = (value, type(value).__name__)

    def get_variable(self, variable):
        if variable not in self.mapped_variables.keys():
            raise ValueError(f"ERROR: {variable} not defined")
        return self.mapped_variables[variable][0]

    def get_type(self, variable):
        return self.mapped_variables[variable][1]
    
