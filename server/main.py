import logging
import os

from app import get_app


DEBUG = os.getenv('APP_DEBUG', 'false').lower() == 'true'
PRODUCTION = os.getenv('APP_ENV', 'production') == 'production'
PREFIX = os.getenv('APP_PREFIX', '')
AUTH_HEADER = os.getenv('AUTH_HEADER_NAME', 'X-Remote-User')

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO
)

app = get_app(
    debug=DEBUG,
    production=PRODUCTION,
    app_prefix=PREFIX,
    auth_header=AUTH_HEADER,
)
