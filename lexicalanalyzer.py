# Native Modules
import os, sys
# Downloaded Modules

# Custom Modules
from lexicaltoken import Token
from errorhandler import LexicalError

# Constants
LOWERCASELETTERS = "abcdefghijklmnopqrstuvwxyz"
UPPERCASECASELETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"

KEYWORDS = {
    "main":    "T#MAIN",
    "private": "T#PRIVATE",
    "public":  "T#PUBLIC",
    "static":  "T#STATIC",
    "new":     "T#NEW",
    "boolean": "T#TYPE_BOOLEAN",
    "int":     "T#TYPE_INTEGER",
    "float":   "T#TYPE_FLOAT",
    "String":  "T#STRING",
    "true":    "T#TRUE",
    "false":   "T#FALSE",
    "if":      "T#IF",
    "else":    "T#ELSE",
    "while":   "T#WHILE",
    "for":     "T#FOR",
    "return":  "T#RETURN",
    "void":    "T#VOID",
    "null":    "T#NULL",
    "this":    "T#THIS",
    "class":   "T#CLASS",
    "System":  "T#SYSTEM",
    "out":     "T#OUT",
    "in":      "T#IN",
    "println": "T#PRINT",
    "read":    "T#READ"
}

PUNCTUATION = {
    ".": "T#DOT",
    ",": "T#COMMA",
    ";": "T#DOT_COMMA",
    "(": "T#LEFT_PARENTHESIS",
    ")": "T#RIGHT_PARENTHESIS",
    "[": "T#LEFT_SQUARE_BRACKET",
    "]": "T#RIGHT_SQUARE_BRACKET",
    "{": "T#LEFT_BRACKET",
    "}": "T#RIGHT_BRACKET"
}

ARITHMETIC_OPERATORS = {
    "+": "T#SUM",
    # [INCODE]: "T#SUBTRACTION",
    "*": "T#MULTIPLICATION"
    # [INCODE]: "T#DIVISION"
}

# RELATIONAL OPERATORS
# [INCODE]: "T#GREATERTHAN"
# [INCODE]: "T#LESSERTHAN"
# [INCODE]: "T#EQUALS"
# [INCODE]: "T#NOTEQUALS"
# [INCODE]: "T#GREATEREQUALS"
# [INCODE]: "T#LESSEREQUALS"
# [INCODE]: "T#AND"
# [INCODE]: "T#OR"
# [INCODE]: "T#NOT"

# GENERAL
# [INCODE]: "T#SPACE"
# [INCODE]: "T#TAB"
# [INCODE]: "T#NEWLINE"
# [INCODE]: "T#POSITIVE_INTEGER"
# [INCODE]: "T#POSITIVE_FLOAT"
# [INCODE]: "T#NEGATIVE_INTEGER"
# [INCODE]: "T#NEGATIVE_FLOAT"
# [INCODE]: "T#IDENTIFIER"
# [INCODE]: "T#ERROR"

