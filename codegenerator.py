# Native Modules
import os, sys
# Downloaded Modules

# Custom Modules


## generate python code with source code
class CodeGenerator(object):
    def __init__(self):
        pass

    def generate(self):
        # class <classname> -> class <classname>:
        # { -> increase tab counter
        # public static void main(String[] <identifier>) -> @staticmethod \n def main():
        # { -> increase tab counter
        # <main block> (variables and commands) -> python variables and commands
        # } -> decrease tab counter 
        # } -> decrease tab counter 
        # if(__name__ == "__main__"): \n <classname>.main()
        pass

    def run(self):
        # call py <generated_code>
        pass


if(__name__ == "__main__"):
    pass