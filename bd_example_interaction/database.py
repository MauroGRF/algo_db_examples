import sqlite3

"""Inicializacion de la Base de datos (DB) con sqlite3 (SQL crudo)"""
# Creando (Si no existe) y conectandose a la DB
db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS question(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        q1 TEXT NOT NULL,
        q2 TEXT NOT NULL,
        q3 TEXT NOT NULL,
        q4 TEXT NOT NULL,
        answer INTEGER NOT NULL
    )
""")


# --- C: CREAR (Insertar registros) ---
def crear_pregunta(question, q1, q2, q3, q4, answer):
    cursor.execute(
        "INSERT INTO question (question, q1, q2, q3, q4, answer) VALUES (?, ?, ?, ?, ?, ?)",
        (question, q1, q2, q3, q4, answer),
    )
    db.commit()
    print("Pregunta agregada con éxito.")
    return cursor.lastrowid


# --- R: LEER (Consultar registros) ---
def leer_preguntas():
    cursor.execute("SELECT * FROM question")
    preguntas = cursor.fetchall()
    print("\n--- Lista de Preguntas ---")
    for row in preguntas:
        print(
            f"ID: {row[0]} | Pregunta: {row[1]} | "
            f"1) {row[2]} 2) {row[3]} 3) {row[4]} 4) {row[5]} | Correcta: {row[6]}"
        )
    print("-------------------------\n")



# --- R: LEER (Consultar UN registro) ---
def leer_una_pregunta(pregunta_id):
    cursor.execute("SELECT * FROM question WHERE id = ?", (pregunta_id,))
    row = cursor.fetchone()
    print(
            f"ID: {row[0]} | Pregunta: {row[1]} | "
            f"1) {row[2]} 2) {row[3]} 3) {row[4]} 4) {row[5]} | Correcta: {row[6]}"
        )
    print("-------------------------\n")

# --- U: ACTUALIZAR (Modificar registros) ---
def actualizar_pregunta(pregunta_id, nueva_question, nuevo_answer):
    cursor.execute(
        "UPDATE question SET question = ?, answer = ? WHERE id = ?",
        (nueva_question, nuevo_answer, pregunta_id),
    )
    db.commit()
    print(f"Pregunta con ID {pregunta_id} actualizada.")


# --- D: ELIMINAR (Borrar registros) ---
def eliminar_pregunta(pregunta_id):
    cursor.execute("DELETE FROM question WHERE id = ?", (pregunta_id,))
    db.commit()
    print(f"Pregunta con ID {pregunta_id} eliminada.")
