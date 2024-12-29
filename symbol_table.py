class SymbolTable:
    def __init__(self):
        self.symbols = {}  # Diccionario para almacenar variables y constantes
        self.constants = set()  # Conjunto de constantes (inmutables)
        self.functions = {}  # Diccionario para almacenar subrutinas

    def add_symbol(self, name, symbol_type, is_constant=False):
        if name in self.symbols:
            raise Exception(f"El símbolo '{name}' ya está declarado en el mismo ámbito.")
        self.symbols[name] = symbol_type
        if is_constant:
            self.constants.add(name)

    def lookup(self, name):
        if name not in self.symbols:
            raise Exception(f"La variable o constante '{name}' no está declarada.")
        return self.symbols[name]

    def is_constant(self, name):
        return name in self.constants

    def add_function(self, name, return_type, params):
        if name in self.functions:
            raise Exception(f"La subrutina '{name}' ya está declarada.")
        self.functions[name] = {
            'return_type': return_type,
            'params': [{'type': param.children[0].value, 'name': param.children[1].value} for param in params]
        }

    def get_function(self, name):
        if name not in self.functions:
            raise Exception(f"La subrutina '{name}' no está declarada.")
        return self.functions[name]