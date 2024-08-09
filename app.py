from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/saluditos')
def saludo():
    return jsonify({'hola':'mundo'})



if __name__ == '__main__':
    app.run(port=8000)