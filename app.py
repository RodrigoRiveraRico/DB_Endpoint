from flask import Flask, jsonify, request
import psycopg2
import os
import sys

if sys.version_info[0:2] != (3, 11):
    print("\n\t==== IMPORTANTE ====")
    print(f"Versión de Python del sistema: {sys.version_info[0]}.{sys.version_info[1]}")
    print("La plataforma fue probada con una versión de Python 3.11")
    print("\t====================\n")

app = Flask(__name__)

# Se obtienen las credenciales desde variables de entorno
dbhost = os.getenv('DB_HOST', 'fastdb.c3.unam.mx')
dbname = os.getenv('DB_NAME', 'epi_puma_censo_inegi_2020_monitor')
dbport = os.getenv('DB_PORT', '5433')
dbuser = os.getenv('DB_USER', 'monitor')
dbpass = os.getenv('DB_PASS', 'monitor123')

def get_connection():
    """Obtiene la conexión a la base de datos."""
    conn_string = f'host={dbhost} dbname={dbname} user={dbuser} password={dbpass} port={dbport}'
    return psycopg2.connect(conn_string)

@app.route('/')
def saludo():
    """Ruta de saludo inicial."""
    return jsonify({'hola': 'mundo'})

@app.route('/variables')
def fetch_variables():
    """Obtiene las variables de la base de datos."""
    with get_connection() as conn:
        with conn.cursor() as curs:
            query = """
                WITH aux AS (
                    SELECT id, 
                           CONCAT(name, '_-_', interval) AS name, 
                           ARRAY[mesh] :: varchar[] AS available_grids, 
                           0 AS level_size, 
                           ARRAY[] :: varchar[] AS filter_fields
                    FROM covariable
                )
                SELECT json_agg(aux) FROM aux;
            """
            curs.execute(query)
            row = curs.fetchone()  # Devuelve una tupla
    return jsonify(row[0])

@app.route('/variables/<id>')
def variables_id(id):
    """Obtiene una variable específica por su ID."""
    q = request.args.get('q', '*')
    offset = request.args.get('offset', '0')  # Cambiado a 0 por defecto
    limit = request.args.get('limit', 10)

    with get_connection() as conn:
        with conn.cursor() as curs:
            query = """
                SELECT id, 0 as level_id 
                FROM covariable 
                WHERE id = %s 
                LIMIT %s OFFSET %s;
            """
            curs.execute(query, (id, limit, offset))
            r = curs.fetchone()

            if not r:
                return jsonify({'error': 'ID no encontrado'}), 404

            cols = [desc[0] for desc in curs.description]  # Nombres de las columnas
            result = {columna: r[i] for i, columna in enumerate(cols)}
    
    return jsonify(result)

@app.route('/get-data/<id>')
def get_data_id(id):
    """Obtiene datos específicos de una covariable por ID y filtros opcionales."""
    grid_id = request.args.get('grid_id')  # mun | state | ageb
    levels_id = request.args.get('levels_id', type=lambda v: v.split(','))
    filter_names = request.args.get('filter_names', type=lambda v: v.split(','))
    filter_values = request.args.get('filter_values', type=lambda v: v.split(','))

    if not grid_id:
        return jsonify({'error': 'grid_id es requerido'}), 400

    with get_connection() as conn:
        with conn.cursor() as curs:
            query = f"""
                WITH aux AS (
                    SELECT id, 
                           %s as grid_id, 
                           0 as level_id, 
                           cells_{grid_id} :: integer[] AS cells, 
                           array_length(cells_{grid_id}, 1) AS n
                    FROM covariable
                    WHERE id = %s
                )
                SELECT json_agg(aux) FROM aux;
            """
            curs.execute(query, (grid_id, id))
            row = curs.fetchone()

    if not row:
        return jsonify({'error': 'ID no encontrado'}), 404

    return jsonify(row[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2112)
