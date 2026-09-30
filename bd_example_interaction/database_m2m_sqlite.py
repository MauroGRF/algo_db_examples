import sqlite3

"""Inicializacion de la Base de datos (DB) con sqlite3 (SQL crudo) - RELACION M2M"""
# Creando (Si no existe) y conectandose a la DB
db = sqlite3.connect("db_m2m_sqlite.sqlite3")
cursor = db.cursor()

# Importante: sqlite3 no aplica las FK ni el ON DELETE CASCADE hasta que se lo pidas
cursor.execute("PRAGMA foreign_keys = ON")

# Una pregunta puede tener MUCHAS etiquetas y una etiqueta puede estar en MUCHAS preguntas.
# Ninguna de las dos tablas tiene FK entre si: la union se guarda en una tabla aparte.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pregunta(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS etiqueta(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
""")

# Tabla intermedia: dos FK + clave compuesta (una pregunta no puede repetir la misma etiqueta)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pregunta_etiqueta(
        pregunta_id INTEGER NOT NULL,
        etiqueta_id INTEGER NOT NULL,
        PRIMARY KEY (pregunta_id, etiqueta_id),
        FOREIGN KEY (pregunta_id) REFERENCES pregunta(id) ON DELETE CASCADE,
        FOREIGN KEY (etiqueta_id) REFERENCES etiqueta(id) ON DELETE CASCADE
    )
""")


def _obtener_pregunta(pregunta_id):
    cursor.execute("SELECT id FROM pregunta WHERE id = ?", (pregunta_id,))
    return cursor.fetchone()


def _obtener_etiqueta(etiqueta_id):
    cursor.execute("SELECT id, nombre FROM etiqueta WHERE id = ?", (etiqueta_id,))
    return cursor.fetchone()


# --- C: CREAR (Insertar registros) ---
def crear_pregunta(texto):
    cursor.execute("INSERT INTO pregunta (texto) VALUES (?)", (texto,))
    db.commit()
    print(f"Pregunta agregada con éxito.")
    return cursor.lastrowid


def crear_etiqueta(nombre):
    cursor.execute("INSERT INTO etiqueta (nombre) VALUES (?)", (nombre,))
    db.commit()
    print(f"Etiqueta agregada con éxito.")
    return cursor.lastrowid


def agregar_etiqueta(pregunta_id, etiqueta_id):
    if _obtener_pregunta(pregunta_id) is None or _obtener_etiqueta(etiqueta_id) is None:
        print("No se pudo agregar la etiqueta (ids inexistentes).")
        return
    # INSERT OR IGNORE: la clave compuesta evita repetir el mismo vinculo
    cursor.execute(
        "INSERT OR IGNORE INTO pregunta_etiqueta (pregunta_id, etiqueta_id) VALUES (?, ?)",
        (pregunta_id, etiqueta_id),
    )
    db.commit()
    nombre = _obtener_etiqueta(etiqueta_id)[1]
    print(f"Etiqueta '{nombre}' agregada a la pregunta #{pregunta_id}.")


# --- R: LEER (Consultar registros) ---
def leer_preguntas():
    # GROUP_CONCAT junta todas las etiquetas de cada pregunta en una sola fila
    cursor.execute("""
        SELECT pregunta.id, pregunta.texto, GROUP_CONCAT(etiqueta.nombre, ', ')
        FROM pregunta
        LEFT JOIN pregunta_etiqueta ON pregunta_etiqueta.pregunta_id = pregunta.id
        LEFT JOIN etiqueta ON etiqueta.id = pregunta_etiqueta.etiqueta_id
        GROUP BY pregunta.id
        ORDER BY pregunta.id
    """)
    print("\n--- Lista de Preguntas (con sus etiquetas) ---")
    for p_id, texto, etiquetas in cursor.fetchall():
        print(f"#{p_id} {texto} | Etiquetas: {etiquetas or '(sin etiquetas)'}")
    print("--------------------------------------------\n")


def leer_preguntas_de_etiqueta(etiqueta_id):
    etiqueta = _obtener_etiqueta(etiqueta_id)
    if etiqueta is None:
        print(f"No existe una etiqueta con ID {etiqueta_id}.")
        return
    cursor.execute("""
        SELECT pregunta.id, pregunta.texto
        FROM pregunta
        JOIN pregunta_etiqueta ON pregunta_etiqueta.pregunta_id = pregunta.id
        WHERE pregunta_etiqueta.etiqueta_id = ?
        ORDER BY pregunta.id
    """, (etiqueta_id,))
    print(f"\n--- Preguntas con la etiqueta '{etiqueta[1]}' ---")
    for p_id, texto in cursor.fetchall():
        print(f"#{p_id} {texto}")
    print("---------------------------------------------\n")


# --- U: ACTUALIZAR (Modificar registros) ---
def actualizar_etiqueta(etiqueta_id, nuevo_nombre):
    if _obtener_etiqueta(etiqueta_id) is None:
        print(f"No existe una etiqueta con ID {etiqueta_id}.")
        return
    cursor.execute("UPDATE etiqueta SET nombre = ? WHERE id = ?", (nuevo_nombre, etiqueta_id))
    db.commit()
    print(f"Etiqueta con ID {etiqueta_id} actualizada.")


def quitar_etiqueta(pregunta_id, etiqueta_id):
    # En M2M no se edita una FK: se borra la fila de la tabla intermedia
    etiqueta = _obtener_etiqueta(etiqueta_id)
    if etiqueta is None:
        print(f"No existe una etiqueta con ID {etiqueta_id}.")
        return
    cursor.execute(
        "DELETE FROM pregunta_etiqueta WHERE pregunta_id = ? AND etiqueta_id = ?",
        (pregunta_id, etiqueta_id),
    )
    db.commit()
    print(f"Etiqueta '{etiqueta[1]}' quitada de la pregunta #{pregunta_id}.")


# --- D: ELIMINAR (Borrar registros) ---
def eliminar_pregunta(pregunta_id):
    cursor.execute("DELETE FROM pregunta WHERE id = ?", (pregunta_id,))
    db.commit()
    print(f"Pregunta #{pregunta_id} eliminada (y sus vinculos con etiquetas).")


def eliminar_etiqueta(etiqueta_id):
    cursor.execute("DELETE FROM etiqueta WHERE id = ?", (etiqueta_id,))
    db.commit()
    print(f"Etiqueta con ID {etiqueta_id} eliminada (y sus vinculos).")
