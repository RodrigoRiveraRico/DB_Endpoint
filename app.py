from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

dbhost = 'fastdb.c3.unam.mx'
dbname = 'epi_puma_censo_inegi_2020'
dbport = '5433'
dbuser = 'monitor'
dbpass = 'monitor123'

def conexion():
    conn_string = f'host={dbhost} dbname={dbname} user={dbuser} password={dbpass} port={dbport}'
    conn = psycopg2.connect(conn_string)
    return conn

@app.route('/')
def saludo():
    return jsonify({'hola':'mundo'})

@app.route('/variables')
def fetch_variables():
    conn = conexion()

    with conn.cursor() as curs:
        curs.execute("""
                     WITH aux AS (
                        SELECT id, name, '{}' AS available_grids, 0 AS "level_size", '{}' as "filter_fields"
                        FROM covariable
                        )
                    SELECT json_agg(aux) FROM aux
                     ;
                     """
                     )

        row = curs.fetchone() # Devuelve una tupla
    conn.close()
    return jsonify(row[0])

@app.route('/get-data/<id>')
def get_data(id):
    grid_id = request.args.get('grid_id') # mun | state | ageb
    levels_id = request.args.get('levels_id')
    filter_names = request.args.get('filter_names')
    filter_values = request.args.get('filter_values')

    conn = conexion()

    with conn.cursor() as curs:
        curs.execute(f"""
                     WITH aux AS (
                        SELECT id, '{grid_id}' as "grid_id", 0 as "level_id", cells_{grid_id} :: integer[] as cells, array_length(cells_{grid_id},1) as n
                        FROM covariable
                        WHERE id = {id}
                        )
                    SELECT json_agg(aux) FROM aux
                     ;
                     """
                     )

        row = curs.fetchone() # Devuelve una tupla
    conn.close()
    return jsonify(row[0])
    



if __name__ == '__main__':
    app.run(port=5000, debug=True)