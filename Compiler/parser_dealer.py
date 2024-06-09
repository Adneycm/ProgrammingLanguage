from token_dealer import Tokenizer
from syntax_tree import \
    Block, Assignment, Identifier,\
    VarDec, Print, While, If, Read,\
    BinOp, UnOp, IntVal, StringVal, NoOp,\
    FuncDec, FuncCall, Return, Routine, Availability, AddTask, DelTask
from symbol_table import SymbolTable


class Parser:
    def __init__(self):
        self.tokenizer = None

    def parse_args(self):
        if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
            args = []
            while self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                vardec = VarDec(value='local')

                arg = self.parse_bool_expression()

                vardec.children.append(arg)
                args.append(vardec)

                if self.tokenizer.next.type == 'COMMA':
                    self.tokenizer.position += 1
                    self.tokenizer.select_next()
            return args
        return []

    def parse_block(self):
        block = Block()
        while self.tokenizer.next.type != 'EOF':
            block.children.append(self.parse_statment())
        return block

    def parse_statment(self):

        if self.tokenizer.next.type == 'IDENTIFIER':
            identifier = Identifier(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type == 'DOT':
                self.tokenizer.position += 1
                self.tokenizer.select_next()
                add_task = AddTask(value=identifier)
                del_task = DelTask(value=identifier)

                if self.tokenizer.next.type not in ['ADD_TASK', 'DEL_TASK']:
                    raise ValueError('Invalid input: Expecting "add_task" or "del_task" after "identifier."')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                    raise ValueError('Invalid input: Expecting "(" after add_task or del_task')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'STR':
                    raise ValueError('Invalid input: Task name to add/del must be string')
                task = self.tokenizer.next.value
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'COMMA':
                    if self.tokenizer.next.type == 'RIGHT-PARENTHESIS':
                        self.tokenizer.position += 1
                        self.tokenizer.select_next()

                        if self.tokenizer.next.type != 'NEW-LINE':
                            raise ValueError('Invalid input: Expecting "new-line" after assignment')
                        self.tokenizer.position += 1
                        self.tokenizer.select_next()
                        del_task.children = [task]
                        return del_task
                    raise ValueError('Invalid input: Expecting "," between task and time to add')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'INT':
                    raise ValueError('Invalid input: Task time to add must be integer')
                task_time = self.tokenizer.next.value
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                    raise ValueError('Invalid input: Expecting ")"')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'NEW-LINE':
                    raise ValueError('Invalid input: Expecting "new-line" after assignment')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                add_task.children = [task, task_time]
                return add_task

            if self.tokenizer.next.type != 'ASSIGN':
                if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                    raise ValueError('Invalid input: Expecting "(" or "=" after identifier')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                funccall = FuncCall(identifier.value)

                funccall.children += self.parse_args()

                if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                    raise ValueError('Invalid input: Expecting ")"')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'NEW-LINE':
                    raise ValueError('Invalid input: Expecting "new-line" after assignment')
                self.tokenizer.position += 1
                self.tokenizer.select_next()
                return funccall

            assignment = Assignment(value='=')
            assignment.children.append(identifier)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            assignment.children.append(self.parse_bool_expression())

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after assignment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return assignment

        if self.tokenizer.next.type == "LOCAL":
            vardec = VarDec(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'IDENTIFIER':
                raise ValueError('Invalid input: Expecting Identifier variable after "local" statment')

            identifier = Identifier(value=self.tokenizer.next.value)
            vardec.children.append(identifier)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type == 'ASSIGN':
                self.tokenizer.position += 1
                self.tokenizer.select_next()
                vardec.children.append(self.parse_bool_expression())

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after local assigment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return vardec

        if self.tokenizer.next.type == 'PRINT':
            node_print = Print(self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting "="')

            self.tokenizer.position += 1
            self.tokenizer.select_next()
            node_print.children.append(self.parse_bool_expression())

            if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting ")"')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after print')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return node_print

        if self.tokenizer.next.type == 'WHILE':
            node_while = While(self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            condition = self.parse_bool_expression()
            node_while.children.append(condition)

            if self.tokenizer.next.type != 'LEFT-CURLY-BRACKET':
                raise ValueError('Invalid input: Expecting "{" after while condition')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after while statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            commands_while = []
            while self.tokenizer.next.type != 'RIGHT-CURLY-BRACKET':
                commands_while.append(self.parse_statment())
            node_while.children.append(commands_while)

            if self.tokenizer.next.type != 'RIGHT-CURLY-BRACKET':
                raise ValueError('Invalid input: Expecting "}" after if statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after if statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return node_while

        if self.tokenizer.next.type == 'IF':
            node_if = If(self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            condition = self.parse_bool_expression()
            node_if.children.append(condition)

            if self.tokenizer.next.type != 'LEFT-CURLY-BRACKET':
                raise ValueError('Invalid input: Expecting "{" after if condition')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after if statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            commands_if = []
            while self.tokenizer.next.type not in ['RIGHT-CURLY-BRACKET', 'ELSE']:
                commands_if.append(self.parse_statment())
            node_if.children.append(commands_if)

            if self.tokenizer.next.type == 'ELSE':
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'NEW-LINE':
                    raise ValueError('Invalid input: Expecting "new-line" after else statment')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                commands_else = []
                while self.tokenizer.next.type != 'RIGHT-CURLY-BRACKET':
                    commands_else.append(self.parse_statment())
                node_if.children.append(commands_else)

            if self.tokenizer.next.type != 'RIGHT-CURLY-BRACKET':
                raise ValueError('Invalid input: Expecting "}" after if statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after if statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return node_if

        if self.tokenizer.next.type == 'FUNCTION':
            funcdec = FuncDec(self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'IDENTIFIER':
                raise ValueError('Invalid input: Expecting Identifier variable after "function" statment')

            identifier = Identifier(value=self.tokenizer.next.value)
            funcdec.children.append(identifier)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting "="')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            funcdec.children += self.parse_args()

            if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting ")"')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "\\n" after function declaration')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            func_block = Block()
            while self.tokenizer.next.type != 'END':
                func_block.children.append(self.parse_statment())
            funcdec.children.append(func_block)

            if self.tokenizer.next.type != 'END':
                raise ValueError('Invalid input: Expecting "end" after if statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after if statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return funcdec

        if self.tokenizer.next.type == 'RETURN':
            node_return = Return(self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            node_return.children.append(self.parse_bool_expression())

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after return')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return node_return

        if self.tokenizer.next.type == 'ROUTINE':
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'IDENTIFIER':
                raise ValueError('Invalid input: Expecting identifier after routine statment')
            identifier = Identifier(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'ASSIGN':
                raise ValueError('Invalid input: Expecting "=" after routine declaration')
            assignment = Assignment(value='=')
            assignment.children.append(identifier)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            assignment.children.append(self.parse_bool_expression())

            if self.tokenizer.next.type != 'NEW-LINE':
                raise ValueError('Invalid input: Expecting "new-line" after assignment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return assignment



        raise ValueError('Invalid input')

    def parse_bool_expression(self):
        node = self.parse_bool_term()
        while self.tokenizer.next.type in ['OR']:
            result = BinOp(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            result.children.append(node)
            result.children.append(self.parse_bool_term())
            node = result
        return node

    def parse_bool_term(self):
        node = self.parse_relational_expression()
        while self.tokenizer.next.type in ['AND']:
            result = BinOp(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            result.children.append(node)
            result.children.append(self.parse_relational_expression())
            node = result
        return node

    def parse_relational_expression(self):
        node = self.parse_expression()
        while self.tokenizer.next.type in ['EQUAL', 'BIGGER', 'SMALLER']:
            result = BinOp(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            result.children.append(node)
            result.children.append(self.parse_expression())
            node = result
        return node

    def parse_expression(self):
        node = self.parse_term()
        while self.tokenizer.next.type in ['PLUS', 'MINUS', 'CONCAT']:
            result = BinOp(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            result.children.append(node)
            result.children.append(self.parse_term())
            node = result
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.tokenizer.next.type in ['MULTIPLICATION', 'DIVISION']:
            result = BinOp(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            result.children.append(node)
            result.children.append(self.parse_factor())
            node = result
        return node

    def parse_factor(self):

        if self.tokenizer.next.type == 'INT':
            result = IntVal(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            return result

        if self.tokenizer.next.type == 'STR':
            result = StringVal(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            return result

        if self.tokenizer.next.type == 'IDENTIFIER':
            result = Identifier(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                return result
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            funccall = FuncCall(result.value)

            funccall.children += self.parse_args()

            if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting ")"')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return funccall
        
        if self.tokenizer.next.type == 'AVAILABILITY':
            availability = Availability(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting "(" after availability method')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'IDENTIFIER':
                raise ValueError('Invalid input: Expecting routine identifier after availability method')
            availability.children.append(self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'COMMA':
                raise ValueError('Invalid input: Expecting "," between availability arguments')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type not in ['INT', 'IDENTIFIER']:
                raise ValueError('Invalid input: Hour argument in availability method must be integer')
            availability.children.append(self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting ")" after availability method')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return availability

        while self.tokenizer.next.type in ['PLUS', 'MINUS', 'NOT']:
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            result = UnOp(value=self.tokenizer.next.value)
            result.children.append(self.parse_factor())
            return result

        if self.tokenizer.next.type == 'LEFT-PARENTHESIS':
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            result = self.parse_bool_expression()

            if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting ")"')
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            return result
        
        if self.tokenizer.next.type == 'LEFT-SQUARE-BRACKET':
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            routine = Routine(value='routine')

            tasks = []
            restrictions = []


            while self.tokenizer.next.type != 'RIGHT-SQUARE-BRACKET':
                if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                    raise ValueError('Invalid input: Expecting "("')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'STR':
                    raise ValueError('Invalid input: Expecting "STR" as task name')
                task = self.tokenizer.next.value
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'COMMA':
                    raise ValueError('Invalid input: Expecting "," between task and time')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'INT':
                    raise ValueError('Invalid input: Expecting "INT" as task time')
                time = self.tokenizer.next.value
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                tasks.append((task, time))

                if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                    raise ValueError('Invalid input: Expecting ")"')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type == 'COMMA':
                    self.tokenizer.position += 1
                    self.tokenizer.select_next()

            self.tokenizer.position += 1
            self.tokenizer.select_next()

            if self.tokenizer.next.type == 'COMMA':
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                if self.tokenizer.next.type != 'LEFT-SQUARE-BRACKET':
                    raise ValueError('Invalid input: Expecting "("')
                self.tokenizer.position += 1
                self.tokenizer.select_next()

                
                while self.tokenizer.next.type != 'RIGHT-SQUARE-BRACKET':
                    if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                        raise ValueError('Invalid input: Expecting "("')
                    self.tokenizer.position += 1
                    self.tokenizer.select_next()

                    if self.tokenizer.next.type != 'INT':
                        raise ValueError('Invalid input: Expecting "INT" as restriction time')
                    lower_restriction = self.tokenizer.next.value
                    self.tokenizer.position += 1
                    self.tokenizer.select_next()

                    if self.tokenizer.next.type != 'COMMA':
                        raise ValueError('Invalid input: Expecting "," between upper and lower restrictions')
                    self.tokenizer.position += 1
                    self.tokenizer.select_next()

                    if self.tokenizer.next.type != 'INT':
                        raise ValueError('Invalid input: Expecting "INT" as restriction time')
                    upper_restriction = self.tokenizer.next.value
                    self.tokenizer.position += 1
                    self.tokenizer.select_next()

                    restrictions.append((lower_restriction, upper_restriction))

                    if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                        raise ValueError('Invalid input: Expecting ")"')
                    self.tokenizer.position += 1
                    self.tokenizer.select_next()

                    if self.tokenizer.next.type == 'COMMA':
                        self.tokenizer.position += 1
                        self.tokenizer.select_next()

                self.tokenizer.position += 1
                self.tokenizer.select_next()

            routine.children = [tasks, restrictions]
            routine.allocate_tasks()
            return routine







        if self.tokenizer.next.type == 'READ':
            result = Read(value=self.tokenizer.next.value)
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            if self.tokenizer.next.type != 'LEFT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting "(" after "read" statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()
            if self.tokenizer.next.type != 'RIGHT-PARENTHESIS':
                raise ValueError('Invalid input: Expecting ")" after "read" statment')
            self.tokenizer.position += 1
            self.tokenizer.select_next()

            return result

        else:
            print('NoOp')
            return NoOp()

    def run(self, source):
        symbol_table = SymbolTable()
        self.tokenizer = Tokenizer(source=source)
        self.tokenizer.position = 0
        self.tokenizer.select_next()
        block = self.parse_block()

        block.evaluate(symbol_table)

