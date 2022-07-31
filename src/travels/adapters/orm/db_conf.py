import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine,
)
from travels.conf import conf

db_path = os.path.join(conf.PARENT_BASE_DIR, "database.db")
def get_sql_session() -> object:
    return sessionmaker (
        bind=create_engine(f"sqlite:///{db_path}")
    )