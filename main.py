import os
from parser_minilang import parser
from semantic_analyzer import SemanticAnalyzer

def leer_archivo(archivo):
    """Lee el contenido de un archivo y lo devuelve como una cadena."""
    # Obtener el directorio actual del script
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(directorio, archivo)

    with open(ruta_completa, 'r') as f:
        return f.read()

if __name__ == "__main__":
    # Especificar el archivo que deseas probar
    archivo_prueba = "programa_valido.txt"  # Cambiar a "programa_invalido.txt" según el caso
    print(f"Procesando archivo: {archivo_prueba}\n")

    try:
        # Leer el contenido del archivo
        codigo = leer_archivo(archivo_prueba)

        # Generar el AST
        ast = parser.parse(codigo)
        print("AST Generado:")
        print(ast)

        # Ejecutar el análisis semántico
        print("\nIniciando análisis semántico...")
        analyzer = SemanticAnalyzer(ast)
        analyzer.analizar()
        print("\nAnálisis semántico completado. El programa es válido.")

    except Exception as e:
        print(f"\nError encontrado durante la ejecución: {e}")