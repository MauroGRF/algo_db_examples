import database_orm

# Probando las operaciones CRUD
p1 = database_orm.crear_pregunta("¿Cual es la capital de Francia?", "Paris", "Lyon", "Roma", "Berlin", 1)
p2 = database_orm.crear_pregunta("¿Cuanto es 2 + 2?", "3", "5", "4", "10", 3)

# Leer los datos insertados
database_orm.leer_preguntas()

# Actualizar la pregunta con ID 1
database_orm.actualizar_pregunta(p1, "¿Cual es la capital de España?", 1)

# Eliminar la pregunta con ID 2
database_orm.eliminar_pregunta(p2)

# Leer nuevamente para ver los cambios
database_orm.leer_preguntas()

# Cerrar la sesion al terminar
database_orm.cerrar_db()
