import tokens as tkn
import ast

class AstTests:

    def TestString(self):
        program = ast.Program()
        program.Statements = [
            ast.LetStatement(
                tkn.Token(tkn.LET, "let"), 
                ast.Identifier(tkn.Token(tkn.IDENT, "myVar"),"myVar"),
                ast.Identifier(tkn.Token(tkn.IDENT, "anotherVar"),"anotherVar")
            )
        ]
        

        if program.String() != "let myVar = anotherVar":
            raise Exception(f'program.String() wrong got={program.String()}')
        
 