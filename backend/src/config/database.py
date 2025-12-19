from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    database_url: str = "postgresql://textbook_user:textbook_password@localhost:5432/textbook_db"

    class Config:
        env_file = ".env"


# Create settings instance
settings = DatabaseSettings()

# Create engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verify connections are alive before using them
    pool_recycle=300,    # Recycle connections after 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()