from src.db_connector import engine
from src.models import *

Base.metadata.create_all(engine)
