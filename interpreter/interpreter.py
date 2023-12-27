# Interpreter

# Identify
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

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
            digit_str = ''
            while current_char.isdigit():
                digit_str += current_char
                self.pos += 1
                try:
                    current_char = text[self.pos]
                except:
                    break            
            self.pos -= 1
            token = Token(INTEGER, int(digit_str))
        elif current_char == '+':
            token = Token(PLUS, current_char)
        elif current_char == '-':
            token = Token(MINUS, current_char)
        
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
        if operator.value_type == PLUS:
            self.eat(PLUS)
        elif operator.value_type == MINUS:
            self.eat(MINUS)

        right = self.current_token
        self.eat(INTEGER)

        result = eval('{lval} {op} {rval}'.format(lval=left.value, op=operator.value, rval=right.value))
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

