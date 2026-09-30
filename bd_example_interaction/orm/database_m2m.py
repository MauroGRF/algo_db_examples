from pathlib import Path

from sqlalchemy import Column, ForeignKey, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

"""Inicializacion de la Base de datos (DB) con SQLAlchemy (ORM) - RELACION M2M"""
# La DB se guarda siempre en la carpeta de este archivo, sin importar desde donde se ejecute
BASE_DIR = Path(__file__).resolve().parent

# Una pregunta puede tener MUCHAS etiquetas y una etiqueta puede estar en MUCHAS preguntas.
# No hay FK en ninguno de los dos lados: la union se guarda en una tabla aparte.
engine = create_engine(f"sqlite:///{BASE_DIR / 'db_m2m.sqlite3'}")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# Tabla intermedia (solo tiene las dos FK y su clave compuesta)
pregunta_etiqueta = Table(
    "pregunta_etiqueta",
    Base.metadata,
    Column("pregunta_id", ForeignKey("pregunta.id"), primary_key=True),
    Column("etiqueta_id", ForeignKey("etiqueta.id"), primary_key=True),
)


class Pregunta(Base):
    __tablename__ = "pregunta"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    texto: Mapped[str] = mapped_column()

    # secondary = tabla donde se guarda la relacion
    etiquetas: Mapped[list["Etiqueta"]] = relationship(
        secondary=pregunta_etiqueta, back_populates="preguntas"
    )


class Etiqueta(Base):
    __tablename__ = "etiqueta"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column()

    preguntas: Mapped[list[Pregunta]] = relationship(
        secondary=pregunta_etiqueta, back_populates="etiquetas"
    )


Base.metadata.create_all(engine)

db = SessionLocal()


# --- C: CREAR ---
def crear_pregunta(texto):
    pregunta = Pregunta(texto=texto)
    db.add(pregunta)
    db.commit()
    print(f"Pregunta agregada con éxito.")
    return pregunta.id


def crear_etiqueta(nombre):
    etiqueta = Etiqueta(nombre=nombre)
    db.add(etiqueta)
    db.commit()
    print(f"Etiqueta agregada con éxito.")
    return etiqueta.id


def agregar_etiqueta(pregunta_id, etiqueta_id):
    # En M2M no se edita la FK: se agrega el objeto a la lista
    pregunta = db.get(Pregunta, pregunta_id)
    etiqueta = db.get(Etiqueta, etiqueta_id)
    if pregunta is None or etiqueta is None:
        print("No se pudo agregar la etiqueta (ids inexistentes).")
        return
    if etiqueta not in pregunta.etiquetas:
        pregunta.etiquetas.append(etiqueta)
        db.commit()
        print(f"Etiqueta '{etiqueta.nombre}' agregada a la pregunta #{pregunta_id}.")


# --- R: LEER ---
def leer_preguntas():
    preguntas = db.scalars(select(Pregunta)).all()
    print("\n--- Lista de Preguntas (con sus etiquetas) ---")
    for p in preguntas:
        nombres = ", ".join(e.nombre for e in p.etiquetas) or "(sin etiquetas)"
        print(f"#{p.id} {p.texto} | Etiquetas: {nombres}")
    print("--------------------------------------------\n")


def leer_preguntas_de_etiqueta(etiqueta_id):
    # El lado inverso de la relacion
    etiqueta = db.get(Etiqueta, etiqueta_id)
    if etiqueta is None:
        print(f"No existe una etiqueta con ID {etiqueta_id}.")
        return
    print(f"\n--- Preguntas con la etiqueta '{etiqueta.nombre}' ---")
    for p in etiqueta.preguntas:
        print(f"#{p.id} {p.texto}")
    print("---------------------------------------------\n")


# --- U: ACTUALIZAR ---
def actualizar_etiqueta(etiqueta_id, nuevo_nombre):
    etiqueta = db.get(Etiqueta, etiqueta_id)
    if etiqueta is None:
        print(f"No existe una etiqueta con ID {etiqueta_id}.")
        return
    etiqueta.nombre = nuevo_nombre
    db.commit()
    print(f"Etiqueta con ID {etiqueta_id} actualizada.")


def quitar_etiqueta(pregunta_id, etiqueta_id):
    pregunta = db.get(Pregunta, pregunta_id)
    etiqueta = db.get(Etiqueta, etiqueta_id)
    if pregunta is None or etiqueta is None:
        print("No se pudo quitar la etiqueta (ids inexistentes).")
        return
    pregunta.etiquetas.remove(etiqueta)
    db.commit()
    print(f"Etiqueta '{etiqueta.nombre}' quitada de la pregunta #{pregunta_id}.")


# --- D: ELIMINAR ---
def eliminar_pregunta(pregunta_id):
    pregunta = db.get(Pregunta, pregunta_id)
    if pregunta is None:
        print(f"No existe una pregunta con ID {pregunta_id}.")
        return
    db.delete(pregunta)
    db.commit()
    print(f"Pregunta #{pregunta_id} eliminada (y sus vinculos con etiquetas).")


def eliminar_etiqueta(etiqueta_id):
    db.delete(db.get(Etiqueta, etiqueta_id))
    db.commit()
    print(f"Etiqueta con ID {etiqueta_id} eliminada (y sus vinculos).")


# --- Cerrar la sesion al terminar ---
def cerrar_db():
    db.close()
    print("Conexion cerrada.")
