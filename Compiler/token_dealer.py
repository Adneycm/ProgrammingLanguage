import re


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = None
        self.next = None
        self.reserved_words = [
            'print', 'function', 'return',
            'while', 'do', 'end',
            'if', 'else', 'then',
            'and', 'or', 'not',
            'read', 'local', 'routine',
            'availability', 'add_task',
            'del_task'
        ]

    def select_next(self):
        # Checking end of file (EOF)
        if self.position >= len(self.source):
            self.next = Token(type='EOF', value=None)
            return

        token = self.source[self.position]
        aux = self.source[self.position]
        letter_after_number = False

        # Checking for blank spaces
        while token == ' ' or token == '\t':
            self.position += 1
            token = self.source[self.position]
            if token.isdigit() and aux.isdigit():
                raise ValueError('Invalid input')

        # Checking for numbers
        while token.isdigit() and self.position + 1 < len(self.source):
            if self.source[self.position + 1].isdigit():
                self.position += 1
                token += self.source[self.position]
            else:
                try:
                    letter_after_number = self.source[self.position + 1].isalpha()
                except:
                    pass
                break

        # Checking for reserved words & variable names
        match = re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', self.source[self.position:])
        if match:
            token = match.group(0)
            self.position += match.end()-1

        if token == '+':
            self.next = Token(type='PLUS', value='+')

        elif token == '-':
            self.next = Token(type='MINUS', value='-')

        elif token == '/':
            self.next = Token(type='DIVISION', value='/')

        elif token == '*':
            self.next = Token(type='MULTIPLICATION', value='*')

        elif token == '(':
            self.next = Token(type='LEFT-PARENTHESIS', value='(')

        elif token == ')':
            self.next = Token(type='RIGHT-PARENTHESIS', value=')')

        elif token == '[':
            self.next = Token(type='LEFT-SQUARE-BRACKET', value='(')

        elif token == ']':
            self.next = Token(type='RIGHT-SQUARE-BRACKET', value=')')

        elif token == '{':
            self.next = Token(type='LEFT-CURLY-BRACKET', value='{')

        elif token == '}':
            self.next = Token(type='RIGHT-CURLY-BRACKET', value='}')

        elif token.isdigit() and not letter_after_number:
            self.next = Token(type='INT', value=int(token))

        elif token == '=':
            if token + self.source[self.position + 1] == '==':
                self.position += 1
                self.next = Token(type='EQUAL', value='==')
            else:
                self.next = Token(type='ASSIGN', value='=')

        elif token == '.':
            if token + self.source[self.position + 1] == '..':
                self.position += 1
                self.next = Token(type='CONCAT', value='..')
            self.next = Token(type='DOT', value='.')

        elif token == ',':
            self.next = Token(type='COMMA', value=',')

        elif token == '>':
            self.next = Token(type='BIGGER', value='>')

        elif token == '<':
            self.next = Token(type='SMALLER', value='<')

        elif token == '\n':
            self.next = Token(type='NEW-LINE', value='\\n')

        elif token in self.reserved_words:
            self.next = Token(type=token.upper(), value=token)

        elif token == '"':
            self.position += 1
            token = self.source[self.position]
            if token == '"':
                self.next = Token(type='STR', value='')
                return
            self.position += 1
            while self.source[self.position] != '"':
                token += self.source[self.position]
                self.position += 1
            self.next = Token(type='STR', value=token)

        elif token not in self.reserved_words:
            self.next = Token(type='IDENTIFIER', value=token)

        else:
            raise ValueError('Invalid input')
        