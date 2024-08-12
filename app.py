from flask import Flask, jsonify
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
        curs.execute("""
                     WITH aux AS (
                        SELECT id, name, mesh AS available_grids, 0 AS "level_size", '{}' as "filter_fields"
                        FROM covariable
                        )
                    SELECT json_agg(aux) FROM aux
                     ;
                     """
                     )

        row = curs.fetchone() # Devuelve una tupla

    return jsonify(row[0])

    



if __name__ == '__main__':
    app.run(port=5000, debug=True)