class LexicalAnalyzer(object):
    def __init__(self):
        self.line = 1
        self.column = 1
        self.tokens = []

    def tokenize(self, p_filename):
        f = open(p_filename)
        while True:
            char = f.read(1)
            if(char):
                # recognizes and handles spaces
                if(char == " "):
                    self.column += 1

                # recognizes and handles tabs
                elif(char == "\t"):
                    self.column += 1

                # recognizes and handles newlines
                elif(char in "\n"):
                    self.line += 1
                    self.column = 1

                # recognizes and handles singleline comments and division "/"
                elif(char == "/"):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar == "/"):
                        self.column += 2
                        while char not in "\n":
                            char = f.read(1)
                            self.column += 1
                        if(char == "\n"):
                            self.column = 1
                            self.line += 1
                    else:
                        _type = "T#DIVISION"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1
                        f.seek(last_column)

                # recognizes and handles positive numbers (integers and decimals)
                elif(char in DIGITS):
                    number = char
                    last_column = f.tell()
                    char = f.read(1)
                    while char in DIGITS + ".":
                        number += char
                        last_column = f.tell()
                        char = f.read(1)
                    if(number.count(".") > 1):
                        raise SyntaxError("O número '{0}' é inválido.".format(number))
                    f.seek(last_column)
                    if("." in number):
                        _type = "T#POSITIVE_FLOAT"
                    else:
                        _type = "T#POSITIVE_INTEGER"
                    self.tokens.append(Token(_type, number, self.line, self.column))
                    self.column += len(number)

                # recognizes and handles negative numbers and subtractions
                elif(char == "-"):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar in DIGITS + "."):
                        # char is a '-' and next char is digit
                        number = char
                        while nextchar != " ":
                            number += nextchar
                            last_column = f.tell()
                            nextchar = f.read(1)
                        if(number.count(".") > 1):
                            raise SyntaxError("O número '{0}' é inválido.".format(number))
                        f.seek(last_column)
                        if("." in number):
                            _type = "T#NEGATIVE_FLOAT"
                        else:
                            _type = "T#NEGATIVE_INTEGER"
                        self.tokens.append(Token(_type, number, self.line, self.column))
                        self.column += len(number)
                    else:
                        # char is a '-' and next char is space
                        _type = "T#SUBTRACTION"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1

                # recognizes and handles keywords/identifiers
                elif(char in LOWERCASELETTERS + UPPERCASECASELETTERS + DIGITS + "_"):
                    word = char
                    last_column = f.tell()
                    char = f.read(1)
                    while char in LOWERCASELETTERS + UPPERCASECASELETTERS + DIGITS + "_":
                        word += char
                        last_column = f.tell()
                        char = f.read(1)
                    f.seek(last_column)
                    if(word in KEYWORDS.keys()):
                        _type = KEYWORDS[word]
                    else:
                        _type = "T#IDENTIFIER"
                    self.tokens.append(Token(_type, word, self.line, self.column))
                    self.column += len(word)

                # recognizes and handles "=" and "=="
                elif(char == "="):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar == "="):
                        _type = "T#EQUALS"
                        char += nextchar
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 2
                    else:
                        _type = "T#ATTRIBUTION"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1
                        f.seek(last_column)

                # recognizes and handles "!" and "!="
                elif(char == "!"):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar == "="):
                        _type = "T#NOT_EQUALS"
                        char += nextchar
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 2
                    else:
                        _type = "T#NOT"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1
                        f.seek(last_column)

                # recognizes and handles ">" and ">="
                elif(char == ">"):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar == "="):
                        _type = "T#GREATER_EQUALS"
                        char += nextchar
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 2
                    else:
                        _type = "T#GREATER_THAN"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1
                        f.seek(last_column)

                # recognizes and handles "<" and "<="
                elif(char == "<"):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar == "="):
                        _type = "T#LESSER_EQUALS"
                        char += nextchar
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 2
                    else:
                        _type = "T#LESSER_THAN"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1
                        f.seek(last_column)

                # recognizes and handles "&&"
                elif(char == "&"):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar == "&"):
                        _type = "T#AND"
                        char += nextchar
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 2
                    else:
                        _type = "T#ERROR"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1
                        f.seek(last_column)

                # recognizes and handles "||"
                elif(char == "|"):
                    last_column = f.tell()
                    nextchar = f.read(1)
                    if(nextchar == "|"):
                        _type = "T#OR"
                        char += nextchar
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 2
                    else:
                        _type = "T#ERROR"
                        self.tokens.append(Token(_type, char, self.line, self.column))
                        self.column += 1
                        f.seek(last_column)

                # recognizes and handles punctuation
                elif(char in PUNCTUATION.keys()):
                    _type = PUNCTUATION[char]
                    self.tokens.append(Token(_type, char, self.line, self.column))
                    self.column += 1

                # recognizes and handles arithmetic operators
                elif(char in ARITHMETIC_OPERATORS.keys()):
                    _type = ARITHMETIC_OPERATORS[char]
                    self.tokens.append(Token(_type, char, self.line, self.column))
                    self.column += 1

                else:
                    #_type = "T#ERROR"
                    #self.tokens.append(Token(_type, char, self.line, self.column))
                    #self.column += 1
                    raise LexicalError("Lexical Error", self.line, self.column)

            else:
                # END OF FILE
                f.close()
                break
        return self.tokens


if(__name__ == "__main__"):
    if(len(sys.argv) == 2):
        if(os.path.isfile(sys.argv[1])):
            lex = LexicalAnalyzer() 

            print("Número de tokens: " + str(len(lex.tokens)))
            
            for token in lex.tokenize(sys.argv[1]):
                if(token.type != "T#ERROR"):
                    print("Encontrado o token \"{0}\" com lexema \"{1}\" na linha {2} coluna {3}".format(token.type, token.lexem, token.line, token.column))
                else:
                    print("Encontrado o token inválido \"{0}\" na linha {1} coluna {2}".format(token.lexem, token.line, token.column), end="<ERROR>\n")
        else:
            print("O arquivo \"{0}\" não é um arquivo válido ou não existe.".format(sys.argv[1]))
    else:
        print("Argumentos inválidos!")
        print("Modo de uso: python lexicalanalyzer.py <nome_do_arquivo_a_ser_analisado>")