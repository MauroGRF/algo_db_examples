import database

# Probando las operaciones CRUD
p1 = database.crear_pregunta("¿Cual es la capital de Francia?", "Paris", "Lyon", "Roma", "Berlin", 1)
p2 = database.crear_pregunta("¿Cuanto es 2 + 2?", "3", "5", "4", "10", 3)

# Leer los datos insertados
database.leer_preguntas()

# Actualizar la pregunta con ID 1
database.actualizar_pregunta(p1, "¿Cual es la capital de España?", 1)

# Eliminar la pregunta con ID 2
database.eliminar_pregunta(p2)

# Leer nuevamente para ver los cambios
database.leer_preguntas()

# Cerrar la conexion al terminar
database.db.close()
