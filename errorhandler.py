class MiniJavaError(BaseException):
    """General compilation error."""
    def __init__(self, p_message, p_line, p_column):
        if(not p_message):
            p_message = "MiniJavaError"
        super().__init__(p_message + " at line " + str(p_line) + " and column " + str(p_column))

class LexicalError(MiniJavaError):
    """Error in lexical analysis."""
    def __init__(self, p_message, p_line, p_column):
        super().__init__(p_message, p_line, p_column)

class SyntaxParsingError(MiniJavaError):
    """Error in the syntax parser."""
    def __init__(self, p_message, p_line, p_column):
        super().__init__(p_message, p_line, p_column)

class SemanticError(MiniJavaError):
    """Error in the semantic validations."""
    def __init__(self, p_message, p_line, p_column):
        super().__init__(p_message, p_line, p_column)

class ExecutionError(MiniJavaError):
    """Error in target code execution."""
    def __init__(self, p_message, p_line, p_column):
        super().__init__(p_message, p_line, p_column)