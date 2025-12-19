from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database settings
    database_url: str = "postgresql://textbook_user:textbook_password@localhost:5432/textbook_db"

    # Qdrant settings
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = "textbook_api_key"

    # OpenAI settings
    openai_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()