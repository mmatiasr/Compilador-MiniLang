import ply.lex as lex

# Palabras reservadas
reserved = {
    'CONST': 'CONST',
    'SUBROUTINE': 'SUBROUTINE',
    'DO': 'DO',
    'END': 'END',
    'int': 'INT',
    'bool': 'BOOL',
    'string': 'STRING',
    'void': 'VOID',
    'print': 'PRINT',
    'main': 'MAIN',
}

# Tokens
tokens = [
    'ID',
    'NUMBER',
    'STRING_LITERAL',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'

# Tokens complejos
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"([^\\\n]|(\\.))*?"'
    t.value = t.value[1:-1]  # Elimina comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es una palabra reservada
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()


