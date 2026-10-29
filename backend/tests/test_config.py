from app.config import Settings


# Build Settings with fake values so the test does not need real secrets
def make_settings(frontend_origin: str) -> Settings:
    return Settings(
        supabase_url="https://example.supabase.co",
        supabase_service_role_key="test-key",
        database_url="postgresql+psycopg://user:pass@localhost/db",
        frontend_origin=frontend_origin,
    )


# A comma-separated origin list becomes a clean list, spaces removed
def test_frontend_origins_splits_and_trims():
    settings = make_settings("https://app.example.com, http://localhost:5173")
    assert settings.frontend_origins == [
        "https://app.example.com",
        "http://localhost:5173",
    ]


# A single origin still works as a one-item list
def test_frontend_origins_single_origin():
    settings = make_settings("http://localhost:5173")
    assert settings.frontend_origins == ["http://localhost:5173"]


# Empty pieces, and pieces that are only a slash, are dropped
def test_frontend_origins_ignores_empty_entries():
    settings = make_settings("https://app.example.com,, /, http://localhost:5173,")
    assert settings.frontend_origins == [
        "https://app.example.com",
        "http://localhost:5173",
    ]


# A trailing slash is removed so the origin matches what browsers send
def test_frontend_origins_strips_trailing_slash():
    settings = make_settings("https://app.example.com/, http://localhost:5173/")
    assert settings.frontend_origins == [
        "https://app.example.com",
        "http://localhost:5173",
    ]
