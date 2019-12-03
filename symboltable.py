# deprecated
class Symbol():
    def __init__(self, p_name, p_type, p_datatype, p_scope):
        self.name = p_name
        self.type = p_type
        self.datatype = p_datatype
        self.scope = p_scope


class SymbolTable(dict):
    def __init__(self):
        super().__init__()

    def allocate(self, p_key):
        if(not(self.lookup(p_key))):
            self.insert(p_key, {})

    def free(self):
        return self.clear()

    def lookup(self, p_key):
        if(p_key in self.keys()):
            return True
        else:
            return False

    def insert(self, p_key, p_value):
        if(not(self.lookup(p_key))):
            self[p_key] = p_value

    def set_attribute(self, p_key, p_value):
        self[p_key] = p_value

    def get_attribute(self, p_key):
        return self.get(p_key)
