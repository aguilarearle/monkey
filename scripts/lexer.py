import tokens as tkn

class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0
        self.readPosition = 0
        self.ch = None
        self.readChar()
    
    def skipWhiteSpace(self):
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
                self.readChar()
        
    def readChar(self):
        if self.readPosition >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.readPosition]
        
        self.position = self.readPosition
        self.readPosition += 1

    def peekChar(self):
        if self.readPosition >= len(self.input):
            return 0
        else: 
            return self.input[self.readPosition]
    

    def readIdentifier(self):
        # An identifier is a name assigned to an element
        # in a program.
        position = self.position
        while self.ch != 0 and self.ch.isalpha():
            self.readChar()
        return self.input[position: self.readPosition - 1]
    
    def readDigit(self):
        position = self.position
        while self.ch != 0 and self.ch.isdigit(): 
            self.readChar()
        return self.input[position: self.readPosition - 1]
        
    def NextToken(self):
        
        tok = None

        self.skipWhiteSpace()
        if self.ch == "+":
            tok = tkn.Token(tkn.PLUS, self.ch)
        elif self.ch == "-":
            tok = tkn.Token(tkn.MINUS, self.ch)
        elif self.ch == "*":
            tok = tkn.Token(tkn.ASTERISK, self.ch)
        elif self.ch == "/":
            tok = tkn.Token(tkn.SLASH, self.ch)
        elif self.ch == "=":
            if self.peekChar() == "=":
                tok = tkn.Token(tkn.EQ, "==")
                self.readChar()
            else:
                tok = tkn.Token(tkn.ASSIGN, self.ch)
        elif self.ch == "!":
            if self.peekChar() == "=":
                tok = tkn.Token(tkn.NOT_EQ, "!=")
                self.readChar()
            else:
                tok = tkn.Token(tkn.BANG, self.ch)
        elif self.ch == "<":
            tok = tkn.Token(tkn.LT, self.ch)                            
        elif self.ch == ">":
            tok = tkn.Token(tkn.GT, self.ch)                                        
        elif self.ch == ",":
            tok = tkn.Token(tkn.COMMA, self.ch)            
        elif self.ch == "{":
            tok = tkn.Token(tkn.LBRACE, self.ch)
        elif self.ch == "}":
            tok = tkn.Token(tkn.RBRACE, self.ch)
        elif self.ch == "(":
            tok = tkn.Token(tkn.LPAREN, self.ch)
        elif self.ch == ")":
            tok = tkn.Token(tkn.RPAREN, self.ch)
        elif self.ch == 0:
            tok = tkn.Token(tkn.EOF, "")
        else:
            if self.ch.isalpha():
                literal = self.readIdentifier()
                tokenType = tkn.lookupIdentifier(literal)
                tok = tkn.Token(tokenType, literal)
                return tok
            elif self.ch.isdigit():
                literal = self.readDigit()
                tok = tkn.Token(tkn.INT, literal)
                return tok
            else:
                tok = tkn.Token(tkn.ILLEGAL, self.ch)
        
        self.readChar()
        return tok
