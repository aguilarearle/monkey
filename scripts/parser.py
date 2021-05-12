from enum import Enum

import ast
import tokens as tkn
import lexer as lex


class Precedence(Enum):
    _ = 0
    LOWEST = 1
    EQUALS = 2 # ==
    LESSGREATER = 3 # > or < 
    SUM = 4 # + 
    PRODUCT = 5 # *
    PREFIX = 6 # -X or !X
    CALL = 7 # function()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented    

precedences = {
    tkn.EQ: Precedence.EQUALS,
    tkn.NOT_EQ: Precedence.EQUALS,
    tkn.LT: Precedence.LESSGREATER,
    tkn.GT: Precedence.LESSGREATER,
    tkn.PLUS: Precedence.SUM,
    tkn.MINUS: Precedence.SUM,
    tkn.SLASH: Precedence.PRODUCT,
    tkn.ASTERISK: Precedence.PRODUCT,
    tkn.LPAREN: Precedence.CALL

}

def prefixParseFn():
    pass

def infixParseFn():
    pass


class Parser:

    def __init__(self, lexer):
        self.l = lexer
        self.errors = []

        self.currToken = None
        self.peekToken = None
        
        self.prefixParseFns = {}
        self.infixParseFns = {}

        self.initializeTokens()


        # Prefix Expressions
        self.registerPrefix(tkn.IDENT, self.parseIdentifier)
        self.registerPrefix(tkn.INT, self.parseIntegerLiteral)
        self.registerPrefix(tkn.BANG, self.parsePrefixExpression)
        self.registerPrefix(tkn.MINUS, self.parsePrefixExpression)
        self.registerPrefix(tkn.TRUE, self.parseBoolean)
        self.registerPrefix(tkn.FALSE, self.parseBoolean)
        self.registerPrefix(tkn.LPAREN, self.parseGroupedExpression)
        self.registerPrefix(tkn.IF, self.parseIFExpression)
        self.registerPrefix(tkn.FUNCTION, self.parseFunctionLiteral)
        # Infix Expressions
        self.registerInfix(tkn.PLUS, self.parseInfixExpression)
        self.registerInfix(tkn.MINUS, self.parseInfixExpression)
        self.registerInfix(tkn.SLASH, self.parseInfixExpression)
        self.registerInfix(tkn.ASTERISK, self.parseInfixExpression)
        self.registerInfix(tkn.EQ, self.parseInfixExpression)
        self.registerInfix(tkn.NOT_EQ, self.parseInfixExpression)
        self.registerInfix(tkn.LT, self.parseInfixExpression)
        self.registerInfix(tkn.GT, self.parseInfixExpression)
        self.registerInfix(tkn.LPAREN, self.parseCallExpression)

    
    def nextToken(self):
        self.currToken = self.peekToken
        self.peekToken = self.l.NextToken()

    def initializeTokens(self):
        self.nextToken()
        self.nextToken()

    def ParseProgram(self):
        program = ast.Program()
        program.Statements = []
        
        while self.currToken.TokenType != tkn.EOF:
            statement = self.ParseStatement()
            if statement is not None:
                program.Statements.append(statement)

            self.nextToken()
        
        return program
        

    def ParseStatement(self):        
        if self.currToken.TokenType == tkn.LET:
            return self.ParseLetStatement()  
        elif    self.currToken.TokenType == tkn.RETURN:
            return self.ParseReturnStatement()  
        else:
            return self.ParseExpressionStatement()

    def ParseLetStatement(self):

        letStmt = ast.LetStatement(self.currToken, None, None)

        if not self.expectedPeekToken(tkn.IDENT):
            return None

        letStmt.Name = ast.Identifier(self.currToken,
                        self.currToken.Literal) 
        
        if not self.expectedPeekToken(tkn.ASSIGN):
            return None        
        
        self.nextToken()
        
        letStmt.Value = self.parseExpression(Precedence.LOWEST)
        
        return letStmt
    
    def ParseReturnStatement(self):
        returnStmt = ast.ReturnStatement(self.currToken)

        # TODO implement Expressions
        
        self.nextToken() ## TO move forward

        returnStmt.ReturnValue = self.parseExpression(Precedence.LOWEST)
        
        return returnStmt


    def ParseExpressionStatement(self):
        expression = self.parseExpression(Precedence.LOWEST)

        #TODO might have to check if nil expression
        stmt = ast.ExpressionStatement(self.currToken, expression)

        return stmt

    def parsePrefixExpression(self):
        expression = ast.PrefixExpression(self.currToken, self.currToken.Literal, None)

        self.nextToken()

        expression.Right = self.parseExpression(Precedence.PREFIX)

        return expression

    def parseInfixExpression(self, left):
        expression = ast.InfixExpression(self.currToken, self.currToken.Literal, left)

        precedence = self.curPrecedence()
        self.nextToken()
        expression.Right = self.parseExpression(precedence)

        return expression

    def parseIntegerLiteral(self):
        literal = ast.IntegerLiteral(self.currToken,None)
        value = int(self.currToken.Literal)

        if value == None:
            msg = f"Could not parse {self.currToken.Literal}, as integer"
            self.errors.append(msg)
            return None

        literal.Value = value 

        return literal        

    def parseExpression(self, precedence):
        if self.currToken.TokenType in self.prefixParseFns:
            prefix = self.prefixParseFns[self.currToken.TokenType]
        else:
            self.noPrefixParseFnError(self.currToken.TokenType)
            return None
        
        leftExp = prefix()

        while precedence < self.peekPrecedence():
            if self.peekToken.TokenType in self.infixParseFns:
                infix = self.infixParseFns[self.peekToken.TokenType]
            else:
                return leftExp

            self.nextToken()

            leftExp = infix(leftExp)

        return leftExp

    def parseGroupedExpression(self):
        self.nextToken()

        exp = self.parseExpression(Precedence.LOWEST)

        if not self.expectedPeekToken(tkn.RPAREN):
            return None
        
        return exp

    def parseIFExpression(self):
        ifExp = ast.IfExpression(self.currToken)

        if not self.expectedPeekToken(tkn.LPAREN):
            return None

        self.nextToken()

        ifExp.Condition = self.parseExpression(Precedence.LOWEST)

        if not self.expectedPeekToken(tkn.RPAREN):
            return None

        if not self.expectedPeekToken(tkn.LBRACE):
            return None

        ifExp.Consequence = self.parseBlockStatement()

        if self.peekTokenIs(tkn.ELSE):
            self.nextToken()

            if not self.expectedPeekToken(tkn.LBRACE):
                return None

            ifExp.Alternative = self.parseBlockStatement()

        return ifExp
        
    def parseFunctionLiteral(self):
        function = ast.FunctionLiteral(self.currToken)
        
        if not self.expectedPeekToken(tkn.LPAREN):
            return None

        function.Parameters = self.parseFunctionParameters()

        if not self.expectedPeekToken(tkn.LBRACE):
            return None        

        function.Body = self.parseBlockStatement()

        return function

    def parseFunctionParameters(self):
        parameters = []

        if self.peekTokenIs(tkn.RPAREN):
            self.nextToken()
            return parameters

        self.nextToken()
        ident = ast.Identifier(self.currToken, self.currToken.Literal)
        parameters.append(ident)

        while self.peekTokenIs(tkn.COMMA):
            self.nextToken()
            self.nextToken()
            ident = ast.Identifier(self.currToken, self.currToken.Literal)
            parameters.append(ident)

        if not self.expectedPeekToken(tkn.RPAREN):
            return None
        
        return parameters

    def parseBlockStatement(self):
        block = ast.BlockStatement(self.currToken)
        block.Statements = []

        self.nextToken()

        while not self.curTokenIs(tkn.RBRACE) and not self.curTokenIs(tkn.EOF):
            stmt = self.ParseStatement()
            if stmt is not None:
                block.Statements.append(stmt)

            self.nextToken()
        
        return block            

    def parseCallExpression(self, function):
        callExp = ast.CallExpression(self.currToken, function)
        callExp.Arguments = self.parseCallArguments()

        return callExp

    def parseCallArguments(self):
        arguments = []
        
        if self.peekTokenIs(tkn.RPAREN):
            self.nextToken()
            return arguments

        self.nextToken()
        arg = self.parseExpression(Precedence.LOWEST)
        arguments.append(arg)

        while self.peekTokenIs(tkn.COMMA):
            self.nextToken()
            self.nextToken()
            arg = self.parseExpression(Precedence.LOWEST)
            arguments.append(arg)        

        if not self.expectedPeekToken(tkn.RPAREN):
            return None
        
        return arguments

    def parseIdentifier(self):
        return ast.Identifier(self.currToken, self.currToken.Literal)

    def parseBoolean(self):
        return ast.Boolean(self.currToken, self.curTokenIs(tkn.TRUE))

    def peekTokenIs(self, token):
        return self.peekToken.TokenType == token

    def curTokenIs(self, token):
        return self.currToken.TokenType == token        

    def expectedPeekToken(self, token):
        if self.peekTokenIs(token):
            self.nextToken()
            return True
        else:
            self.peekError(token)
            return False

    def Errors(self):
        return self.errors
    
    def peekError(self, token):
        msg = f"expected next token to be {token}, got {self.peekToken.TokenType}"
        self.errors.append(msg)

    def noPrefixParseFnError(self, tokenType):
        msg = f'No prefix parse function found for {tokenType}'
        self.errors.append(msg)

    def registerPrefix(self, tokenType, fn):
        self.prefixParseFns[tokenType] = fn
    
    def registerInfix(self, tokenType, fn):
        self.infixParseFns[tokenType] = fn

    def peekPrecedence(self):
        if self.peekToken.TokenType in precedences:
            return precedences[self.peekToken.TokenType]
        
        return Precedence.LOWEST

    def curPrecedence(self):
        if self.currToken.TokenType in precedences:
            return precedences[self.currToken.TokenType]
        
        return Precedence.LOWEST
        

