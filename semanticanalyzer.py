# Native Modules
import os, sys
# Downloaded Modules

# Custom Modules


# Identificar escopo do programa principal (usar identificador do programa principal)
# Verificar ocorrência de duplicidade na declaração de um identificador (não pode ter variáveis repetidas no mesmo escopo)
# Verificação do uso de identificadores não declarados na atribuição
# Na atribuição e na soma, verificar compatibilidade de tipos

# para cada token,
#   se token é identificador:
#       checar se identificador foi declarado antes
#       checar se na tabela há outro token com o mesmo nome e mesmo escopo
#       se sim: erro de identificador existente


class SemanticAnalyzer(object):
    def __init__(self, p_symboltable):
        self.symboltable = p_symboltable

    def validateIdentifiers(self):
        # check if identifier exists, if have another declared with same name
        pass

    def validateTypeCompatibility(self):
        # check if all elements of the expression are of the same type
        pass

    def analyze(self):
        # 
        self.validateIdentifiers()
        self.validateTypeCompatibility()


if(__name__ == "__main__"):
    pass