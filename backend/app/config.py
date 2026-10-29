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
        return [
            origin.strip().rstrip("/")
            for origin in self.frontend_origin.split(",")
            if origin.strip()
        ]


settings = Settings()
