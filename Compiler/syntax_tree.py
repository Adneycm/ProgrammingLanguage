from abc import ABC, abstractmethod
from func_table import FuncTable
from symbol_table import SymbolTable
from routine import allocate_tasks, insert_task, delete_task

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

    @abstractmethod
    def evaluate(self):
        pass


class Block(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        for child in self.children:
            if type(child).__name__ == 'Return':
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)


class Assignment(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        variable = self.children[0].value
        if type(self.children[1]).__name__ == 'Identifier':
            value = symbol_table.get_variable(self.children[1].evaluate(symbol_table))
        else:
            value = self.children[1].evaluate(symbol_table)
        symbol_table.set_variable(variable, value)


class Identifier(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        return self.value


class Routine(Node):
    def __init__(self, value=None):
        super().__init__(value=value)
        self.free_time = None
        self.tasks_time = None

    def evaluate(self, symbol_table):
        return self
    
    def allocate_tasks(self):
        self.free_time, self.tasks_time = allocate_tasks(self.children[0], self.children[1])
    
    def get_free_time(self):
        return self.free_time
    
    def get_tasks_time(self):
        return self.tasks_time
    
    def print_routine(self):
        print(f"Free time: {self.free_time}")
        print(f"Tasks time: {self.tasks_time}")
    

class Availability(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        routine = symbol_table.get_variable(self.children[0])
        hour = symbol_table.get_variable(self.children[1])
        return hour in routine.get_free_time()


class AddTask(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        routine = symbol_table.get_variable(self.value.evaluate(symbol_table))
        routine = insert_task(self.children[0], self.children[1], routine)
        symbol_table.set_variable(self.value.evaluate(symbol_table), routine)
        return


class DelTask(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        routine = symbol_table.get_variable(self.value.evaluate(symbol_table))
        routine = delete_task(self.children[0], routine)
        symbol_table.set_variable(self.value.evaluate(symbol_table), routine)
        return
    

class VarDec(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        symbol_table.create_variable(self.children[0].value)
        if len(self.children) > 1:
            symbol_table.set_variable(self.children[0].value, self.children[1].evaluate(symbol_table))


class FuncDec(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        FuncTable.declare_function(FuncTable, self.children[0].evaluate(symbol_table), self)
        return


class FuncCall(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        funcdec = FuncTable.call_function(FuncTable, self.value)
        if len(funcdec.children[1:-1]) != len(self.children):
            raise ValueError(f'Number of args does not match for function {self.value}')
        if type(funcdec.children[-1].children[-1]).__name__ != 'Return':
            raise ValueError(f'Function without return')
        local_symbol_table = SymbolTable()
        passed_args = 0
        for arg in funcdec.children[1:-1]:
            if type(self.children[passed_args].children[0]).__name__ == 'Identifier':
                value = symbol_table.get_variable(self.children[passed_args].children[0].evaluate(symbol_table))
            else:
                value = self.children[passed_args].children[0].evaluate(symbol_table)

            local_symbol_table.create_variable(arg.children[0].value)
            local_symbol_table.set_variable(arg.children[0].value,value)
            passed_args+=1

        return funcdec.children[-1].evaluate(local_symbol_table)


class Return(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)


class Print(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        print_value = self.children[0]
        if type(print_value).__name__ == 'Identifier':
            try:
                result = symbol_table.get_variable(print_value.evaluate(symbol_table))
                if type(result).__name__ == 'Routine':
                    result.print_routine()
                    return
                if type(result).__name__ == 'int' or type(result).__name__ == 'float':
                    result = int(result)
                print(result)
                return
            except KeyError:
                raise Exception(f"Variable {print_value.evaluate(symbol_table)} not declared")

        result = print_value.evaluate(symbol_table)
        if type(result).__name__ == 'int' or type(result).__name__ == 'float':
            result = int(result)
        print(result)


class While(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table):
            for command_while in self.children[1]:
                command_while.evaluate(symbol_table)
        return


class If(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table):
            for command_if in self.children[1]:
                command_if.evaluate(symbol_table)
        else:
            if len(self.children) == 3:
                for command_else in self.children[2]:
                    command_else.evaluate(symbol_table)
        return


class Read(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        return int(input())


class BinOp(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        left_val = self.children[0].evaluate(symbol_table)
        right_val = self.children[1].evaluate(symbol_table)

        if left_val in symbol_table.mapped_variables.keys():
            left_val = symbol_table.get_variable(left_val)
        if right_val in symbol_table.mapped_variables.keys():
            right_val = symbol_table.get_variable(right_val)

        if type(left_val).__name__ == 'float':
            left_val = int(left_val)
        if type(right_val).__name__ == 'float':
            right_val = int(right_val)

        if self.value == '+':
            return left_val + right_val
        elif self.value == '-':
            return left_val - right_val
        elif self.value == '..':
            return str(left_val) + str(right_val)

        elif self.value == '*':
            return left_val * right_val
        elif self.value == '/':
            return left_val / right_val

        elif self.value == '>':
            if type(left_val).__name__ == type(right_val).__name__:
                return int(left_val > right_val)
            raise ValueError("ERROR: Incompatible types in '>' operation")
        elif self.value == '<':
            if type(left_val).__name__ == type(right_val).__name__:
                return int(left_val < right_val)
            raise ValueError("ERROR: Incompatible types in '<' operation")
        elif self.value == '==':
            if type(left_val).__name__ == type(right_val).__name__:
                return int(left_val == right_val)
            raise ValueError("ERROR: Incompatible types in '==' operation")

        elif self.value == 'and':
            if type(left_val).__name__ == type(right_val).__name__:
                return left_val and right_val
            raise ValueError("ERROR: Incompatible types in 'and' operation")
        elif self.value == 'or':
            if type(left_val).__name__ == type(right_val).__name__:
                return left_val or right_val
            raise ValueError("ERROR: Incompatible types in 'or' operation")
        else:
            raise ValueError("Invalid input")


class UnOp(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        child_val = self.children[0].evaluate(symbol_table)
        if self.value == '-':
            return -child_val
        elif self.value == 'not':
            return int(not child_val)
        else:
            return child_val


class IntVal(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        return self.value


class StringVal(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self, symbol_table):
        return self.value


class NoOp(Node):
    def __init__(self, value=None):
        super().__init__(value=value)

    def evaluate(self):
        return None

