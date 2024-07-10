# module-specific constants
from src.config import settings
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES = 60

ACCESS_TOKEN_SECRET_KEY = settings.oauth_token_secret
ACCESS_TOKEN_ALGORITHM = "HS256"