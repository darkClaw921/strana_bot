from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    INSTAGRAM_GRAPH_VERSION: str = 'v21.0'
    INSTAGRAM_ACCESS_TOKEN: str
    INSTAGRAM_PAGE_ID: str
    WEBHOOK_VERIFY_TOKEN: str
    
    @property
    def GRAPH_API_URL(self) -> str:
        return f'https://graph.facebook.com/{self.INSTAGRAM_GRAPH_VERSION}'
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
