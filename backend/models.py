from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String, index=True)


class Repositories(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    name = Column(String, index=True)


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    metric1 = Column(String, index=True)
    metric2 = Column(String, index=True)
    created_at = Column(String, index=True)


class Dummy(Base):
    __tablename__ = "dummy"

    id = Column(Integer, primary_key=True, index=True)
    test = Column(String, index=True)
