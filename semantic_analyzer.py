from symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTable()

    def analizar(self):
        if isinstance(self.ast, list):
            for node in self.ast:
                self.visitar(node)
        else:
            self.visitar(self.ast)

    def visitar(self, node):
        if isinstance(node, list):  # Si el nodo es una lista, procesar cada elemento
            for hijo in node:
                self.visitar(hijo)
            return

        print(f"Visitando nodo: {node.nodetype}")
        if node.nodetype == 'program':
            for hijo in node.children:
                self.visitar(hijo)
        elif node.nodetype == 'consts':
            self.visitar_consts(node)
        elif node.nodetype == 'const_decl':
            self.visitar_consts_decl(node)
        elif node.nodetype == 'vars':
            self.visitar_vars(node)
        elif node.nodetype == 'var_decl':
            self.visitar_var_decl(node)
        elif node.nodetype == 'subroutine_decl':
            self.visitar_subroutine_decl(node)
        elif node.nodetype == 'main':
            self.visitar_main(node)
        elif node.nodetype == 'print':
            self.visitar_print(node)
        elif node.nodetype == 'call':
            self.visitar_llamada(node)
        elif node.nodetype == 'binary_op':
            self.visitar_operacion_binaria(node)
        elif node.nodetype == 'literal':
            return self.manejar_literal(node)
        else:
            raise Exception(f"Nodo desconocido: {node.nodetype}")

    def visitar_consts(self, node):
        print(f"Procesando nodo consts con {len(node.children)} declaraciones.")
        for const in node.chidren:
            if const.nodetype != 'const_decl':
                raise Exception(f"Nodo inesperado dentro de consts: {const}")
            self.visitar_consts_decl(const)

    def visitar_vars(self, node):
        for var in node.children:
            var_tipo = var.children[0].value  # Tipo
            var_nombre = var.children[1].value  # Nombre
            print(f"Registrando variable: {var_nombre} de tipo {var_tipo}")
            self.symbol_table.anyadir_simbolo(var_nombre, var_tipo)

    def visitar_main(self, node):
        print("Analizando función main...")
        for stmt in node.children:
            self.visitar(stmt)

    def visitar_print(self, node):
        expr = node.children[0]
        if expr.nodetype == 'literal':
            print(f"Validando print de literal: {expr.value}")
        elif expr.nodetype == 'id':
            var_nombre = expr.value
            self.symbol_table.buscar(var_nombre)  # Verificar si la variable está declarada
            print(f"Validando print de variable: {var_nombre}")
        else:
            raise Exception("Tipo de expresión no válida en print.")

 
    def visitar_operacion_binaria(self, node):
        tipo_izq = self.visitar(node.children[0])
        tipo_der = self.visitar(node.children[1])
        if node.value == '+':
            if tipo_izq == 'string' and tipo_der == 'string':
                return 'string'  # Concatenación de strings
            elif tipo_izq == 'string' and tipo_der == 'int':
                return 'string'  # Conversión implícita y concatenación
            elif tipo_izq == 'int' and tipo_der == 'string':
                return 'string'  # Conversión implícita y concatenación
            elif tipo_izq != tipo_der:
                raise Exception(f"Operación no válida entre {tipo_izq} y {tipo_der}.")
        elif node.value in ['-', '*', '/']:
            if tipo_izq != 'int' or tipo_der != 'int':
                raise Exception(f"Operación no válida: {node.value} solo es válida entre enteros.")
        return tipo_izq
    
    #def visit_return(self, node):
        subroutine_nombre = node.parent.value  # Asume que el nodo tiene un padre que representa la subrutina
        declared_return_type = self.symbol_table.functions[subroutine_nombre]['return_type']
        if declared_return_type == 'void':
            if len(node.children) > 0:
                raise Exception(f"La subrutina '{subroutine_nombre}' no debe devolver un valor, ya que su tipo es 'void'.")
        else:
            if len(node.children) == 0:
                raise Exception(f"La subrutina '{subroutine_nombre}' debe devolver un valor de tipo '{declared_return_type}'.")
            return_type = self.visitar(node.children[0])
            if return_type != declared_return_type:
                raise Exception(f"La subrutina '{subroutine_nombre}' debe devolver un valor de tipo '{declared_return_type}', pero devuelve '{return_type}'.")

    #def visit_subroutine_call(self, node):
        subroutine_nombre = node.value
        params_declarados = self.symbol_table.lookup_function(subroutine_nombre)['params']
        if len(params_declarados) != len(node.children):
            raise Exception(f"La subrutina '{subroutine_nombre}' esperaba {len(params_declarados)} parámetros, pero se pasaron {len(node.children)}.")
        for i, param in enumerate(node.children):
            param_tipo = self.visitar(param)
            if param_tipo != params_declarados[i]:
                raise Exception(f"El parámetro {i+1} debe ser de tipo {params_declarados[i]}, pero se encontró {param_tipo}.")

    def visitar_consts_decl(self, node):
        """Procesa una declaración de constante."""
        print(f"Procesando declaración de constante: {node}")
        const_tipo = node.children[0].value  # Tipo
        const_nombre = node.children[1].value  # Nombre
        const_valor = node.value  # Valor
        print(f"Registrando constante: {const_nombre} de tipo {const_tipo} con valor {const_valor}")
        self.symbol_table.anyadir_simbolo(const_nombre, const_tipo, es_const=True)

    def visitar_var_decl(self, node):
        """Procesa una declaración de variable."""
        print(f"Procesando declaración de variable: {node}")
        var_tipo = node.children[0].value  # Tipo
        var_nombre = node.children[1].value  # Nombre
        var_value = node.value  # Valor (puede ser un ASTNode o un literal)
        print(f"Registrando variable: {var_nombre} de tipo {var_tipo} con valor {var_value}")
        self.symbol_table.anyadir_simbolo(var_nombre, var_tipo, es_const=False)

    def visitar_subroutine_decl(self, node):
        """Procesa una declaración de subrutina."""
        print(f"Procesando declaración de subrutina: {node}")
        subroutine_tipo = node.children[0].value  # Tipo de retorno
        subroutine_nombre = node.children[1].value  # Nombre de la subrutina
        params = node.children[2]  # Parámetros
        cuerpo = node.children[3]  # Cuerpo de la subrutina

        # Registrar la subrutina en la tabla de símbolos
        print(f"Registrando subrutina: {subroutine_nombre} con tipo de retorno {subroutine_tipo} y parámetros {params}")
        self.symbol_table.anyadir_func(subroutine_nombre, subroutine_tipo, params)

        # Analizar los parámetros
        for param in params:
            if param.nodetype != 'param':
                raise Exception(f"Nodo inesperado dentro de los parámetros de la subrutina '{subroutine_nombre}': {param}")
            param_tipo = param.children[0].value  # Tipo del parámetro
            param_nombre = param.children[1].value  # Nombre del parámetro
            print(f"Registrando parámetro: {param_nombre} de tipo {param_tipo}")
            self.symbol_table.anyadir_simbolo(param_nombre, param_tipo)

        # Analizar el cuerpo de la subrutina
        for stmt in cuerpo:
            self.visitar(stmt)

    
    def visitar_llamada(self, node):
        """Procesa una llamada a subrutina."""
        print(f"Procesando llamada a subrutina: {node}")
        subroutine_nombre = node.children[0].value  # Nombre de la subrutina
        arguments = node.children[1]  # Argumentos pasados a la subrutina

        # Verificar si la subrutina está declarada
        subroutine_info = self.symbol_table.get_func(subroutine_nombre)
        params_declarados = subroutine_info['params']

        # Verificar que el número de argumentos coincida
        if len(arguments) != len(params_declarados):
            raise Exception(
                f"La subrutina '{subroutine_nombre}' esperaba {len(params_declarados)} parámetros, "
                f"pero se pasaron {len(arguments)}."
            )

        # Verificar que los tipos de los argumentos coincidan con los parámetros declarados
        for i, arg in enumerate(arguments):
            arg_tipo = self.visitar(arg)  # Determinar el tipo del argumento
            param_tipo = params_declarados[i]['type']  # Tipo del parámetro esperado
            if arg_tipo != param_tipo:
                raise Exception(
                    f"El parámetro {i + 1} de la subrutina '{subroutine_nombre}' debe ser de tipo '{param_tipo}', "
                    f"pero se encontró '{arg_tipo}'."
                )

        print(f"Llamada a la subrutina '{subroutine_nombre}' validada con éxito.")

    def manejar_literal(self, node):
        """Procesa un nodo de tipo literal."""
        print(f"Procesando literal: {node.value}")
        if isinstance(node.value, int):
            return 'int'
        elif isinstance(node.value, str):
            return 'string'
        else:
            raise Exception(f"Tipo de literal desconocido: {node.value}")