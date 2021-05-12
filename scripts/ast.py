class Node:
    def TokenLiteral(self):
        pass

    def String(self):
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass


class LetStatement(Statement):
    def __init__(self, token, identifier, expression):
        self.Token = token # tkn.LET
        self.Name = identifier
        self.Value = expression
    
    def TokenLiteral(self):
        return self.Token.Literal

    def String(self):
        out = f'{self.TokenLiteral()} {self.Name.String()} = '

        if self.Value is not None:
            out += f'{self.Value.String()}'

        return out 

class BlockStatement(Statement):
    def __init__(self, token, statements = None):
        self.Token = token
        self.Statements = statements

    def TokenLiteral(self):
        return self.Token.Literal

    def String(self):
        out = ""

        for stmt in self.Statements:
            out += stmt.String()
        
        return out

class Identifier(Expression):
    def __init__(self, token, value):
        self.Token = token # tkn.IDENT
        self.Value = value

    def TokenLiteral(self):
        return self.Token.Literal

    def String(self):
        return self.Value

class ReturnStatement(Statement):
    def __init__(self, token, value = None):
        self.Token = token # tkn.RETURN
        self.ReturnValue = value
       
    def TokenLiteral(self):
        return self.Token.Literal

    def String(self):
        out = f'{self.TokenLiteral()} '
        
        if self.ReturnValue is not None:
            
            out += f'{self.ReturnValue.String()}'
        else:
            print('NUll return value')
        return out

class ExpressionStatement(Statement):
    def __init__(self, token, expression):
        self.Token = token # tkn.
        self.Expression = expression 
    
    def TokenLiteral(self):
        return self.Token.Literal     

    def String(self):
        if self.Expression is not None:
            return f'{self.Expression.String()}'     
        else:
            return ""
    
class IntegerLiteral(Expression):
    def __init__(self, token, value):
        self.Token = token # tkn.INT
        self.Value = value

    def TokenLiteral(self):
        return self.Token.Literal

    def String(self):
        return self.TokenLiteral()

class Boolean(Expression):
    def __init__(self, token, value):
        self.Token = token
        self.Value = value

    def TokenLiteral(self):
        return self.Token.Literal
    
    def String(self):
        return self.Token.Literal

class PrefixExpression(Expression):
    def __init__(self, token, operator, right):
        self.Token = token
        self.Operator = operator
        self.Right = right

    def TokenLiteral(self):
        return self.Token.Literal

    def String(self):
        return f'({self.Operator} {self.Right.String()})'

class InfixExpression(Expression):
    def __init__(self, token, operator, left = None, right = None):
        self.Token = token
        self.Operator = operator
        self.Left = left
        self.Right = right

    def TokenLiteral(self):
        return self.Token.Literal

    def String(self):
        return f'({self.Left.String()} {self.Operator} {self.Right.String()})'        

class IfExpression(Expression):
    def __init__(self, token, condition = None, consequence = None, alternative = None):
        self.Token = token
        self.Condition = condition
        self.Consequence = consequence
        self.Alternative = alternative

    def TokenLiteral(self):
        return self.Token.Literal
    
    def String(self):
        out = f'{self.TokenLiteral()} {self.Condition.String()} {self.Consequence.String()}'

        if self.Alternative is not None:
            out += f'else {self.Alternative.String()}'

class FunctionLiteral(Expression):
    def __init__(self, token, parameters = None, body = None):
        self.Token = token
        self.Parameters = parameters
        self.Body = body

    def TokenLiteral(self):
        return self.Token.Literal
    
    def String(self):
        out = f'{self.TokenLiteral()}('

        for p in self.Parameters:
            out += f'{p.String()}'

        out += '){'

        out += self.Body.String()

        out += '}'

        return out

class CallExpression(Expression):
    def __init__(self, token, function = None, arguments = None):
        self.Token = token
        self.Function = function
        self.Arguments = arguments

    def TokenLiteral(self):
        return self.Token.Literal
    
    def String(self):
        out = f'{self.TokenLiteral()} ('

        for arg in self.Arguments:
            out += f'{arg.String()}'
        
        out += ")"

        return out 


class Program:
    def __init__(self):
        self.Statements = None

    def TokenLiteral(self):
        if len(self.Statements) > 0:
            return self.Statements[0].TokenLiteral()
        else: 
            return ""

    def String(self):
        programStmts = ""

        for stmt in self.Statements:
            programStmts += stmt.String()
        
        return programStmts
