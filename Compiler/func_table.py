class FuncTable:
    mapped_functions = {}

    @staticmethod
    def declare_function(cls, function_name, function):
        if function_name in cls.mapped_functions.keys():
            raise ValueError(f"ERROR: Function {function_name} already declared")
        cls.mapped_functions[function_name] = function

    @staticmethod
    def call_function(cls, function_name):
        if function_name not in cls.mapped_functions.keys():
            raise ValueError(f"ERROR: Function {function_name} not declared")
        return cls.mapped_functions[function_name]

