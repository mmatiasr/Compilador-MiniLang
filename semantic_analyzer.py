from symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTable()

    def analyze(self):
        if isinstance(self.ast, list):
            for node in self.ast:
                self.visit(node)
        else:
            self.visit(self.ast)

    def visit(self, node):
        if isinstance(node, list):  # Si el nodo es una lista, procesar cada elemento
            for child in node:
                self.visit(child)
            return

        print(f"Visitando nodo: {node.nodetype}")
        if node.nodetype == 'program':
            for child in node.children:
                self.visit(child)
        elif node.nodetype == 'consts':
            self.visit_consts(node)
        elif node.nodetype == 'vars':
            self.visit_vars(node)
        elif node.nodetype == 'main':
            self.visit_main(node)
        elif node.nodetype == 'print':
            self.visit_print(node)
        elif node.nodetype == 'assignment':
            self.visit_assignment(node)
        elif node.nodetype == 'binary_op':
            self.visit_binary_op(node)
        else:
            raise Exception(f"Nodo desconocido: {node.nodetype}")

    def visit_consts(self, node):
        print(f"Procesando nodo consts con {len(node.children)} declaraciones.")
        for const in node.children:
            if const.nodetype != 'const_decl':
                raise Exception(f"Nodo inesperado dentro de consts: {const}")
            const_type = const.children[0].value  # Tipo
            const_name = const.children[1].value  # Nombre
            const_value = const.value  # Valor
            print(f"Registrando constante: {const_name} de tipo {const_type} con valor {const_value}")
            self.symbol_table.add_symbol(const_name, const_type, is_constant=True)

    def visit_vars(self, node):
        for var in node.children:
            var_type = var.children[0].value  # Tipo
            var_name = var.children[1].value  # Nombre
            print(f"Registrando variable: {var_name} de tipo {var_type}")
            self.symbol_table.add_symbol(var_name, var_type)

    def visit_main(self, node):
        print("Analizando función main...")
        #if len(node.children) > 0:
         #   raise Exception("El bloque principal no puede contener código.")
        for stmt in node.children:
            self.visit(stmt)


    def visit_print(self, node):
        expr = node.children[0]
        if expr.nodetype == 'literal':
            print(f"Validando print de literal: {expr.value}")
        elif expr.nodetype == 'id':
            var_name = expr.value
            self.symbol_table.lookup(var_name)  # Verificar si la variable está declarada
            print(f"Validando print de variable: {var_name}")
        else:
            raise Exception("Tipo de expresión no válida en print.")

    def visit_assignment(self, node):
        var_name = node.children[0].value
        if var_name in self.symbol_table.functions:
            raise Exception(f"No se puede asignar un valor a la función '{var_name}'.")
        if self.symbol_table.is_constant(var_name):
            raise Exception(f"No se puede reasignar la constante '{var_name}'.")
        var_type = self.symbol_table.lookup(var_name)
        value_type = self.visit(node.children[1])
        if var_type != value_type:
            raise Exception(f"Tipo incompatible en la asignación: se esperaba '{var_type}', pero se encontró '{value_type}'.")

    def visit_binary_op(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        if node.value == '+':
            if left_type == 'string' and right_type == 'string':
                return 'string'  # Concatenación de strings
            elif left_type == 'string' and right_type == 'int':
                return 'string'  # Conversión implícita y concatenación
            elif left_type == 'int' and right_type == 'string':
                return 'string'  # Conversión implícita y concatenación
            elif left_type != right_type:
                raise Exception(f"Operación no válida entre {left_type} y {right_type}.")
        elif node.value in ['-', '*', '/']:
            if left_type != 'int' or right_type != 'int':
                raise Exception(f"Operación no válida: {node.value} solo es válida entre enteros.")
        return left_type
    
    def visit_return(self, node):
        subroutine_name = node.parent.value  # Asume que el nodo tiene un padre que representa la subrutina
        declared_return_type = self.symbol_table.functions[subroutine_name]['return_type']
        if declared_return_type == 'void':
            if len(node.children) > 0:
                raise Exception(f"La subrutina '{subroutine_name}' no debe devolver un valor, ya que su tipo es 'void'.")
        else:
            if len(node.children) == 0:
                raise Exception(f"La subrutina '{subroutine_name}' debe devolver un valor de tipo '{declared_return_type}'.")
            return_type = self.visit(node.children[0])
            if return_type != declared_return_type:
                raise Exception(f"La subrutina '{subroutine_name}' debe devolver un valor de tipo '{declared_return_type}', pero devuelve '{return_type}'.")

    def visit_subroutine_call(self, node):
        subroutine_name = node.value
        declared_params = self.symbol_table.lookup_function(subroutine_name)['params']
        if len(declared_params) != len(node.children):
            raise Exception(f"La subrutina '{subroutine_name}' esperaba {len(declared_params)} parámetros, pero se pasaron {len(node.children)}.")
        for i, param in enumerate(node.children):
            param_type = self.visit(param)
            if param_type != declared_params[i]:
                raise Exception(f"El parámetro {i+1} debe ser de tipo {declared_params[i]}, pero se encontró {param_type}.")


