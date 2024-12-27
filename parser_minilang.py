import ply.yacc as yacc
from lexer_minilang import tokens

class ASTNode:
    def __init__(self, nodetype, children=None, value=None):
        self.nodetype = nodetype
        self.children = children if children else []
        self.value = value

    def __repr__(self):
        return f"ASTNode({self.nodetype}, {self.value}, {self.children})"

# Regla principal del programa
def p_program(p):
    '''program : consts vars subroutines main'''
    print("Procesando programa...")
    p[0] = ASTNode('program', [p[1], p[2], p[3], p[4]])

# Reglas para tipos
def p_type(p):
    '''type : INT
            | STRING
            | BOOL'''
    p[0] = p[1]

# Declaraciones de constantes
def p_consts(p):
    '''consts : consts const_decl
              | empty'''
    if len(p) == 3:  # Caso recursivo
        p[0] = p[1] + [p[2]]
    else:  # Caso base
        p[0] = []

def p_const_decl(p):
    '''const_decl : CONST type ID ASSIGN expr SEMICOLON'''
    print(f"Declaración de constante: {p[3]} de tipo {p[2]} con valor {p[5]}")
    p[0] = ASTNode('const_decl', [ASTNode('type', value=p[2]), ASTNode('id', value=p[3])], p[5])

# Declaraciones de variables
def p_vars(p):
    '''vars : vars var_decl
            | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_var_decl(p):
    '''var_decl : type ID ASSIGN expr SEMICOLON'''
    print(f"Declarando variable: {p[2]} de tipo {p[1]} con valor {p[4]}")
    p[0] = ASTNode('var_decl', [ASTNode('type', value=p[1]), ASTNode('id', value=p[2])], p[4])

# Declaraciones de subrutinas
def p_subroutines(p):
    '''subroutines : subroutines subroutine_decl
                   | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_subroutine_decl(p):
    '''subroutine_decl : SUBROUTINE type ID LPAREN param_list RPAREN DO stmt_list END'''
    print(f"Declarando subrutina: {p[3]} con tipo de retorno {p[2]} y parámetros {p[5]}")
    p[0] = ASTNode('subroutine_decl', [ASTNode('type', value=p[2]), ASTNode('id', value=p[3]), p[5], p[8]])

# Lista de parámetros para subrutinas
def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param
                  | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_param(p):
    '''param : type ID'''
    p[0] = ASTNode('param', [ASTNode('type', value=p[1]), ASTNode('id', value=p[2])])

# Bloque principal del programa
def p_main(p):
    '''main : SUBROUTINE VOID MAIN LPAREN RPAREN DO stmt_list END'''
    print("Procesando función main...")
    p[0] = ASTNode('main', p[7])

# Lista de sentencias
def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Sentencias individuales
def p_stmt(p):
    '''stmt : var_decl
            | const_decl
            | subroutine_decl
            | PRINT LPAREN expr RPAREN SEMICOLON'''
    if len(p) == 6:
        print(f"Procesando sentencia print: {p[3]}")
        p[0] = ASTNode('print', [p[3]])
    else:
        p[0] = p[1]

# Expresiones
def p_expr(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | STRING_LITERAL
            | NUMBER
            | ID'''
    if len(p) == 4:  # Operación binaria
        print(f"Operación binaria: {p[2]} entre {p[1]} y {p[3]}")
        p[0] = ASTNode('binary_op', [p[1], p[3]], p[2])
    else:  # Literal o identificador
        p[0] = ASTNode('literal', value=p[1])

# Regla para vacío
def p_empty(p):
    '''empty :'''
    p[0] = []

# Manejo de errores
def p_error(p):
    if p:
        print(f"Error de sintaxis cerca de '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis al final del archivo.")

# Construcción del parser
parser = yacc.yacc()
