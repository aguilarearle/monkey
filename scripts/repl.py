import lexer as lxr
import tokens as tkn
import parser as prsr
import threading

running = True
lexer_input = None

class bcolors:
    OKBLUE  = '\033[94m'
    OKCYAN  = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC    = '\033[0m'
    FAIL    = '\033[91m'

class Repl:

    def __init__(self):
        
        listening_thread = threading.Thread(target=self.listener)
        printing_thread = threading.Thread(target=self.lexer_printer)
        print(f"{bcolors.FAIL} H4ck3r Lang: ")
        
        listening_thread.start()
        printing_thread.start()

        listening_thread.join()
        printing_thread.join()
    
    def lexer_printer(self):
        global running, lexer_input
        while running:
            if lexer_input:
                printing = True    
                l = lxr.Lexer(lexer_input)
                p = prsr.Parser(l)

                program = p.ParseProgram()

                if len(p.Errors()) != 0:
                    self.printParserErrors(p.Errors())
                    continue
                

                while printing:
                    print(f"{bcolors.WARNING} ==> {bcolors.ENDC}{program.String()}")  
                    printing = False
                    lexer_input = None


    def listener(self): 
        global running, lexer_input
        while running:
            user_input = input()


            if user_input == "quit":
                running = False
                continue
            lexer_input = user_input                
            
            
            

            
    
