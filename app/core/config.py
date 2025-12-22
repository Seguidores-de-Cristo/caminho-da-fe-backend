import os
import json
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
	"DATABASE_URL",
	"mysql+pymysql://caminho_user:caminho_password@127.0.0.1:3306/caminho_db",
)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-to-a-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# CORS configuration
# Set `CORS_ORIGINS` as a JSON array (e.g. '["https://example.com"]') or a
# comma-separated list (e.g. 'https://a.com,https://b.com'). Use '*' to allow all origins.
_cors_raw = os.getenv("CORS_ORIGINS", "")
if _cors_raw:
	try:
		parsed = json.loads(_cors_raw)
		if isinstance(parsed, list):
			CORS_ORIGINS = parsed
		else:
			CORS_ORIGINS = [str(parsed)]
	except Exception:
		# fallback: treat as comma-separated list
		CORS_ORIGINS = [o.strip() for o in _cors_raw.split(",") if o.strip()]
else:
	CORS_ORIGINS = []

# Allow using '*' as a single token to allow all origins
if len(CORS_ORIGINS) == 1 and CORS_ORIGINS[0] == "*":
	CORS_ORIGINS = ["*"]