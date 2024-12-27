from parser_minilang import parser
from semantic_analyzer import SemanticAnalyzer
from casos_test import casos

if __name__ == "__main__":
    for test_name, code in casos.items():
        print(f"\n--- {test_name} ---")
        try:
            # Generar el AST
            ast = parser.parse(code)
            print("AST Generado:", ast)

            # Ejecutar el análisis semántico
            analyzer = SemanticAnalyzer(ast)
            analyzer.analyze()
            print("Análisis semántico completado.\n")
        except Exception as e:
            print(f"Error: {e}\n")
