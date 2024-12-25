import ply.yacc as yacc
from lexer_minilang import tokens

class ASTNode:
    def __init__(self, nodetype, children=None, value=None):
        self.nodetype = nodetype
        self.children = children if children else []
        self.value = value

    def __repr__(self):
        return f"ASTNode({self.nodetype}, {self.value}, {self.children})"

def p_program(p):
    '''program : consts vars subroutines main'''
    print("Procesando programa...")
    print(f"Tokens procesados en program: consts={p[1]}, vars={p[2]}, subroutines={p[3]}, main={p[4]}")
    p[0] = ASTNode('program', [p[1], p[2], p[3], p[4]])

def p_consts(p):
    '''consts : consts CONST const_list
              | CONST const_list'''
    if len(p) == 4:  # Caso recursivo: múltiples bloques CONST
        print(f"Procesando bloque adicional CONST con lista: {p[3]}")
        p[1].children.extend(p[3])  # Agregar las nuevas declaraciones al nodo existente
        p[0] = p[1]
    else:  # Caso base: primer bloque CONST
        print(f"Procesando bloque inicial CONST con lista: {p[2]}")
        p[0] = ASTNode('consts', p[2])  # Crear un nodo con las declaraciones




def p_const_list(p):
    '''const_list : const_list const_decl
                  | const_decl'''
    if len(p) == 3:
        print(f"Agregando constante a la lista: {p[2]}")
        p[0] = p[1] + [p[2]]
    else:
        print(f"Iniciando nueva lista de constantes con: {p[1]}")
        p[0] = [p[1]]

def p_const_decl(p):
    '''const_decl : INT ID ASSIGN NUMBER SEMICOLON
                  | STRING ID ASSIGN STRING_LITERAL SEMICOLON'''
    print(f"Declaración de constante: {p[1]} {p[2]} = {p[4]}")
    p[0] = ASTNode(
        'const_decl',
        [ASTNode('type', value=p[1]), ASTNode('id', value=p[2])],
        p[4]
    )

def p_vars(p):
    '''vars : empty'''
    print("Procesando bloque de variables (vacío).")
    p[0] = ASTNode('vars', [])  # Devuelve un nodo ASTNode vacío


def p_subroutines(p):
    '''subroutines : empty'''
    print("Procesando subrutinas (vacío).")
    p[0] = []

def p_main(p):
    '''main : SUBROUTINE VOID MAIN LPAREN RPAREN DO stmt_list END'''
    print("Procesando función main...")
    p[0] = ASTNode('main', p[7])

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_stmt(p):
    '''stmt : PRINT LPAREN expr RPAREN SEMICOLON'''
    print(f"Procesando sentencia print: {p[3]}")
    p[0] = ASTNode('print', [p[3]])

def p_expr(p):
    '''expr : STRING_LITERAL
            | ID'''
    p[0] = ASTNode('literal', value=p[1])

def p_empty(p):
    '''empty :'''
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis cerca de '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis al final del archivo.")

parser = yacc.yacc()


