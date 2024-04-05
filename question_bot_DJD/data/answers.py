import sqlalchemy

from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    __tablename__ = "answers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    applic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("applications.id"))
