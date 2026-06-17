from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    backend_url: str = "http://localhost:8000"
    camera_source: str = "0"
    seat_config_path: str = "seat_config.example.json"
    yolo_model: str = "yolov8n.pt"
    confidence_threshold: float = 0.45
    occupied_frames_threshold: int = 5
    empty_frames_threshold: int = 10
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
