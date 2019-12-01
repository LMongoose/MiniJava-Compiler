_dict = {
  "variable1": "",
  "function1": {
      "variable1": "",
      "variable2": ""
  },
  "variable2": "",
  "function2": {
      "variable1": ""
  }
}

class SymbolTable():
    def __init__(self):
        self.table = {}

    def allocate(self, p_key):
        if(not(p_key in self.table.keys())):
            self.table[p_key] = {}

    def free(self):
        self.table = {}

    def lookup(self, p_key):
        if(p_key in self.table.keys()):
            return self.table[p_key]
        else:
            return 0

    def insert(self, p_key, p_value):
        if(not(p_key in self.table.keys())):
            self.table[p_key] = p_value

    def set_attribute(self, p_key):
        pass

    def get_attribute(self, p_key):
        pass


maintable = SymbolTable()
maintable.insert("var1", 8)

subtable1 = SymbolTable()
subtable1.insert("var1", 4)
subtable1.insert("var2", 1)
maintable.insert("function1", subtable1)

maintable.insert("var2", 3)

subtable2 = SymbolTable()
subtable2.insert("var1", 7)
maintable.insert("function2", subtable2)

for data in maintable.table:
    if(isinstance(maintable.table[data], SymbolTable)):
        for subdata in maintable.table[data].table:
            print(data + ": " + subdata)
    else:
        print("global: " + data)