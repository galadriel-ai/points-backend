import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

ENVIRONMENT = os.getenv("PLATFORM_ENVIRONMENT", "local")

APPLICATION_NAME = "POINTS"
API_PORT = int(os.getenv("API_PORT", 5000))
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1/")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
LOG_FILE_PATH = "logs/logs.log"

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'passw0rd')
DB_DATABASE = os.getenv('DB_DATABASE', 'points')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', 5432)

PROMETHEUS_MULTIPROC_DIR = os.getenv("PROMETHEUS_MULTIPROC_DIR", None)

EXPLORER_API_BASE_URL = "https://explorer.galadriel.com/api/v2/"


def is_production():
    return ENVIRONMENT == "production"
