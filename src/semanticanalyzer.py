# Native Modules
import os, sys
# Downloaded Modules

# Custom Modules
from errorhandler import SemanticError
import main


class SemanticAnalyzer():
    def __init__(self):
        pass

    def addTokenToTable(self, p_token):
        # TODO: check if have another declared with same name and scope
        if(not(p_token) in main.symboltable):
            main.symboltable.append(p_token)
        else:
            raise SemanticError("Token is already on symboltable", p_token.line, p_token.column)

    def validateIdentifier(self):
        # TODO: check if identifier exists
        pass

    def validateTypeCompatibility(self, p_expressionlist):
        for token in p_expressionlist[1:]:
            if(token.type != p_expressionlist[0].type):
                raise SemanticError("The elements of the expression are not of the same type", p_expressionlist[0].line, p_expressionlist[0].column)

    def analyze(self):
        # TODO: check commands, procedure/function callings, operations, comparations, etc.
        pass

if(__name__ == "__main__"):
    pass