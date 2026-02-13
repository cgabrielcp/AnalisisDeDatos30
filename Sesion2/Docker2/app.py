from flask import Flask

app = Flask(__name__)

@app.route('/api/hello')
def hello():
    return 'Hola Mundo desde Docker'

@app.route('/api/getData')
def getData():
    resultado = 'Mensajes'
    return resultado

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

