casos = {
    "No variables duplicadas (válido)": '''
    int x = 10;
    string y = "Hola";
    ''',
    "Variables duplicadas (inválido)": '''
    int x = 10;
    int x = 20;  
    ''',
    "Reasignar constantes (inválido)": '''
    CONST int x = 10;
    x = 20;   
    ''',
    "Concatenación de strings (válido)": '''
    string x = "Hola";
    string y = " Mundo";
    string z = x + y;
    print(z);
    ''',
    "Subrutina con parámetros válidos": '''
    SUBROUTINE void myFunc(int a, string b) DO
        print(a);
        print(b);
    END
    myFunc(10, "Hola");
    ''',
    "Subrutina con parámetros inválidos": '''
    SUBROUTINE void myFunc(int a, string b) DO
        print(a);
        print(b);
    END
    myFunc("Hola", 10);  
    ''',
}
