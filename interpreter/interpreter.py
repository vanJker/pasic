# Interpreter

# Identify
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token:
    def __init__(self, value_type, value) -> None:
        self.value_type = value_type    # value type of token
        self.value = value              # value of token
    
    def __str__(self) -> str:
        return 'Token({value_type}, {value})'.format(value_type=self.value_type, value=self.value)
    
    def __repr__(self) -> str:
        return self.__str__()

class Interpreter:
    def __init__(self, text: str) -> None:
        self.text = text                    # expression of input
        self.pos  = 0                       # current position of char in text
        self.current_token: Token = None    # current token
    
    def error(self):
        '''Throw error if get error input.
        '''
        raise Exception('Warning: error input!')

    def get_next_token(self) -> Token:
        '''Get next token from text.
        '''
        text = self.text
        if self.pos >= len(text):
            return Token(EOF, None)
        
        current_char = text[self.pos]
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
        elif current_char == '+':
            token = Token(PLUS, current_char)
        
        self.pos += 1
        return token

    def eat(self, token_type) -> None:
        '''match current token with given token type, and get next token.
        '''
        if self.current_token.value_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        '''Evaluate expression.
        '''
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)

        operator = self.current_token
        self.eat(PLUS)

        right = self.current_token
        self.eat(INTEGER)

        result = left.value + right.value
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

