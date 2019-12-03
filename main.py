################################
#  MINIJAVA COMPILER IN PYTHON
################################


# Native Modules
import os, sys
# Downloaded Modules

# Custom Modules
from lexicalanalyzer import LexicalAnalyzer
from parser import PrimitiveRecursiveParser
from semanticanalyzer import SemanticAnalyzer
from codegenerator import CodeGenerator


if(__name__ == "__main__"):
    symboltable = []
    if(len(sys.argv) == 2):
        if(os.path.isfile(sys.argv[1])):
            lexer = LexicalAnalyzer()
            tokenlist = lexer.tokenize()

            parser = PrimitiveRecursiveParser(tokenlist)
            symboltable = parser.parse()

            validator = SemanticAnalyzer()
            #validator.analyze()

            codegen = CodeGenerator()
            codegen.generate(tokenlist, "target.py")
            codegen.run()
        else:
            print("O arquivo \"{0}\" não é um arquivo válido ou não existe.".format(sys.argv[1]))
    else:
        print("Argumentos inválidos!")
        print("Modo de uso: python lexicalanalyzer.py <nome_do_arquivo_a_ser_analisado>")