# DMScript Tokens
class Token:
    def __init__(self, TokenType = "", Literal = ""):
        self.TokenType = TokenType
        self.Literal = Literal
        
    def __str__(self):
        return self.TokenType

def lookupIdentifier(literal):
    if literal in keywords.keys():
        return keywords[literal]
    else:
        return IDENT


# Identifiers and Literals
ILLEGAL = "ILLEGAL"
EOF = "EOF"

IDENT = "IDENT"
INT = "INT"

# Operators
PLUS = "+"
ASSIGN = "="
MINUS = "-"
ASTERISK = "*"
SLASH = "/"
MODULO = "%"
FLOOR = "FLOOR"

EQ =  "=="
NOT_EQ = "!=" 
GT = ">"
LT = "<"

GT_EQ = ">="
LT_EQ = "<="

AND = "&&"
OR =  "||"
BANG = "!"

# Fork 
UNDERSCORE = "_"
PIPE = "->"

# Delimiters
COMMA = ","

LPAREN = "("
RPAREN = ")"

LBRACE = "{"
RBRACE = "}"

# Keywords

LET = "LET"
IF = "IF"
ELSE = "ELSE"

TRUE = "TRUE"
FALSE = "FALSE"

FUNCTION = "FUNCTION"
RETURN = "RETURN"

keywords = {
    "fn": FUNCTION,
    "let": LET,
    "true": TRUE,
    "false": FALSE,
    "if": IF,
    "else": ELSE,
    "return": RETURN
}

