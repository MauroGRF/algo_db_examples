import database_fk_sqlite

# Crear dos quizzes
q1 = database_fk_sqlite.crear_quiz("Quizz de Historia")
q2 = database_fk_sqlite.crear_quiz("Quizz de Matematicas")

# Crear preguntas ya asignadas a un quiz (FK)
p1 = database_fk_sqlite.crear_pregunta(q1, "¿En que ano empezo la Revolution Francesa?", 1789)
p2 = database_fk_sqlite.crear_pregunta(q1, "¿Quien fue el primer emperador de Roma?", 2)
p3 = database_fk_sqlite.crear_pregunta(q2, "¿Cuanto es 7 x 8?", 3)

# Leer la relacion con un JOIN: un quiz con sus muchas preguntas
database_fk_sqlite.leer_quizzes()

# Filtrar por la FK
database_fk_sqlite.leer_preguntas_de_quiz(q1)

# Actualizar datos
database_fk_sqlite.actualizar_quiz(q1, "Quizz de Historia Universal")

# Actualizar la FK: la pregunta p3 pasa al quiz de Historia
database_fk_sqlite.mover_pregunta(p3, q1)

# Eliminar
database_fk_sqlite.eliminar_pregunta(p2)
database_fk_sqlite.eliminar_quiz(q2)  # ON DELETE CASCADE: borra sus preguntas

# Ver el resultado
database_fk_sqlite.leer_quizzes()

# Cerrar la conexion al terminar
database_fk_sqlite.db.close()
