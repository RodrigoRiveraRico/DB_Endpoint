<h1 align="center">Servicio de endpoints para Chilam Project</h1>

<p align="center">~ Centro de Ciencias de la Complejidad, UNAM ~</p>

<br/>

## Contenido

* [Descripción](#descripcion)

* [Ejecución](#ejecución)

    * [WINDOWS](#windows)

    * [LINUX](#linux)

## Descripción
Este servicio de endpoints fue creado con la intención de incorporar una nueva fuente de datos para el proyecto Chilam. Click [aquí](chilam) para ir al repositorio del proyecto.

Los endpoints creados siguen la arquitectura propuesta en [este](conabio) repositorio.

Los endpoints se crean a partir de los datos almacenados en una base de datos en `PostgreSQL`. La descripción de los datos con los que se trabaja es la siguiente:

* Tipo de dato:

    | columna | tipo |
    |:--:|:--:|
    | **id** | integer not null |
    | **name** | text |
    | **interval** | text |
    | **mesh** | text |
    | **cells_{mesh}** | character varying[] |

**Nota:** Nótese que _{mesh}_ en el nombre de la columna _cells\_{mesh}_ corresponde con uno de los valores almacenados en la columna _mesh_, de modo que hay tantas columnas _cells\_{mesh}_ como valores distintos en _mesh_.


* Estructura:

    | id | name | interval | mesh | cells_mun | cells_state |
    |:--:|:--:|:--:|:--:|:--:|:--:|
    | 1 | Población Total | 100:200 | mun | [01432, 02345, 04112] | null |
    | 2 | Población Total | 200:300 | mun | [02243, 10353, 11221] | null |
    | 3 | Población Total | 300:400 | state | null | [10] | 

**Nota:** Los datos con los que se trabaja están almacenados en una sola tabla.

[chilam]: (https://github.com/RodrigoRiveraRico/chilam_project)

[conabio]: (https://github.com/CONABIO/species_v3.0)

## Ejecución

El servicio fue probado con Python 3.11

### WINDOWS

```cmd
flask --app app run --port=2112 --host=0.0.0.0
```

### LINUX 

```bash
flask --app app run --port=2112 --host=0.0.0.0
```

> host=0.0.0.0 para que el servicio se pueda visualizar desde cualquier dispositivo conectado a la red del servidor donde se ejecuta el servicio.

