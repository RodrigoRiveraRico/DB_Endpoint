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
    conn.close()

    return jsonify(r[0])

    


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
    conn_string = f'host={dbhost} dbname={dbname} user={dbuser} password={dbpass} port={dbport}'
    conn = psycopg2.connect(conn_string)

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

    rensponse_data = {
        'id':int(id),
        'levels_id':levels_id,
        'filter_names': filter_names,
        'filter_values' : filter_values
    }

    return jsonify(rensponse_data)


if __name__ == '__main__':
    app.run(port=5000, debug=True)