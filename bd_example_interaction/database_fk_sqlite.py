import sqlite3

"""Inicializacion de la Base de datos (DB) con sqlite3 (SQL crudo) - RELACION FK (1:N)"""
# Creando (Si no existe) y conectandose a la DB
db = sqlite3.connect("db_fk_sqlite.sqlite3")
cursor = db.cursor()

# Importante: sqlite3 no aplica las FK ni el ON DELETE CASCADE hasta que se lo pidas
cursor.execute("PRAGMA foreign_keys = ON")

# Un QUIZ tiene MUCHAS preguntas (1:N) -> la FK vive en la tabla hija (question)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS question(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL,
        correcta INTEGER NOT NULL,
        quiz_id INTEGER NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
    )
""")


def _obtener_quiz(quiz_id):
    cursor.execute("SELECT id FROM quiz WHERE id = ?", (quiz_id,))
    return cursor.fetchone()


# --- C: CREAR (Insertar registros) ---
def crear_quiz(titulo):
    cursor.execute("INSERT INTO quiz (titulo) VALUES (?)", (titulo,))
    db.commit()
    print(f"Quiz '{titulo}' agregado con éxito.")
    return cursor.lastrowid


def crear_pregunta(quiz_id, texto, correcta):
    if _obtener_quiz(quiz_id) is None:
        print(f"No existe un quiz con ID {quiz_id}.")
        return
    cursor.execute(
        "INSERT INTO question (texto, correcta, quiz_id) VALUES (?, ?, ?)",
        (texto, correcta, quiz_id),
    )
    db.commit()
    print(f"Pregunta agregada al quiz con ID {quiz_id}.")
    return cursor.lastrowid


# --- R: LEER (Consultar registros) ---
def leer_quizzes():
    # LEFT JOIN para traer los quizzes aunque no tengan preguntas
    cursor.execute("""
        SELECT quiz.id, quiz.titulo, question.id, question.texto, question.correcta
        FROM quiz
        LEFT JOIN question ON question.quiz_id = quiz.id
        ORDER BY quiz.id, question.id
    """)
    print("\n--- Lista de Quizzes (con sus preguntas) ---")
    quiz_actual = None
    for quiz_id, titulo, p_id, texto, correcta in cursor.fetchall():
        # El ORDER BY agrupa las preguntas del mismo quiz: el titulo se imprime una sola vez
        if quiz_id != quiz_actual:
            print(f"Quiz #{quiz_id}: {titulo}")
            quiz_actual = quiz_id
        if p_id is not None:
            print(f"   - #{p_id} {texto} | Correcta: {correcta}")
    print("------------------------------------------\n")


def leer_preguntas_de_quiz(quiz_id):
    cursor.execute(
        "SELECT id, texto FROM question WHERE quiz_id = ? ORDER BY id", (quiz_id,)
    )
    print(f"\n--- Preguntas del quiz con ID {quiz_id} ---")
    for p_id, texto in cursor.fetchall():
        print(f"#{p_id} {texto}")
    print("-------------------------------------\n")


# --- U: ACTUALIZAR (Modificar registros) ---
def actualizar_quiz(quiz_id, nuevo_titulo):
    if _obtener_quiz(quiz_id) is None:
        print(f"No existe un quiz con ID {quiz_id}.")
        return
    cursor.execute("UPDATE quiz SET titulo = ? WHERE id = ?", (nuevo_titulo, quiz_id))
    db.commit()
    print(f"Quiz con ID {quiz_id} actualizado.")


def mover_pregunta(pregunta_id, nuevo_quiz_id):
    # Cambiar la FK: la pregunta pasa a pertenecer a otro quiz
    if _obtener_quiz(nuevo_quiz_id) is None:
        print(f"No existe un quiz con ID {nuevo_quiz_id}.")
        return
    cursor.execute(
        "UPDATE question SET quiz_id = ? WHERE id = ?", (nuevo_quiz_id, pregunta_id)
    )
    db.commit()
    print(f"Pregunta #{pregunta_id} movida al quiz con ID {nuevo_quiz_id}.")


# --- D: ELIMINAR (Borrar registros) ---
def eliminar_pregunta(pregunta_id):
    cursor.execute("DELETE FROM question WHERE id = ?", (pregunta_id,))
    db.commit()
    print(f"Pregunta #{pregunta_id} eliminada.")


def eliminar_quiz(quiz_id):
    # El ON DELETE CASCADE de la FK borra tambien las preguntas del quiz
    cursor.execute("DELETE FROM quiz WHERE id = ?", (quiz_id,))
    db.commit()
    print(f"Quiz con ID {quiz_id} eliminado (y sus preguntas).")
