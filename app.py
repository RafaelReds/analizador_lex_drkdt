import re
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

def analizar_codigo(code):
    tokens = []
    errores = []
    
    # Definiciones de patrones
    patrones = {
        'ITEM': r'\b(XP|HP|ITEM|PRINT)\b',
        'ASSIGN': r'=',
        'NUMBER': r'\b\d+(\.\d+)?\b',
        'STRING': r'"[^"]*"|\b([A-Za-z]+)\b',
        'END': r';'
    }
    
    # Tokenizar línea por línea
    lineas = code.splitlines()
    
    # Verificar si hay código
    if not lineas:
        errores.append("Error: El código está vacío.")
        return tokens, errores

    # Verificar presencia de [INIT] y [STOP]
    tiene_init = any('[INIT]' in linea for linea in lineas)
    tiene_stop = any('[STOP]' in linea for linea in lineas)

    if not tiene_init:
        errores.append("Error: Falta la etiqueta [INIT] al inicio del código.")
    if not tiene_stop:
        errores.append("Error: Falta la etiqueta [STOP] al final del código.")

    # Verificar si INIT está en la primera línea y STOP en la última
    if tiene_init and '[INIT]' not in lineas[0]:
        errores.append(f"Error en línea 1: [INIT] debe estar al inicio del código.")

    if tiene_stop and '[STOP]' not in lineas[-1]:
        errores.append(f"Error: [STOP] debe estar en la última línea del código.")

    # Tokenizar y analizar línea por línea
    for num_linea, linea in enumerate(lineas, start=1):
        linea = linea.strip()

        # Ignorar líneas vacías
        if not linea:
            continue

        # Omitir validaciones en líneas de INIT y STOP
        if linea in ['[INIT]', '[STOP]']:
            continue

        # Verificar terminación de línea
        if not linea.endswith(';'):
            errores.append(f"Error en línea {num_linea}: falta ';' al final de la línea.")
            continue

        # Verificar asignaciones correctas
        if '=>' in linea:
            errores.append(f"Error en línea {num_linea}: operador inválido '=>' en lugar de '='.")
            continue

        # Verificar formato de número decimal con punto
        if ',' in linea:
            errores.append(f"Error en línea {num_linea}: número decimal inválido, use punto (.) en lugar de coma (,).")
            continue

        # Tokenizar la línea
        pos = 0
        while pos < len(linea):
            match = None
            for tipo, patron in patrones.items():
                regex = re.compile(patron)
                match = regex.match(linea, pos)
                if match:
                    valor = match.group(0)
                    tokens.append((tipo, valor))
                    pos = match.end()
                    break
            if not match:
                errores.append(f"Error en línea {num_linea}: token no reconocido '{linea[pos]}'.")
                break
            pos += 1
    
    return tokens, errores

@app.route('/')
def index():
    return render_template('index.html', code="", tokens=[], errores=[])

@app.route('/open-file', methods=['POST'])
def open_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    file_content = file.read().decode('utf-8')
    return render_template('index.html', code=file_content, tokens=[], errores=[])

@app.route('/save-file', methods=['POST'])
def save_file():
    code_content = request.form['code']
    filename = request.form.get('filename', 'codigo_guardado.txt')  # Obtener nombre del archivo
    filepath = os.path.join(os.getcwd(), filename)  # Guardar en la misma carpeta

    try:
        with open(filepath, 'w') as file:
            file.write(code_content)
        errores = [f"Archivo guardado exitosamente como '{filename}'."]
    except Exception as e:
        errores = [f"Error al guardar el archivo: {str(e)}"]

    return render_template('index.html', code=code_content, tokens=[], errores=errores)

@app.route('/compilar', methods=['POST'])
def compilar():
    code_content = request.form['code']
    tokens, errores = analizar_codigo(code_content)
    return render_template('index.html', code=code_content, tokens=tokens, errores=errores)

if __name__ == '__main__':
    app.run(debug=True)
