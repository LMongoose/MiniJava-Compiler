# Native Modules
import sys
# Downloaded Modules

# Custom Modules
from lexicalanalyzer import LexicalAnalyzer
#from symboltable import SymbolTable


class Parser(object):
    def __init__(self, p_symboltable, p_lexer):
        self.symboltable = p_symboltable
        self.lexer = p_lexer
        self.token = None
        self.tokens = []
        self.lastpos = 0
        #self.currentscope = None
        self.finalerror = []

    def searchToken(self):
        if((self.lastpos >= 0) and (self.lastpos <= len(self.tokens)-1)):
            _token = self.tokens[self.lastpos]
            self.lastpos += 1
            self.token = _token
        elif(self.lastpos > len(self.tokens)):
            self.token = "<EOF>"

    def error(self, p_message, p_line, p_column):
        # handle errors
        self.finalerror.append(p_message + " at line " + str(p_line) + " and column " + str(p_column))


class PRP(Parser):
    def __init__(self, p_symboltable, p_lexer):
        Parser.__init__(self, p_symboltable, p_lexer)

    def parse(self):
        self.tokens = self.lexer.tokenize()
        if(self.validateProgram()):
            return True
        else:
            print("Error parsing the source file.")
            print("Traceback:")
            for e in self.finalerror:
                print("|- " + e)
            print()
            return False

    def validateProgram(self): 
        # <T#CLASS> <T#IDENTIFIER> <T#LEFT_BRACKET> <validateMain> <T#RIGHT_BRACKET>
        self.searchToken()
        if(self.token.type == "T#CLASS"):
            self.searchToken()
            if(self.token.type == "T#IDENTIFIER"):
                self.searchToken()
                if(self.token.type == "T#LEFT_BRACKET"):
                    #self.searchToken()
                    if(self.validateMain()):
                        self.searchToken()
                        if(self.token.type == "T#RIGHT_BRACKET"):
                            return True
                        else:
                            self.error("Missing \"}\"", self.token.line, self.token.column)
                    else:
                        self.error("Main program is not valid", self.token.line, self.token.column)
                else:
                    self.error("Missing \"{\"", self.token.line, self.token.column)
            else:
                self.error("Missing an \"identifier\"", self.token.line, self.token.column)
        else:
            self.error("Missing \"class\"", self.token.line, self.token.column)
        return False

    def validateMain(self):
        # <T#PUBLIC> <T#STATIC> <T#VOID> <T#MAIN> <T#LEFT_PARENTHESIS> <T#STRING> <T#LEFT_SQUARE_BRACKET> <T#RIGHT_SQUARE_BRACKET> <T#IDENTIFIER> <T#RIGHT_PARENTHESIS> <validateBlock>
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
                                            self.searchToken()
                                            if(self.token.type == "T#RIGHT_PARENTHESIS"):
                                                #self.searchToken()
                                                if(self.validateBlock()):
                                                    return True
                                                else:
                                                    self.error("Main program block is not valid", self.token.line, self.token.column)
                                            else:
                                                self.error("Missing \")\"", self.token.line, self.token.column)
                                        else:
                                            self.error("Missing an \"identifier\"", self.token.line, self.token.column)
                                    else:
                                        self.error("Missing \"]\"", self.token.line, self.token.column)
                                else:
                                    self.error("Missing \"[\"", self.token.line, self.token.column)
                            else:
                                self.error("Missing \"String\"", self.token.line, self.token.column)
                        else:
                            self.error("Missing \"(\"", self.token.line, self.token.column)
                    else:
                        self.error("Missing \"main\"", self.token.line, self.token.column)
                else:
                    self.error("Missing \"void\"", self.token.line, self.token.column)
            else:
                self.error("Missing \"static\"", self.token.line, self.token.column)
        else:
            self.error("Missing \"public\"", self.token.line, self.token.column)
        return False

    def validateBlock(self):
        # <T#LEFT_BRACKET> (<stepVariableDeclaration> | <validateCommand>) <T#RIGHT_BRACKET>
        self.searchToken()
        if(self.token.type == "T#LEFT_BRACKET"):
            while(self.token.type != "T#RIGHT_BRACKET"):
                self.searchToken()
                if(not ( (self.stepVariableDeclaration()) or (self.validateCommand()) )):
                    self.error("Error at declaring variable or command", self.token.line, self.token.column)
                    return False
            if(self.token.type == "T#RIGHT_BRACKET"):
                return True
            else:
                self.error("Missing \"}\"", self.token.line, self.token.column)
                return False

    def stepVariableDeclaration(self):
        # <validateVariableDeclaration> <T#DOT_COMMA> 
        # { <validateVariableDeclaration> <T#DOT_COMMA> }
        pass

    def validateVariableDeclaration(self):
        # ( T#PRIVATE | T#PUBLIC | T#STATIC ) ( <T#TYPE_BOOLEAN> | <T#TYPE_INTEGER> ) <validateAttribution>
        self.searchToken()
        if((self.token.type == "T#PRIVATE") or (self.token.type == "T#PUBLIC") or (self.token.type == "T#STATIC")):
            self.searchToken()
            if((self.token.type == "T#TYPE_BOOLEAN") or (self.token.type == "T#TYPE_INTEGER")):
                self.searchToken()
                if(self.validateAttribution()):
                    return True
                else:
                    self.error("Error at variable attribution.", self.token.line, self.token.column)
            else:
                self.error("Missing variable type.", self.token.line, self.token.column)
        else:
            self.error("Missing variable behavior.", self.token.line, self.token.column)
        return False

    def validateCommand(self):
        # ( <validateAttribution> | <validatePrint> | <validateRead> | <validateFunctionCall> | <validateExpression> ) <T#DOT_COMMA>
        # { ( <validateAttribution> | <validatePrint> | <validateRead> | <validateFunctionCall> | <validateExpression> ) <T#DOT_COMMA>}
        pass

    def validateAttribution(self):
        # <T#IDENTIFIER> <T#EQUALS> <validateExpression>
        self.searchToken()
        if(self.token.type == "T#IDENTIFIER"):
            self.searchToken()
            if(self.token.type == "T#EQUALS"):
                self.searchToken()
                if(self.validateExpression()):
                    return True
                else:
                    self.error("Error at expression definition.", self.token.line, self.token.column)
            else:
                self.error("Missing \"=\"", self.token.line, self.token.column)
        else:
            self.error("Missing an \"identifier\"", self.token.line, self.token.column)
        return False

    def validatePrint(self):
        # <T#PRINT> <T#LEFT_PARENTHESIS> <validateExpression> <T#RIGHT_PARENTHESIS>
        self.searchToken()
        if(self.token.type == "T#PRINT"):
            self.searchToken()
            if(self.token.type == "T#LEFT_PARENTHESIS"):
                self.searchToken()
                if(self.validateExpression()):
                    self.searchToken()
                    if(self.token.type == "T#RIGHT_PARENTHESIS"):
                        return True
                    else:
                        self.error("Missing \")\"", self.token.line, self.token.column)
                else:
                    self.error("Error at expression definition.", self.token.line, self.token.column)
            else:
                self.error("Missing \"(\"", self.token.line, self.token.column)
        else:
            self.error("Missing \"System.out.Println\"", self.token.line, self.token.column)
        return False

    def validateRead(self):
        # <T#READ> <T#LEFT_PARENTHESIS> <validateExpression> <T#RIGHT_PARENTHESIS>
        self.searchToken()
        if(self.token.type == "T#READ"):
            self.searchToken()
            if(self.token.type == "T#LEFT_PARENTHESIS"):
                self.searchToken()
                if(self.validateExpression()):
                    self.searchToken()
                    if(self.token.type == "T#RIGHT_PARENTHESIS"):
                        return True
                    else:
                        self.error("Missing \")\"", self.token.line, self.token.column)
                else:
                    self.error("Error at expression definition.", self.token.line, self.token.column)
            else:
                self.error("Missing \"(\"", self.token.line, self.token.column)
        else:
            self.error("Missing \"System.in.Read\"", self.token.line, self.token.column)

    def validateFunctionCall(self):
        # <T#IDENTIFIER> <T#LEFT_PARENTHESIS> <validateExpression> <T#RIGHT_PARENTHESIS>
        self.searchToken()
        if(self.token.type == "T#IDENTIFIER"):
            self.searchToken()
            if(self.token.type == "T#LEFT_PARENTHESIS"):
                self.searchToken()
                if(self.validateExpression()):
                    self.searchToken()
                    if(self.token.type == "T#RIGHT_PARENTHESIS"):
                        return True
                    else:
                        self.error("Missing \")\"", self.token.line, self.token.column)
                else:
                    self.error("Error at expression definition.", self.token.line, self.token.column)
            else:
                self.error("Missing \"(\"", self.token.line, self.token.column)
        else:
            self.error("Missing an \"identifier\"", self.token.line, self.token.column)
        return False

    def validateExpression(self):
        # <expression> ::= <simple_expression> [ <relational_op> <simple_expression> ]
        # <relational_op> ::= (T#NOTEQUALS | T#EQUALS | T#LESSERTHAN | T#LESSEREQUALS | T#GREATERTHAN | T#GREATEREQUALS)
	    # <simple_expression> ::= <term> { (T#SUM | T#SUBTRACTION | T#OR) <term> }
	    # <term> ::= <m,> { (T#MULTIPLICATION | T#DIVISION | T#AND) <factor> }
	    # <factor> ::= (T#IDENTIFIER | <validateFunctionCall> | T#NOT <factor> | <parenthesis_exp> | (T#POSITIVE_INTEGER | T#NEGATIVE_INTEGER) | (T#TRUE | T#FALSE))
        # <parenthesis_exp> ::= T#LEFT_PARENTHESIS <expression> T#RIGHT_PARENTHESIS
        pass


if(__name__ == "__main__"):
    def printSymbolTable(p_parser):
        print()
        print("Symbol Table:")
        print("TOKENTYPE, TOKENLEXEM, TOKENSCOPE")
        for data in p_parser.symboltable:
            print(data.type +", "+ data.lexem + ", " + data.scope)

    try:
        table = []
        lexer = LexicalAnalyzer(sys.argv[1])
        parser = PRP(table, lexer)
        if(parser.parse()):
            print(sys.argv[1] + " is a valid program.")
            printSymbolTable(parser)
        else:
            print(sys.argv[1] + " is not a valid program.")
    except IndexError:
        print("Missing target source file.")
        print("Usage:")
        print(" -> python parser.py <SOURCE_TO_READ>")
        print(" -> py parser.py <SOURCE_TO_READ>")