import database_m2m

# Crear preguntas y etiquetas por separado
p_francia = database_m2m.crear_pregunta("¿Cual es la capital de Francia?")
p_mate = database_m2m.crear_pregunta("¿Cuanto es 2 + 2?")
p_quijote = database_m2m.crear_pregunta("¿Quien escribio Don Quijote?")

e_geo = database_m2m.crear_etiqueta("geografia")
e_mate = database_m2m.crear_etiqueta("matematicas")
e_lit = database_m2m.crear_etiqueta("literatura")
e_cult = database_m2m.crear_etiqueta("cultura")

# Relacionar (M2M): la misma etiqueta en varias preguntas y al reves
database_m2m.agregar_etiqueta(p_francia, e_geo)  # Paris -> geografia
database_m2m.agregar_etiqueta(p_francia, e_cult)  # Paris -> cultura
database_m2m.agregar_etiqueta(p_mate, e_mate)  # 2 + 2 -> matematicas
database_m2m.agregar_etiqueta(p_mate, e_cult)  # 2 + 2 -> cultura
database_m2m.agregar_etiqueta(p_quijote, e_lit)  # Quijote -> literatura
database_m2m.agregar_etiqueta(p_quijote, e_cult)  # Quijote -> cultura

# Leer la relacion desde el lado de las preguntas
database_m2m.leer_preguntas()

# Leer la relacion desde el lado de las etiquetas
database_m2m.leer_preguntas_de_etiqueta(e_cult)

# Actualizar
database_m2m.actualizar_etiqueta(e_geo, "geografia y monde")

# Quitar un vinculo (la pregunta de Paris ya no es de geografia)
database_m2m.quitar_etiqueta(p_francia, e_geo)

# Eliminar (se borran los vinculos, no la otra tabla)
database_m2m.eliminar_etiqueta(e_cult)
database_m2m.eliminar_pregunta(p_mate)

# Ver el resultado
database_m2m.leer_preguntas()

# Cerrar la sesion al terminar
database_m2m.cerrar_db()
