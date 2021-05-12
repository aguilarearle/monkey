import parser as prsr
import ast
import lexer as lxr
from dataclasses import dataclass
from typing import List



class ParserTests:

    def TestStatements(self):
        print("Running TestStatements ...")
        self.TestLetStatements()
        self.TestReturnStatements()
        self.TestIdentifierExpressions()
        self.TestIntegerLiteralExpressions()
        self.TestPrefixOperatorExpression()
        self.TestParsingInfixExpression()
        self.TestOperatorPrecedence()
        self.TestBooleanExpressions()
        self.TestIfExpressions()
        self.TestIfElseExpressions()

        self.TestFunctionLiteralParsing()
        self.TestFunctionParameterParsing()
        self.TestCallExpressionParsing()

    def TestLetStatements(self):
        print("Running TestLetStatements ...")
        @dataclass
        class test:
            input: str
            expectedIdentifier: str
            expectedValue: object

        tests = [
            test("let x = 5", "x", 5),
            test("let y = true", "y", True),
            test("let foobar = y", "foobar", "y"),

        ]


        for tt in tests:

            l = lxr.Lexer(tt.input)
            p = prsr.Parser(l)

            program = p.ParseProgram()
            self.checkParsersErrors(p)

            if program is None:
                raise Exception('ParseProgram() returned None')
        
            if len(program.Statements) != 1:
                raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

            stmt = program.Statements[0]

            if not self.testLetStatement(stmt, tt.expectedIdentifier):
                return

            val = stmt.Value

            if not self.testLiteralExpression(val, tt.expectedValue):
                return 


    def TestReturnStatements(self):
        print("Running TestReturnStatements ...")        

        @dataclass
        class test:
            input: str
            expectedValue: object

        tests = [
            test("return 5", 5),
            test("return true", True),
            test("return y", "y"),

        ]  

        for tt in tests:         
            l = lxr.Lexer(tt.input)
            p = prsr.Parser(l)

            program = p.ParseProgram()
            self.checkParsersErrors(p)

            if program is None:
                raise Exception('ParseProgram() returned None')
        
            if len(program.Statements) != 1:
                raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')
        
            stmt = program.Statements[0]
            if not self.testReturnStatement(stmt):
                return 

            val = stmt.Value
            if not self.testLiteralExpression(val, tt.expectedValue):
                return
            
               

    def TestIdentifierExpressions(self):
        print("Running TestIdentifierExpressions ...")
        input = """
        foobar
        """     

        l = lxr.Lexer(input)
        p = prsr.Parser(l)

        program = p.ParseProgram()
        self.checkParsersErrors(p)

        if len(program.Statements) != 1:
            raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

        stmt = program.Statements[0]
        if not isinstance(stmt, ast.ExpressionStatement):
            raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')        
                
        
        ident = stmt.Expression
        if not isinstance(ident, ast.Identifier):
            raise Exception(f'Expression is not a ast.Identifier got={stmt.Expression}')        

        if ident.Value != "foobar":
            raise Exception(f'ident.Value is not foobar got={ident.Value}')

        if ident.TokenLiteral() != "foobar":
            raise Exception(f'ident.TokenLiteral() is not foobar got={ident.TokenLiteral()}')            


    def TestBooleanExpressions(self):
        print("Running TestBooleanExpressions ...")
        input = """
        true
        """     

        l = lxr.Lexer(input)
        p = prsr.Parser(l)

        program = p.ParseProgram()
        self.checkParsersErrors(p)

        if len(program.Statements) != 1:
            raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

        stmt = program.Statements[0]
        if not isinstance(stmt, ast.ExpressionStatement):
            raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')        
                
        
        ident = stmt.Expression
        if not isinstance(ident, ast.Boolean):
            raise Exception(f'Expression is not a ast.Boolean got={stmt.Expression}')        

        if ident.Value != True:
            raise Exception(f'ident.Value is not True got={ident.Value}')

        if ident.TokenLiteral() != "true":
            raise Exception(f'ident.TokenLiteral() is not True got={ident.TokenLiteral()}')           

    def TestIntegerLiteralExpressions(self):
        print("Running TestIntegerLiteralExpressions ...")
        input = """
        5
        """

        l = lxr.Lexer(input)
        p = prsr.Parser(l)

        program = p.ParseProgram()
        self.checkParsersErrors(p)

        if len(program.Statements) != 1:
            raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

        stmt = program.Statements[0]
        if not isinstance(stmt, ast.ExpressionStatement):
            raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')        
                
        
        literal = stmt.Expression
        if not isinstance(literal, ast.IntegerLiteral):
            raise Exception(f'Expression is not a ast.Identifier got={stmt.Expression}')        

        if literal.Value != 5:
            raise Exception(f'ident.Value is not 5 got={literal.Value}')

        if literal.TokenLiteral() != "5":
            raise Exception(f'ident.TokenLiteral() is not "5" got={literal.TokenLiteral()}')                    

    def TestPrefixOperatorExpression(self):
        print("Running TestPrefixOperatorExpression ...")
        @dataclass
        class PrefixTest:
            input: str
            operator: str
            integerValue: int

        testPrefixes = [
            PrefixTest("!5", "!", 5),
            PrefixTest("-15", "-", 15)
        ]

        for testPrefix in testPrefixes:

            l = lxr.Lexer(testPrefix.input)
            p = prsr.Parser(l)

            program = p.ParseProgram()
            self.checkParsersErrors(p)

            if len(program.Statements) != 1:
                raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

            stmt = program.Statements[0]
            if not isinstance(stmt, ast.ExpressionStatement):
                raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')        
                

            prefixExp = stmt.Expression
            if not isinstance(prefixExp, ast.PrefixExpression):
                raise Exception(f'Expression is not a ast.PrefixExpression got={stmt.Expression}')                  
            
            if prefixExp.Operator != testPrefix.operator:
                raise Exception(f'Prefix expression operator not {testPrefix.operator} got={prefixExp.Operator}')

            if not self.testIntegerLiteral(prefixExp.Right, testPrefix.integerValue):
                return

    def TestParsingInfixExpression(self):
        print("Running TestParsingInfixExpression ...")
        @dataclass
        class InfixTest:
            input: str
            leftValue: int
            operator: str
            rightValue: int

        testInfixes = [
            InfixTest("5 + 5" , 5, "+" , 5),
            InfixTest("5 - 5" , 5, "-" , 5),
            InfixTest("5 * 5" , 5, "*" , 5),
            InfixTest("5 / 5" , 5, "/" , 5),
            InfixTest("5 > 5" , 5, ">" , 5),
            InfixTest("5 < 5" , 5, "<" , 5),
            InfixTest("5 == 5", 5, "==", 5),
            InfixTest("5 != 5", 5, "!=", 5),
            InfixTest("true == true" , True, "==", True),
            InfixTest("true != false", True, "!=", False),
            InfixTest("false == false", False, "==", False),
        ]

        for testInfix in testInfixes:
            l = lxr.Lexer(testInfix.input)
            p = prsr.Parser(l)

            program = p.ParseProgram()
            self.checkParsersErrors(p)

            if len(program.Statements) != 1:
                raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

            stmt = program.Statements[0]

            if not self.testInfixExpression(stmt.Expression, testInfix.leftValue, testInfix.operator, testInfix.rightValue):
                return


    def TestOperatorPrecedence(self):
        @dataclass
        class test:
            input: str
            expected: str
        
        tests = [
            test(
                "-a + b",
                "((- a) + b)"
            ),
            test(
                "!-a",
                "(! (- a))"
            ),
            test(
                "a + b + c",
                "((a + b) + c)"
            ),
            test(
                "a + b - c",
                "((a + b) - c)"
            ),     
            test(
                "a * b * c",
                "((a * b) * c)"
            ),
            test(
                "a * b / c",
                "((a * b) / c)"
            ),
            test(
                "a + b / c",
                "(a + (b / c))"
            ),   
            test(
                "5 > 4 == 3 < 4",
                "((5 > 4) == (3 < 4))"
            ),
            test(
                "5 > 4 != 3 < 4",
                "((5 > 4) != (3 < 4))"
            ),
            test(
                "3 + 4 * 5 == 3 * 1 + 4 * 5",
                "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"
            ),
            test(
                "true",
                "true"
            ),
            test(
                "false",
                "false"
            ),
            test(
                "3 > 5 == false",
                "((3 > 5) == false)"
            ),
            test(
                "3 < 5 == true",
                "((3 < 5) == true)"
            ),
            test(
                "1 + (2 + 3) + 4",
                "((1 + (2 + 3)) + 4)"
            ),
            test(
                "(5 + 5) * 2",
                "((5 + 5) * 2)"
            ),
            test(
                "2 / (5 + 5)",
                "(2 / (5 + 5))"
            ),
            test(
                "-(5 + 5)",
                "(- (5 + 5))"
            ),
            test(
                "!(true == true)",
                "(! (true == true))"
            )  
        ]

        for tt in tests:
            l = lxr.Lexer(tt.input)
            p = prsr.Parser(l)

            program = p.ParseProgram()
            self.checkParsersErrors(p) 

            actual = program.String()

            if actual != tt.expected:
                raise Exception(f'expected = {tt.expected}, got = {actual}')

    def TestIfExpressions(self):
        print("Running TestIfExpressions ...")
        input = """
        if (x < y){ x }
        """     

        l = lxr.Lexer(input)
        p = prsr.Parser(l)

        program = p.ParseProgram()
        self.checkParsersErrors(p)

        if len(program.Statements) != 1:
            raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

        stmt = program.Statements[0]
        if not isinstance(stmt, ast.ExpressionStatement):
            raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')

        exp = stmt.Expression
        if not isinstance(exp, ast.IfExpression):
            raise Exception(f'stmt.Expression is not a ast.IfExpression got={stmt.Expression}')

        if not self.testInfixExpression(exp.Condition, "x", "<", "y"):
            return
        
        if len(exp.Consequence.Statements) != 1:
            raise Exception(f'exp.Consequence.Statements does not contain 1 statement, got={len(exp.Consequence.Statements)}')

        consequence = exp.Consequence.Statements[0]

        if not isinstance(consequence, ast.ExpressionStatement):
            raise Exception(f'consequence is not a ast.ExpressionStatement got={exp.Consequence.Statements[0]}')
        
        if not self.testIdentifier(consequence.Expression, "x"):
            return
        
        if exp.Alternative is not None:
            raise Exception(f'exp.Alternative is not None got={exp.Alternative}')


    def TestIfElseExpressions(self):
        print("Running TestIfElseExpressions ...")
        input = """
        if (x < y){ x } else { y }
        """     

        l = lxr.Lexer(input)
        p = prsr.Parser(l)

        program = p.ParseProgram()
        self.checkParsersErrors(p)

        if len(program.Statements) != 1:
            raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

        stmt = program.Statements[0]
        if not isinstance(stmt, ast.ExpressionStatement):
            raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')

        exp = stmt.Expression
        if not isinstance(exp, ast.IfExpression):
            raise Exception(f'stmt.Expression is not a ast.IfExpression got={stmt.Expression}')
   
        if not self.testInfixExpression(exp.Condition, "x", "<", "y"):
            return
        
        if len(exp.Consequence.Statements) != 1:
            raise Exception(f'exp.Consequence.Statements does not contain 1 statement, got={len(exp.Consequence.Statements)}')

        consequence = exp.Consequence.Statements[0]

        if not isinstance(consequence, ast.ExpressionStatement):
            raise Exception(f'consequence is not a ast.ExpressionStatement got={exp.Consequence.Statements[0]}')
        
        if not self.testIdentifier(consequence.Expression, "x"):
            return

        if len(exp.Alternative.Statements) != 1:
            raise Exception(f'exp.Alternative.Statements does not contain 1 statement, got={len(exp.Alternative.Statements)}')

        alternative = exp.Alternative.Statements[0]

        if not isinstance(alternative, ast.ExpressionStatement):
            raise Exception(f'consequence is not a ast.ExpressionStatement got={exp.Alternative.Statements[0]}')
        
        if not self.testIdentifier(alternative.Expression, "y"):
            return

    def TestFunctionLiteralParsing(self):
        print("Running TestFunctionLiteralParsing ...")
        input = """
        fn(x, y){ x + y }
        """       
        
        l = lxr.Lexer(input)
        p = prsr.Parser(l)

        program = p.ParseProgram()
        self.checkParsersErrors(p)

        if len(program.Statements) != 1:
            raise Exception(f'program.Statements does not contain 1 statements. got={len(program.Statements)}')

        stmt = program.Statements[0]
        if not isinstance(stmt, ast.ExpressionStatement):
            raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')        

        function = stmt.Expression
        if not isinstance(function, ast.FunctionLiteral):
            raise Exception(f'stmt.Expression is not a ast.FunctionLiteral got={stmt.Expression}')            

        if len(function.Parameters) != 2:
            raise Exception(f'function.Parameters does not contain 2 paramters got={len(function.Parameters)}')

        self.testLiteralExpression(function.Parameters[0], 'x')
        self.testLiteralExpression(function.Parameters[1], 'y')

        if len(function.Body.Statements) != 1:
            raise Exception(f'function.Body does not contain 1 statement got={len(function.Body)}')

        bodyStmt = function.Body.Statements[0]

        if not isinstance(bodyStmt, ast.ExpressionStatement):
            raise Exception(f'bodyStmt is not a ast.ExpressionStatement got={bodyStmt}')        
        
        self.testInfixExpression(bodyStmt.Expression, "x", "+", "y")

    def TestFunctionParameterParsing(self):
        @dataclass
        class test:
            input: str
            expectedParams: List[str]
        
        tests = [
            test("fn() {}",[]),
            test("fn(x) {}",['x']),
            test("fn(x, y, z) {}",['x', 'y', 'z'])
        ]

        for tt in tests:
            l = lxr.Lexer(tt.input)
            p = prsr.Parser(l)

            program = p.ParseProgram()
            self.checkParsersErrors(p)     

            stmt = program.Statements[0]       

            if not isinstance(stmt, ast.ExpressionStatement):
                raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')
            
            function = stmt.Expression

            if len(function.Parameters) != len(tt.expectedParams):
                raise Exception(f'function.Parameters does not contain {len(tt.expectedParams)} parameters got {len(function.Parameters)}')

            ix = 0
            for p in tt.expectedParams:
                self.testLiteralExpression(function.Parameters[ix], p)
                ix += 1

    def TestCallExpressionParsing(self):
        print("Running TestCallExpressionParsing ...")
        input = """
        add(1, 2 * 3, 4 + 5)
        """     
        
        l = lxr.Lexer(input)
        p = prsr.Parser(l)

        program = p.ParseProgram()
        self.checkParsersErrors(p)

        if len(program.Statements) != 1:
            raise Exception(f'program.Statements does not contain 1 statement got={len(program.Statements)}')

        stmt = program.Statements[0]
        if not isinstance(stmt, ast.ExpressionStatement):
            raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')        

        funcCall = stmt.Expression
        if not isinstance(funcCall, ast.CallExpression):
            raise Exception(f'stmt.Expression is not a ast.CallExpression got={stmt.Expression}') 

        if not self.testIdentifier(funcCall.Function, "add"):
            return 

        if len(function.Arguments) != 3:
            raise Exception(f'function.Arguments does not contain 3 statements got={stmt.Expression}') 

        self.testLiteralExpression(function.Arguments[0],1)
        self.testInfixExpression(function.Arguments[1], 2, "*", 3)
        self.testInfixExpression(function.Arguments[2], 4, "+", 5)

    def TestCallExpressionParsing(self):
        @dataclass
        class test:
            input: str
            expectedParams: List[int]
            paramType: List[str]
        
        tests = [
            test("add()",[], []),
            test("add(1)",[1], ["Literal"]),
            test("add(1, 2 * 3, 4 + 5)",[1, (2, '*', 3),  (4, '+', 5)], ["Literal", "Infix", "Infix"])
        ]
        for tt in tests:
            l = lxr.Lexer(tt.input)
            p = prsr.Parser(l)

            program = p.ParseProgram()
            self.checkParsersErrors(p)     

            stmt = program.Statements[0]       

            if not isinstance(stmt, ast.ExpressionStatement):
                raise Exception(f'statement is not a ast.ExpressionStatement got={program.Statements[0]}')
            
            funcCall = stmt.Expression

            if not isinstance(funcCall, ast.CallExpression):
                raise Exception(f'stmt.Expression is not a ast.CallExpression got={stmt.Expression}')             

            if not self.testIdentifier(funcCall.Function, "add"):
                return 

            if len(funcCall.Arguments) != len(tt.expectedParams):
                raise Exception(f'function.Arguments does not contain {len(tt.expectedParams)} statements got={len(funcCall.Arguments)}') 
            
            
            ix = 0
            for param in tt.expectedParams:
                if tt.paramType[ix] == "Literal":
                    self.testLiteralExpression(funcCall.Arguments[ix], param)
                elif tt.paramType[ix] == "Infix":
                  self.testInfixExpression(funcCall.Arguments[ix], param[0], param[1], param[2])  
                ix += 1
        
    # def TestOperatorPrecedence(self):
    #     @dataclass
    #     class test:
    #         input: str
    #         expected: str
        
    #     tests = [
    #         test("a + add(b * c) + d", 
    #              "((a + add((b * c))) + d)"),
    #         test("add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))", 
    #              "add(a, b, 1, (2 * 3), (4, + 5), add(6, (7 * 8)))"),
    #         test("add(a + b +  c * d / f + g)",
    #              "add((((a + b) + ((c * d) / f)) + g))")                 
    #     ]

    def testLiteralExpression(self, exp, expected):
        if isinstance(expected, bool):
            return self.testBooleanLiteral(exp, expected)
        elif isinstance(expected, str):
            return self.testIdentifier(exp, expected)
        elif isinstance(expected, int):
            return self.testIntegerLiteral(exp, expected)
        else:
            raise Exception(f'type of exp not handled got {exp}')
    

    def testInfixExpression(self, exp, left, operator, right):
        if not isinstance(exp, ast.InfixExpression):
            raise Exception(f'exp is not ast.InfixExpression got={exp}')

        if not self.testLiteralExpression(exp.Left, left):
            return False

        if exp.Operator != operator:
            raise Exception(f'exp.Operator not {operator} got={exp.Operator}')
        
        if not self.testLiteralExpression(exp.Right, right):
            return False

        return True

    def testIntegerLiteral(self, expression, value):

        if not isinstance(expression, ast.IntegerLiteral):
            raise Exception(f'Expression is not a ast.IntegerLiteral got={expression}')

        if expression.Value != value:
            raise Exception(f'expression.Value is not {value} got={expression.Value}')        
            
        if expression.TokenLiteral() != str(value):
            raise Exception(f'expression.TokenLiteral() is not {value} got={expression.TokenLiteral()}') 

        return True

    def testBooleanLiteral(self, exp, value):
        if not isinstance(exp, ast.Boolean):
            raise Exception(f'Expression is not a ast.IntegerLiteral got={exp}')
        
        if exp.Value != value:
            raise Exception(f'exp.Value is not {value} got={exp.Value}')        
            
        if exp.TokenLiteral() != str(value).lower():
            raise Exception(f'exp.TokenLiteral() is not {value} got={exp.TokenLiteral()}') 

        return True

    def testIdentifier(self, exp, value):
        if not isinstance(exp, ast.Identifier):
            raise Exception(f'Expression is not a ast.Identifier, got={exp}')
        
        if exp.Value != value:
            raise Exception(f'Expression.Value is not {value} got={exp.Value}')

        if exp.TokenLiteral() != value:
            raise Exception(f'Expression.TokenLiteral() is not {value} got={exp.TokenLiteral()}')

        return True


    def checkParsersErrors(self, p):
        errors = p.Errors()
        if len(errors) == 0:
            return
        print(f'parser has {len(errors)}')

        for error in errors:
            print(f'parser error: {error}')
        

    def testReturnStatement(self, returnStmt):
        if not isinstance(returnStmt, ast.ReturnStatement):
            raise Exception(f'statement is not a ast.PopStatement got={returnStmt}') 

        if returnStmt.TokenLiteral() != "return":
            raise Exception(f'Statement literal not "pop" got={returnStmt.TokenLiteral()}')
            

    def testLetStatement(self, letStmt, name):
        
        if not isinstance(letStmt, ast.LetStatement):
            raise Exception(f'Statement is not a Variable statement got={s}') 
        
        if letStmt.Name.Value != name:
            raise Exception(f'Variable statement not {name} got {letStmt.Name.Value} instead.')

        if letStmt.Name.TokenLiteral() != name:
            raise Exception(f'Variable statement literal not {name} got {letStmt.Name.TokenLiteral()} instead.')
        
        return True
