import logging
import re

from app.auth import configure_auth
from app.auth.remote import RemoteAuth
from fastapi import FastAPI


VERSION = (1, 0, 0)
logger = logging.getLogger(__name__)


def get_version():
    return '.'.join(map(str, VERSION))


def get_app(
    debug: bool = False,
    production: bool = True,
    app_prefix: str = '',
    auth_header: str = 'X-Remote-User'
) -> FastAPI:
    from app.routers import games, health, me, names, users
    from fastapi import FastAPI, Request, status
    
    app = FastAPI(
        title='Prenoms',
        version=get_version(),
        debug=debug,
        production=production,
        root_path=app_prefix,
    )

    configure_auth(RemoteAuth, header_name=auth_header)

    logger.debug('Creating application with following parameters: production=%s ; debug=%s ; app_prefix=%s', production, debug, app_prefix)

    if production:
        access_logger = logging.getLogger(__name__)
        re_status = re.compile('^HTTP_[0-9]+_(.+)$')
        status_strings = { 
            v: re_status.match(k).group(1).replace('_', ' ') for k, v in status.__dict__.items() if k.startswith('HTTP_')
        }

        @app.middleware('http')
        async def access_log(request: Request, call_next):
            response = await call_next(request)

            access_logger.info(
                '%s - "%s %s %s" %d %s',
                request.headers.get('x-forwarded-for', request.client.host),
                request.method,
                request.url,
                'HTTP/{}'.format(request.scope['http_version']),
                response.status_code,
                status_strings.get(response.status_code, '')
            )

            return response

    app.include_router(games.router, prefix='/games')
    app.include_router(health.router, prefix='/health')
    app.include_router(me.router, prefix='/me')
    app.include_router(names.router, prefix='/names')
    app.include_router(users.router, prefix='/users')

    return app
