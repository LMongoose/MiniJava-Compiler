# Native Modules
import os, sys, subprocess
# Downloaded Modules

# Custom Modules
from errorhandler import ExecutionError
import main


class CodeGenerator():
    def __init__(self):
        self.targetfilename = ""
        self.line = 1
        self.column = 1

    def generate(self, p_tokenlist, p_targetfilename):
        # class <classname> -> class <classname>:
        # { -> increase tab counter
        # public static void main(String[] <identifier>) -> @staticmethod \n def main():
        # { -> increase tab counter
        # int x = 1000; -> x = 1000
        # bool y = true; -> y = True
        # System.out.println(expression); -> print(expression)
        # } -> decrease tab counter 
        # } -> decrease tab counter 
        # if(__name__ == "__main__"):
        # \t<classname>.main()
        self.targetfilename = p_targetfilename

        try:
            with open(self.targetfilename) as outputfile:
                _currpos, _tabcount = 0, 0
                if(p_tokenlist[_currpos].type == "T#CLASS"):
                    outputfile.write("{0} {1} {2}\n".format("class", p_tokenlist[_currpos+1].lexem, ":"))
                    _currpos += 2
                elif(p_tokenlist[_currpos].type == "T#LEFT_BRACKET"):
                    _tabcount += 1
                    _currpos += 1
                elif(p_tokenlist[_currpos].type == "T#RIGHT_BRACKET"):
                    _tabcount -= 1
                    _currpos += 1
                elif(p_tokenlist[_currpos].type == "T#PUBLIC"):
                    self.line = p_tokenlist[_currpos].line
                    self.column = p_tokenlist[_currpos].column
                    if(p_tokenlist[_currpos+1].type == "T#STATIC"):
                        if(p_tokenlist[_currpos+2].type == "T#VOID"):
                            if(p_tokenlist[_currpos+3].type == "T#MAIN"):
                                outputfile.write("\t"*_tabcount+"@staticmethod\n")
                                outputfile.write("\t"*_tabcount+"def main():\n")
                                _currpos += 4
                elif(p_tokenlist[_currpos].type == "T#SYSTEM"):
                    self.line = p_tokenlist[_currpos].line
                    self.column = p_tokenlist[_currpos].column
                    if(p_tokenlist[_currpos].type == "T#DOT"):
                        if(p_tokenlist[_currpos].type == "T#OUT"):
                            if(p_tokenlist[_currpos].type == "T#DOT"):
                                if(p_tokenlist[_currpos].type == "T#PRINT"):
                                    outputfile.write("\t"*_tabcount+"print("+p_tokenlist[_currpos+6].value+")\n")
                elif((p_tokenlist[_currpos].type == "T#TYPE_BOOLEAN") or (p_tokenlist[_currpos].type == "T#TYPE_INTEGER")):
                    self.line = p_tokenlist[_currpos].line
                    self.column = p_tokenlist[_currpos].column
                    outputfile.write("\t"*_tabcount+p_tokenlist[_currpos+1].lexem + "="+ p_tokenlist[_currpos+2].lexem+"\n")
                outputfile.write("if(__name__ == \"__main__\"):\n")
                outputfile.write("\t"+p_tokenlist[1].lexem +".main()")
        except:
            raise ExecutionError("Failed to generate target '{0}'".format(self.targetfilename), self.line, self.column)

    def run(self):
        # call py <generated_code>
        try:
            if(self.targetfilename):
                os.system("py " + self.targetfilename)
            else:
                raise ExecutionError("Failed to execute '{0}'".format(self.targetfilename), self.line, self.column)
        except:
            raise ExecutionError("Failed to execute '{0}'".format(self.targetfilename), self.line, self.column)


if(__name__ == "__main__"):
    pass