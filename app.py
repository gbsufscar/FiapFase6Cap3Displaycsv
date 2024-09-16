from flask import Flask, request, render_template
import pandas as pd

# Inicializa o Flask
app = Flask(__name__)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o arquivo CSV
@app.route('/display', methods=['POST'])
def display_file():
    file = request.files['file'] # Pega o arquivo enviado pelo formulário
    if not file:
        return "No file"

    # Tenta ler o arquivo com diferentes codificações
    try:
        df = pd.read_csv(file, delimiter=";")
    except UnicodeDecodeError:
        file.seek(0)  # Reseta o ponteiro do arquivo
        try:
            df = pd.read_csv(file, encoding='latin1', delimiter=";") # Tenta outra codificação
        except UnicodeDecodeError:
            file.seek(0)  # Reseta o ponteiro do arquivo
            df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=";") # Tenta outra codificação

    # Renderiza o template com os dados do arquivo CSV
    return render_template('display.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True) # Inicia o servidor em modo de debug