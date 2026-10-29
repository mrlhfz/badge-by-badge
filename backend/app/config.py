from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str
    supabase_service_role_key: str
    database_url: str
    frontend_origin: str

    @property
    def frontend_origins(self) -> list[str]:
        # Split "https://a.com, http://localhost:5173/" into a clean list of origins
        # Clean each piece first, then drop the ones that are empty after cleaning
        cleaned = (part.strip().rstrip("/") for part in self.frontend_origin.split(","))
        return [origin for origin in cleaned if origin]


settings = Settings()
