from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

dbhost = 'fastdb.c3.unam.mx'
dbname = 'epi_puma_censo_inegi_2020'
dbport = '5433'
dbuser = 'monitor'
dbpass = 'monitor123'

@app.route('/')
def saludo():
    return jsonify({'hola':'mundo'})

@app.route('/variables')
def fetch_variables():
    conn_string = f'host={dbhost} dbname={dbname} user={dbuser} password={dbpass} port={dbport}'
    conn = psycopg2.connect(conn_string)

    with conn.cursor() as curs:
        curs.execute("""with aux as (
                        select id, name, mesh
                            from covariable
                        )
                        select json_agg(aux) from aux;"""
                     )

        r = curs.fetchone()

        # print(r[0][0])


    return jsonify(r[0])

    


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
    app.run(port=5000, debug=True)