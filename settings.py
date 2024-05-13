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

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "passw0rd")
DB_DATABASE = os.getenv("DB_DATABASE", "points")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)

PROMETHEUS_MULTIPROC_DIR = os.getenv("PROMETHEUS_MULTIPROC_DIR", None)

WEB3_RPC_URL = os.getenv("WEB3_RPC_URL", "https://devnet.galadriel.com")
EXPLORER_API_BASE_URL = "https://explorer.galadriel.com/api/v2/"

FAUCET_ADDRESS = os.getenv("FAUCET_ADDRESS", "0x2AfAcDdd5218943CfB52D4B43205bB96dD87A165")

GALADRIEL_TWITTER_USER_ID = os.getenv("GALADRIEL_TWITTER_USER_ID", "1384448028774383616")

TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
# This URL needs to be set in the twitter developer settings! AUTH DOES NOT WORK with any url
TWITTER_AUTH_CALLBACK = os.getenv("TWITTER_AUTH_CALLBACK", "http://localhost:5000/v1/auth/x/callback")
# Randomly generated secret key eg `openssl rand -hex 32`
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
# Where API redirects if user is logged in
FRONTEND_AUTH_CALLBACK_URL = os.getenv("FRONTEND_AUTH_CALLBACK_URL", "http://localhost:3000/auth/callback")


def is_production():
    return ENVIRONMENT == "production"


if not is_production():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
