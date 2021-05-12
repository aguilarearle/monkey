import tokens as tkn
import lexer as lxr

class LexerTests:
    
    def TestNextToken(self):
        print("Running TestNextToken")
        input = """
        let five = 5
        let ten = 10

        let add = fn(x, y){
            x + y
        }

        let result = add(five, ten)

        !-/*5
        5 < 10 > 5

        if (5 < 10) {
            return true
        }else{
            return false
        }

        10 == 10
        10 != 9
        """
        testTokens = [
            (tkn.LET, "let"),
            (tkn.IDENT, "five"),
            (tkn.ASSIGN, "="),
            (tkn.INT, "5"),
            (tkn.LET, "let"),
            (tkn.IDENT, "ten"),
            (tkn.ASSIGN, "="),
            (tkn.INT, "10"),
            (tkn.LET, "let"),
            (tkn.IDENT, "add"),
            (tkn.ASSIGN, "="),
            (tkn.FUNCTION, "fn"),
            (tkn.LPAREN, "("),
            (tkn.IDENT, "x"),
            (tkn.COMMA, ","),
            (tkn.IDENT, "y"),
            (tkn.RPAREN, ")"),        
            (tkn.LBRACE, "{"),
            (tkn.IDENT, "x"),
            (tkn.PLUS, "+"),
            (tkn.IDENT, "y"),
            (tkn.RBRACE, "}"),
            (tkn.LET, "let"),
            (tkn.IDENT, "result"),
            (tkn.ASSIGN, "="),
            (tkn.IDENT, "add"),
            (tkn.LPAREN, "("),
            (tkn.IDENT, "five"),
            (tkn.COMMA, ","),
            (tkn.IDENT, "ten"),
            (tkn.RPAREN, ")"),
            (tkn.BANG, "!"),
            (tkn.MINUS, "-"),
            (tkn.SLASH, "/"),
            (tkn.ASTERISK, "*"),
            (tkn.INT, "5"),
            (tkn.INT, "5"), 
            (tkn.LT, "<"),
            (tkn.INT, "10"),
            (tkn.GT, ">"),
            (tkn.INT, "5"),
            (tkn.IF, "if"),
            (tkn.LPAREN, "("),
            (tkn.INT, "5"), 
            (tkn.LT, "<"),
            (tkn.INT, "10"),
            (tkn.RPAREN, ")"),
            (tkn.LBRACE, "{"),
            (tkn.RETURN, "return"),
            (tkn.TRUE, "true"),
            (tkn.RBRACE, "}"),
            (tkn.ELSE, "else"),
            (tkn.LBRACE, "{"),
            (tkn.RETURN, "return"),
            (tkn.FALSE, "false"),
            (tkn.RBRACE, "}"),
            (tkn.INT, "10"),
            (tkn.EQ, "=="),
            (tkn.INT, "10"),
            (tkn.INT, "10"),
            (tkn.NOT_EQ, "!="),
            (tkn.INT, "9"),
        ]

        resultTokens = []

        l = lxr.Lexer(input)

        ix = 0

        for index, tuple in enumerate(testTokens):
            key = tuple[0]
            value = tuple[1]
            tok = l.NextToken()
            resultTokens.append((tok.TokenType, tok.Literal))
            # print("key: %s, value: %s" %(key, value))
            # print("tok.TokenType: %s, tok.Literal: %s" %(tok.TokenType, tok.Literal))
            # value_hex = ":".join("{:02x}".format(ord(c)) for c in value)
            # literal_hex = ":".join("{:02x}".format(ord(c)) for c in tok.Literal)
            # print(f'value_hex: {value_hex}, literal_hex: {literal_hex}')
        
            if tok.TokenType != key:
                raise Exception(f'Test[{ix}] failed: TokenType wrong, expected: {key}, got: {tok.TokenType}')
            if tok.Literal != value:
                raise Exception(f'Test[{ix}] failed: Literal wrong, expected: {value}, got: {tok.Literal}')
            ix += 1
        
        print(resultTokens)
        
        

