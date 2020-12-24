class Token():
    def __init__(self, p_type, p_lexem, p_line, p_column):
        self.type = p_type
        self.lexem = p_lexem
        self.line = p_line
        self.column = p_column
        self.address = "" ## position in symboltable
        self.datatype = "" ## boolean/integer
        self.scope = "" ## global/function/procedure
        self.value = ""