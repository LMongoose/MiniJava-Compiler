# Native Modules
import sys
# Downloaded Modules

# Custom Modules
from lexicalanalyzer import LexicalAnalyzer
from semanticanalyzer import SemanticAnalyzer
#from symboltable import SymbolTable
from errorhandler import SyntaxParsingError
import main

class Parser():
    def __init__(self):
        self.tokens = []
        self.token = None
        self.lastpos = 0
        #self.currentscope = None
        self.currentexp = []

    def searchToken(self):
        if((self.lastpos >= 0) and (self.lastpos <= len(self.tokens)-1)):
            _token = self.tokens[self.lastpos]
            self.lastpos += 1
            self.token = _token
        elif(self.lastpos > len(self.tokens)):
            self.token = "<EOF>"

    def returnToken(self):
        self.lastpos -= 1
        self.token = self.tokens[self.lastpos]


class PRP(Parser):
    def __init__(self):
        Parser.__init__(self)

    def parse(self, p_tokenlist):
        self.tokens = p_tokenlist
        self.validateProgram()

    def validateProgram(self): 
        self.searchToken()
        if(self.token.type == "T#CLASS"):
            self.searchToken()
            if(self.token.type == "T#IDENTIFIER"):
                ## TODO: add to symboltable (main class identifier)
                self.searchToken()
                if(self.token.type == "T#LEFT_BRACKET"):
                    self.validateMain()
                else:
                    raise SyntaxParsingError("Missing \"{\"", self.token.line, self.token.column)
            else:
                raise SyntaxParsingError("Missing an \"identifier\"", self.token.line, self.token.column)
        else:
            raise SyntaxParsingError("Missing \"class\"", self.token.line, self.token.column)

    def validateMain(self):
        self.searchToken()
        if(self.token.type == "T#PUBLIC"):
            self.searchToken()
            if(self.token.type == "T#STATIC"):
                self.searchToken()
                if(self.token.type == "T#VOID"):
                    self.searchToken()
                    if(self.token.type == "T#MAIN"):
                        self.searchToken()
                        if(self.token.type == "T#LEFT_PARENTHESIS"):
                            self.searchToken()
                            if(self.token.type == "T#STRING"):
                                self.searchToken()
                                if(self.token.type == "T#LEFT_SQUARE_BRACKET"):
                                    self.searchToken()
                                    if(self.token.type == "T#RIGHT_SQUARE_BRACKET"):
                                        self.searchToken()
                                        if(self.token.type == "T#IDENTIFIER"):
                                            ## TODO: add to symboltable (main identifier)
                                            self.searchToken()
                                            if(self.token.type == "T#RIGHT_PARENTHESIS"):
                                                self.searchToken()
                                                if(self.token.type == "T#LEFT_BRACKET"):
                                                    self.validateBlock()
                                                else:
                                                    raise SyntaxParsingError("Missing \"{\"", self.token.line, self.token.column)
                                            else:
                                                raise SyntaxParsingError("Missing \")\"", self.token.line, self.token.column)
                                        else:
                                            raise SyntaxParsingError("Missing an \"identifier\"", self.token.line, self.token.column)
                                    else:
                                        raise SyntaxParsingError("Missing \"]\"", self.token.line, self.token.column)
                                else:
                                    raise SyntaxParsingError("Missing \"[\"", self.token.line, self.token.column)
                            else:
                                raise SyntaxParsingError("Missing \"String\"", self.token.line, self.token.column)
                        else:
                            raise SyntaxParsingError("Missing \"(\"", self.token.line, self.token.column)
                    else:
                        raise SyntaxParsingError("Missing \"main\"", self.token.line, self.token.column)
                else:
                    raise SyntaxParsingError("Missing \"void\"", self.token.line, self.token.column)
            else:
                raise SyntaxParsingError("Missing \"static\"", self.token.line, self.token.column)
        else:
            raise SyntaxParsingError("Missing \"public\"", self.token.line, self.token.column)

    def validateBlock(self):
        self.searchToken()
        while(self.token.type == "T#RIGHT_BRACKET"):
            self.searchToken()
            if((self.token.type == "T#TYPE_BOOLEAN") or (self.token.type == "T#TYPE_INTEGER")):
                self.validateVariableDeclaration()
            elif(self.token.type == "T#SYSTEM"):
                self.validateCommand()

    def validateVariableDeclaration(self):
        if((self.token.type == "T#TYPE_BOOLEAN") or (self.token.type == "T#TYPE_INTEGER")):
            self.validateAttribution()
        else:
            raise SyntaxParsingError("Missing variable type.", self.token.line, self.token.column)

    def validateAttribution(self):
        self.searchToken()
        if(self.token.type == "T#IDENTIFIER"):
            ## TODO: 
            #   add in symboltable if is new variable / search in symboltable if is only attribution
            #   add token in symboltable with datatype, scope and value and save symboltable position in token
            self.searchToken()
            if(self.token.type == "T#ATTRIBUTION"):
                self.searchToken()
                self.validateExpression()
            else:
                raise SyntaxParsingError("Missing \"=\"", self.token.line, self.token.column)
        else:
            raise SyntaxParsingError("Missing an \"identifier\"", self.token.line, self.token.column)

    def validateCommand(self):
        if(self.token.type == "T#SYSTEM"):
            self.searchToken()
            if(self.token.type == "T#DOT"):
                self.searchToken()
                if(self.token.type == "T#OUT"):
                    self.searchToken()
                    if(self.token.type == "T#DOT"):
                        self.validatePrint()
                    else:
                        raise SyntaxParsingError("Missing a \".\"", self.token.line, self.token.column)
                #elif(self.token.type == "T#IN"):
                #    self.searchToken()
                #    if(self.token.type == "T#DOT"):
                #        self.validateRead()
                else:
                    raise SyntaxParsingError("Missing an \"out\"", self.token.line, self.token.column)
            else:
                raise SyntaxParsingError("Missing a \".\"", self.token.line, self.token.column)
        #elif:
        #   HANDLE FUTURE COMMANDS (if, else, while, not, ....)
        else:
            raise SyntaxParsingError("Missing a command", self.token.line, self.token.column)

    def validatePrint(self):
        self.searchToken()
        if(self.token.type == "T#PRINT"):
            self.searchToken()
            if(self.token.type == "T#LEFT_PARENTHESIS"):
                self.searchToken()
                self.validateExpression()
                self.searchToken()
                if(self.token.type == "T#RIGHT_PARENTHESIS"):
                    return
                else:
                    raise SyntaxParsingError("Missing an \")\"", self.token.line, self.token.column)
            else:
                raise SyntaxParsingError("Missing an \"(\"", self.token.line, self.token.column)
        else:
            raise SyntaxParsingError("Missing an \"println\"", self.token.line, self.token.column)

    def validateExpression(self):
        self.currentexp = []
        self.validateTerm()
        self.searchToken()
        if(not(self.token.type in ["T#MULTSUMIPLICATION", "T#SUBTRACTION"])):
            raise SyntaxParsingError("Missing an sum or subtraction operator", self.token.line, self.token.column)
        self.validateTerm()
        main.validator.validateTypeCompatibility(self.currentexp)

    def validateTerm(self):
        self.validateFactor()
        self.searchToken()
        if(not(self.token.type in ["T#MULTIPLICATION", "T#DIVISION"])):
            raise SyntaxParsingError("Missing an multiplication or division operator", self.token.line, self.token.column)
        self.validateFactor()

    def validateFactor(self):
        self.searchToken()
        if(self.token.type == "T#LEFT_PARENTHESIS"):
            self.validateClosedExpression()
        elif(self.token.type == "T#IDENTIFIER"):
            self.currentexp.append(self.token)
            ## TODO: search in symboltable and pass the value attributed to the identifier
            return
        elif(self.token.type == "T#POSITIVE_INTEGER"):
            self.currentexp.append(self.token)
        else:
            raise SyntaxParsingError("Invalid value in expression, expected identifier or number", self.token.line, self.token.column)

    def validateClosedExpression(self):
        if(self.token.type == "T#LEFT_PARENTHESIS"):
            self.validateExpression()
            self.searchToken()
            if(not (self.token.type == "T#RIGHT_PARENTHESIS")):
                raise SyntaxParsingError("Missing an \")\"", self.token.line, self.token.column)
        else:
            raise SyntaxParsingError("Missing an \"(\"", self.token.line, self.token.column)


if(__name__ == "__main__"):
    def printSymbolTable(p_symboltable):
        print()
        print("Symbol Table:")
        print("TOKENTYPE, TOKENLEXEM, TOKENSCOPE")
        for data in p_symboltable:
            print(data.type +", "+ data.lexem + ", " + data.scope)

    try:
        table = []
        lexer = LexicalAnalyzer()
        tokenlist = lexer.tokenize(sys.argv[1])
        parser = PRP()
        parser.parse(tokenlist)
        print(sys.argv[1] + " is a valid program.")
        printSymbolTable(table)
    except IndexError:
        print("Missing target source file.")
        print("Usage:")
        print(" -> python parser.py <SOURCE_TO_READ>")
        print(" -> py parser.py <SOURCE_TO_READ>")