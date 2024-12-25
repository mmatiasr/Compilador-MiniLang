class SymbolTable:
    def __init__(self):
        self.symbols = {}  # Diccionario para almacenar variables y constantes
        self.constants = set()  # Conjunto de constantes (inmutables)

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
