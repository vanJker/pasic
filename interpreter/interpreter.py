INTEGER, PLUS, MINUS, MUL, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'

class Token:
    def __init__(self, value_type, value):
        self.value_type = value_type    # value type of token
        self.value = value              # value of token
    
    def __str__(self) -> str:
        return 'Token({value_type}, {value})'.format(value_type=self.value_type, value=self.value)
    
    def __repr__(self) -> str:
        return self.__str__()

class Interpreter:
    def __init__(self, text: str):
        self.text = text                                # expression of input
        self.pos  = 0                                   # current position of char in text
        self.current_token: Token = None                # current token
        self.current_char: str = self.text[self.pos]    # current char
    
    def error(self):
        '''Throw error if get error input.
        '''
        raise Exception('Warning: error input!')
    
    def advance(self):
        '''Get next character from text.
        '''
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        '''Skip whitspaces in text.
        '''
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def long_integer(self):
        '''Get multi-digit integer from text.
        '''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self) -> Token:
        '''Get next token from text.
        '''
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.long_integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            self.error()
        return Token(EOF, None)

    def eat(self, token_type) -> None:
        '''match current token with given token type, and get next token.
        '''
        if self.current_token.value_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
        
    def term(self):
        '''Evaluate the term.
        '''
        term_value = self.current_token.value
        self.eat(INTEGER)
        return term_value

    def expr(self):
        '''Evaluate the expression.
        '''
        self.current_token = self.get_next_token()
        result = self.term()

        while not self.current_token.value_type == EOF:
            operator = self.current_token
            self.eat(operator.value_type)
            right = self.term()
            result = eval('{lval} {op} {rval}'.format(lval=result, op=operator.value, rval=right))
        
        return result

def main():
    while True:
        try:
            text = input(">>> ")
        except EOFError:
            break
        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print('{text} = {result}'.format(text=text, result=result))

if __name__ == '__main__':
    main()

