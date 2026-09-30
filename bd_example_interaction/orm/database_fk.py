from pathlib import Path

from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)

"""Inicializacion de la Base de datos (DB) con SQLAlchemy (ORM) - RELACION FK (1:N)"""
# La DB se guarda siempre en la carpeta de este archivo, sin importar desde donde se ejecute
BASE_DIR = Path(__file__).resolve().parent

# Un QUIZ tiene MUCHAS preguntas (1:N) -> la FK vive en la tabla hija (question)
engine = create_engine(f"sqlite:///{BASE_DIR / 'db_fk.sqlite3'}")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# Lado "1" de la relacion
class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column()

    # back_populates conecta los dos lados de la misma relacion
    preguntas: Mapped[list["Question"]] = relationship(
        back_populates="quiz",
        cascade="all, delete-orphan",  # al borrar el quiz se borran sus preguntas
    )


# Lado "N" de la relacion
class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    texto: Mapped[str] = mapped_column()
    correcta: Mapped[int] = mapped_column()

    # La FK: guarda el id del quiz al que pertenece cada pregunta
    quiz_id: Mapped[int | None] = mapped_column(ForeignKey("quiz.id"))

    quiz: Mapped["Quiz | None"] = relationship(back_populates="preguntas")


Base.metadata.create_all(engine)

db = SessionLocal()


# --- C: CREAR ---
def crear_quiz(titulo):
    quiz = Quiz(titulo=titulo)
    db.add(quiz)
    db.commit()
    print(f"Quiz '{titulo}' agregado con éxito.")
    return quiz.id


def crear_pregunta(quiz_id, texto, correcta):
    if db.get(Quiz, quiz_id) is None:
        print(f"No existe un quiz con ID {quiz_id}.")
        return
    pregunta = Question(texto=texto, correcta=correcta, quiz_id=quiz_id)
    db.add(pregunta)
    db.commit()
    print(f"Pregunta agregada al quiz con ID {quiz_id}.")
    return pregunta.id


# --- R: LEER ---
def leer_quizzes():
    quizzes = db.scalars(select(Quiz)).all()
    print("\n--- Lista de Quizzes (con sus preguntas) ---")
    for quiz in quizzes:
        print(f"Quiz #{quiz.id}: {quiz.titulo}")
        for p in quiz.preguntas:
            print(f"   - #{p.id} {p.texto} | Correcta: {p.correcta}")
    print("------------------------------------------\n")


def leer_preguntas_de_quiz(quiz_id):
    # Consulta con filtro usando la FK
    preguntas = db.scalars(select(Question).where(Question.quiz_id == quiz_id)).all()
    print(f"\n--- Preguntas del quiz con ID {quiz_id} ---")
    for p in preguntas:
        print(f"#{p.id} {p.texto}")
    print("-------------------------------------\n")


# --- U: ACTUALIZAR ---
def actualizar_quiz(quiz_id, nuevo_titulo):
    quiz = db.get(Quiz, quiz_id)
    if quiz is None:
        print(f"No existe un quiz con ID {quiz_id}.")
        return
    quiz.titulo = nuevo_titulo
    db.commit()
    print(f"Quiz con ID {quiz_id} actualizado.")


def mover_pregunta(pregunta_id, nuevo_quiz_id):
    # Cambiar la FK: la pregunta pasa a pertenecer a otro quiz
    pregunta = db.get(Question, pregunta_id)
    if pregunta is None or db.get(Quiz, nuevo_quiz_id) is None:
        print("No se pudo mover la pregunta (ids inexistentes).")
        return
    pregunta.quiz_id = nuevo_quiz_id
    db.commit()
    print(f"Pregunta #{pregunta_id} movida al quiz con ID {nuevo_quiz_id}.")


# --- D: ELIMINAR ---
def eliminar_pregunta(pregunta_id):
    pregunta = db.get(Question, pregunta_id)
    if pregunta is None:
        print(f"No existe una pregunta con ID {pregunta_id}.")
        return
    db.delete(pregunta)
    db.commit()
    print(f"Pregunta #{pregunta_id} eliminada.")


def eliminar_quiz(quiz_id):
    # cascade="all, delete-orphan" -> se borran tambien sus preguntas
    quiz = db.get(Quiz, quiz_id)
    if quiz is None:
        print(f"No existe un quiz con ID {quiz_id}.")
        return
    db.delete(quiz)
    db.commit()
    print(f"Quiz con ID {quiz_id} eliminado (y sus preguntas).")


# --- Cerrar la sesion al terminar ---
def cerrar_db():
    db.close()
    print("Conexion cerrada.")
