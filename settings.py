import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

ENVIRONMENT = os.getenv("PLATFORM_ENVIRONMENT", "local")

APPLICATION_NAME = "POINTS"
API_PORT = int(os.getenv("API_PORT", 5000))
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost/")
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

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
# This URL needs to be set in the discord app ouath2 settings! AUTH DOES NOT WORK with any url
DISCORD_AUTH_CALLBACK = os.getenv("DISCORD_AUTH_CALLBACK", "http://localhost:5000/v1/auth/discord/callback")

CHAIN_ID = os.getenv("CHAIN_ID", 1)

GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_PATH", "sidekik-ai-points-backend.json")
GOOGLE_BUCKET_NAME = os.getenv("GOOGLE_BUCKET_NAME", "galadriel-user-assets")

def is_production() -> bool:
    return ENVIRONMENT == "production"


def get_server_url() -> str:
    if is_production():
        return "https://api.points.galadriel.com"
    base_url = API_BASE_URL
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    return f"{base_url}:{API_PORT}"


def get_domain() -> str:
    if is_production():
        return "galadriel.com"
    return "localhost"


if not is_production():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
