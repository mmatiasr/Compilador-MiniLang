from parser_minilang import parser
from semantic_analyzer import SemanticAnalyzer

if __name__ == "__main__":
    # Entrada del programa
    data = '''
    CONST int x = 10;
    CONST int x = 20;
    CONST string message = "Hola!";
    SUBROUTINE void main() DO
        print(message);
    END
    '''

    # Generar el AST con el parser
    ast = parser.parse(data)
    print("AST Generado:", ast)

    # Ejecutar el analizador semántico
    print("\nIniciando análisis semántico...")
    analyzer = SemanticAnalyzer(ast)
    analyzer.analyze()
    print("\nAnálisis semántico completado.")
