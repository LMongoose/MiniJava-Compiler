class Symbol():
    def __init__(self, p_name, p_type, p_datatype, p_scope):
        self.name = p_name
        self.type = p_type
        self.datatype = p_datatype
        self.scope = p_scope

# deprecated
class SymbolTable(dict):
    def allocate(self, p_key):
        if(not(p_key in self.keys())):
            self.insert(p_key, {})

    def free(self):
        return self.clear()

    def lookup(self, p_key):
        if(p_key in self.keys()):
            return self[p_key]
        else:
            return None

    def insert(self, p_key, p_value):
        if(not(p_key in self.keys())):
            self[p_key] = p_value

    def set_attribute(self, p_key):
        self[p_key] = None

    def get_attribute(self, p_key):
        return self.get(p_key)
