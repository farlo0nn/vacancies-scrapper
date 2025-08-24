from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import PG_DBNAME, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER

Base = declarative_base()
engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
)
SessionLocal = sessionmaker(bind=engine)
