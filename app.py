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
                        SELECT id, 
                            CONCAT(name, '_-_', interval) AS name, 
                            ARRAY[mesh] :: varchar[] AS available_grids, 
                            0 AS "level_size", 
                            ARRAY[] :: varchar[] as "filter_fields"
                        FROM covariable
                        )
                    SELECT json_agg(aux) FROM aux
                     ;
                     """
                     )

        row = curs.fetchone() # Devuelve una tupla
    conn.close()
    return jsonify(row[0])

@app.route('/variables/<id>')
def variables_id(id):
    conn_string = f'host={dbhost} dbname={dbname} user={dbuser} password={dbpass} port={dbport}'
    conn = psycopg2.connect(conn_string)

    q = request.args.get('q', '*')
    offset = request.args.get('offset', 'null')
    limit = request.args.get('limit', 10)

    # Qstr = f"SELECT {q} FROM public.covariable WHERE id = {str(id)} LIMIT {str(limit)} OFFSET {str(offset)};"
    Qstr = f"SELECT id, 0 as level_id FROM public.covariable WHERE id = {str(id)} LIMIT {str(limit)} OFFSET {str(offset)};"
    # WHERE id = {str()}
    R_dict = {}
    with conn.cursor() as curs:
        curs.execute(Qstr)

        r = curs.fetchone()
        print(r)
        cols = [desc[0] for desc in curs.description]   #Nombre de las columnas
        R_dict = {columna: r[i] for i, columna in enumerate(cols)}  # Obtener la consulta como diccionario de pares nombre de la columna, valor en la columna.
        # print(r[0])
    
    # result = {'id': R_dict['id'], 'level_id': 0, 'data':{'name':R_dict['name']}}
    result = {'id': R_dict['id'], 'level_id': 0, 'data':{}}

    return jsonify(result)

@app.route('/get-data/<id>')
def get_data_id(id):
    conn = conexion()
    grid_id = request.args.get('grid_id') # mun | state | ageb

    # Desde la URL (Query Strings): (ej. levels_id=1,2,3)
    levels_id = request.args.get('levels_id', type=lambda v: v.split(','))
    filter_names = request.args.get('filter_names', type=lambda v: v.split(','))
    filter_values = request.args.get('filter_values', type=lambda v: v.split(','))

    # #Desde el body de la solicitud como JSON:
    # data = request.get_json()
    # levels_id = data.get('levels_id')
    # filter_names = data.get('filter_names')
    # filter_values = data.get('filter_values')

    # #Desde un formulario: (ej. levels_id=1,2,3 en el formulario)
    # levels_id = request.form.get('levels_id').split(',')
    # filter_names = request.form.get('filter_names').split(',')
    # filter_values = request.form.get('filter_values').split(',')

    with conn.cursor() as curs:
        curs.execute(f"""
                     WITH aux AS (
                        SELECT id, 
                            '{grid_id}' as "grid_id", 
                            0 as "level_id", 
                            cells_{grid_id} :: integer[] as cells, 
                            array_length(cells_{grid_id},1) as n
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
    app.run(host='0.0.0.0', port=2112)
