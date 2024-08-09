from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def saludo():
    return jsonify({'hola':'mundo'})


@app.route('/variables/:id:')
def variables_id():
    q = request.args.get('q', '*')
    offset = request.args.get('offset', None)
    limit = request.args.get('limit', 10)

    x = [
        {'a': 1},
        {'b' : 2}
    ]

    print(len(x))
    return x

if __name__ == '__main__':
    app.run(port=8000)