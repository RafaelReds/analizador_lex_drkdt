import re

# Función para eliminar comentarios y espacios en blanco innecesarios
def procesar_codigo(codigo):
    # Eliminar comentarios de línea que comienzan con //
    codigo = re.sub(r'//.*', '', codigo)
    
    # Eliminar comentarios de bloque /* ... */
    codigo = re.sub(r'/\*.*?\*/', '', codigo, flags=re.DOTALL)
    
    # Eliminar saltos de línea y múltiples espacios
    codigo = re.sub(r'\s+', ' ', codigo)
    
    # Retornar el código limpio y listo para tokenizar
    return codigo.strip()

# Definimos los patrones de los tokens usando expresiones regulares
token_specification = [
    ('PRINT',    r'\bPRINT\b'),       # Palabra clave PRINT
    ('XP',       r'\bXP\b'),           # Variable XP
    ('HP',       r'\bHP\b'),           # Variable HP
    ('ITEM',     r'\bITEM\b'),         # Variable ITEM
    ('STATUS',   r'\bALIVE\b|\bKO\b'), # STATUS: booleano ALIVE o KO
    ('NUMBER',   r'\d+(\.\d+)?'),      # Números generales
    ('ASSIGN',   r'='),                # Operador de asignación
    ('END',      r';'),                # Fin de línea
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),  # Identificadores (variables)
    ('OP',       r'[+\-*/]'),          # Operadores matemáticos estándar
    ('LOOT',     r'\bLOOT\b'),         # Operador LOOT (suma)
    ('DAMAGE',   r'\bDAMAGE\b'),       # Operador DAMAGE (resta)
    ('MULTI',    r'\bMULTI\b'),        # Operador MULTI (multiplicación)
    ('SPLIT',    r'\bSPLIT\b'),        # Operador SPLIT (división)
    ('MATCH',    r'\bMATCH\b'),        # Igual a (==)
    ('MISMATCH', r'\bMISMATCH\b'),     # No igual a (!=)
    ('LOWER',    r'\bLOWER\b'),        # Menor que (<)
    ('HIGHER',   r'\bHIGHER\b'),       # Mayor que (>)
    ('NOTHIGHER', r'\bNOTHIGHER\b'),   # Menor o igual (<=)
    ('NOTLOWER', r'\bNOTLOWER\b'),     # Mayor o igual (>=)
    ('LPAREN',   r'\('),               # Paréntesis izquierdo
    ('RPAREN',   r'\)'),               # Paréntesis derecho
    ('SKIP',     r'[ \t]+'),           # Espacios en blanco y tabulaciones
]

# Compilamos las expresiones regulares en un solo patrón
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

# Función para generar tokens a partir del código procesado
def tokenize(codigo):
    for match in re.finditer(token_regex, codigo):
        kind = match.lastgroup
        value = match.group()
        
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'SKIP':
            continue  # Ignoramos espacios en blanco y tabulaciones
        
        yield kind, value

# Función principal que procesa y tokeniza el código de entrada
def analizar(codigo):
    # Procesar el código para eliminar comentarios y espacios
    codigo_procesado = procesar_codigo(codigo)

    # Generar los tokens
    tokens = list(tokenize(codigo_procesado))

    # Retornar los tokens generados
    return tokens
