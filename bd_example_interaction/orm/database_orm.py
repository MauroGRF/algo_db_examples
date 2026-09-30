from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

"""Inicializacion de la Base de datos (DB) con SQLAlchemy (ORM)"""
# La DB se guarda siempre en la carpeta de este archivo, sin importar desde donde se ejecute
BASE_DIR = Path(__file__).resolve().parent

# Creando (Si no existe) el motor de conexion a la DB
engine = create_engine(f"sqlite:///{BASE_DIR / 'db_orm.sqlite3'}")
SessionLocal = sessionmaker(bind=engine)


# Base: clase de la que heredan todos los modelos
class Base(DeclarativeBase):
    pass


# Modelo: cada atributo mapea a una columna de la tabla
class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column()
    q1: Mapped[str] = mapped_column()
    q2: Mapped[str] = mapped_column()
    q3: Mapped[str] = mapped_column()
    q4: Mapped[str] = mapped_column()
    answer: Mapped[int] = mapped_column()


# Crea la tabla (si no existe) -> reemplaza al CREATE TABLE
Base.metadata.create_all(engine)

# Sesion abierta: equivalente a la conexion + cursor de sqlite3
db = SessionLocal()


# --- C: CREAR (Insertar registros) ---
def crear_pregunta(question, q1, q2, q3, q4, answer):
    pregunta = Question(question=question, q1=q1, q2=q2, q3=q3, q4=q4, answer=answer)
    db.add(pregunta)
    db.commit()
    print("Pregunta agregada con éxito.")
    return pregunta.id


# --- R: LEER (Consultar registros) ---
def leer_preguntas():
    preguntas = db.scalars(select(Question)).all()
    print("\n--- Lista de Preguntas ---")
    for p in preguntas:
        print(
            f"ID: {p.id} | Pregunta: {p.question} | "
            f"1) {p.q1} 2) {p.q2} 3) {p.q3} 4) {p.q4} | Correcta: {p.answer}"
        )
    print("-------------------------\n")


# --- U: ACTUALIZAR (Modificar registros) ---
def actualizar_pregunta(pregunta_id, nueva_question, nuevo_answer):
    pregunta = db.get(Question, pregunta_id)
    if pregunta is None:
        print(f"No existe una pregunta con ID {pregunta_id}.")
        return
    pregunta.question = nueva_question
    pregunta.answer = nuevo_answer
    db.commit()
    print(f"Pregunta con ID {pregunta_id} actualizada.")


# --- D: ELIMINAR (Borrar registros) ---
def eliminar_pregunta(pregunta_id):
    pregunta = db.get(Question, pregunta_id)
    if pregunta is None:
        print(f"No existe una pregunta con ID {pregunta_id}.")
        return
    db.delete(pregunta)
    db.commit()
    print(f"Pregunta con ID {pregunta_id} eliminada.")


# --- Cerrar la sesion al terminar ---
def cerrar_db():
    db.close()
    print("Conexion cerrada.")
