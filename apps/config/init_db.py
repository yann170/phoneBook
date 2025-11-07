
from .database import engine, SQLModel


SQLModel.metadata.create_all(engine)