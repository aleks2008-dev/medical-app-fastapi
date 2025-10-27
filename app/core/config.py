from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL settings
    database_url: str = "postgresql+asyncpg://admin:password@localhost:5432/medical_db"
    
    # App settings
    environment: str = "development"
    debug: bool = True
    
    # JWT settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email settings
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@medicalapp.com"
    
    # Redis settings
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        extra="ignore"
        case_sensitive = False

settings = Settings()