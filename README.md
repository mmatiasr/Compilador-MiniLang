Este programa es un compilador, diseñado para procesar y comprobar que un fichero que contiene código cumple un formato especificado. Con esto, conseguimos traducir un codigo fuente en MiniLang a 
un lenguaje maquina ejecutable, gestionando estructuras de datos y control de flujo basicas. La primera fase del programa consiste en implementar un analizador léxico que lea el
codigo fuente y lo convierta en una secuencia de tokens. Estos tokens incluiran identificadores, palabras clave, operadores y
literales, lo que permitira una representacion estructurada del codigo. A continuación, se procederá con el análisis sintáctico,
que construirá un Árbol de Sintaxis Abstracta (AST) a partir de la secuencia de tokens generada por el lexer. Durante esta
fase, es esencial manejar correctamente las declaraciones de variables, definiciones de subrutinas y estructuras de control,
además de implementar mecanismos para reportar errores sintacticos.
Una vez que se haya creado el AST, se realizara un análisis semantico del código.
