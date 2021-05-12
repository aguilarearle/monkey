import lexerTests
import parserTests
import astTests
import repl as rp 
import sys

def main(mode):
    if mode == "l-test":
        testFramework = lexerTests.LexerTests()
        testFramework.TestNextToken()
    elif mode == "p-test":
        testFramework = parserTests.ParserTests()
        testFramework.TestStatements()
    elif mode == "a-test":
        testFramework = astTests.AstTests()
        testFramework.TestString()
    elif mode == "repl":
        print("Starting repl")
        repl = rp.Repl()
    
    else:
        print(f"Unknown mode: {mode}")

    
if __name__ == '__main__':

    if len(sys.argv) == 0:
        main("test")
    elif len(sys.argv) > 2:
        raise Exception(f'Error: Must provide one argument: "test" or "repl" to run.')
    else:
        main(sys.argv[1])
    
