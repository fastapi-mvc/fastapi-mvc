# Configuration

This application provides flexibility of configuration. 
All significant settings are defined by the environment variables, each with the default value. 
Moreover, package CLI allows overriding core ones: host, port, workers. 
You can modify all other available configuration settings in the gunicorn.conf.py file.

Priority of overriding configuration:

1. cli
2. environment variables
3. gunicorn.conf.py

All application configuration is available in `demo_project.config` submodule.

### Environment variables

#### Application configuration

| Key                         | Default                                                             | Description                                                    |
|-----------------------------|---------------------------------------------------------------------|----------------------------------------------------------------|
| FASTAPI_HOST                | `"127.0.0.1"`                                                       | FastAPI host to bind.                                          |
| FASTAPI_PORT                | `"8000"`                                                            | FastAPI port to bind.                                          |
| FASTAPI_WORKERS             | `"2"`                                                               | Number of gunicorn workers (uvicorn.workers.UvicornWorker)     |
| FASTAPI_DEBUG               | `"True"`                                                            | FastAPI logging level. You should disable this for production. |
| FASTAPI_PROJECT_NAME        | `"fastapi-mvc-example"`                                             | FastAPI project name.                                          |
| FASTAPI_VERSION             | `"0.4.0"`                                                           | Application version.                                           |
| FASTAPI_DOCS_URL            | `"/"`                                                               | Path where swagger ui will be served at.                       |
| FASTAPI_USE_REDIS           | `"False"`                                                           | Whether or not to use Redis.                                   |
| FASTAPI_GUNICORN_LOG_LEVEL  | `"info"`                                                            | The granularity of gunicorn log output                         |
| FASTAPI_GUNICORN_LOG_FORMAT | `'%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'`     | Gunicorn log format                                            |

#### Redis configuration

| Key                        | Default       | Description                               |
|----------------------------|---------------|-------------------------------------------|
| FASTAPI_REDIS_HOTS         | `"127.0.0.1"` | Redis host.                               |
| FASTAPI_REDIS_PORT         | `"6379"`      | Redis port.                               |
| FASTAPI_REDIS_USERNAME     | `""`          | Redis username.                           |
| FASTAPI_REDIS_PASSWORD     | `""`          | Redis password.                           |
| FASTAPI_REDIS_USE_SENTINEL | `"False"`     | If provided Redis config is for Sentinel. |

### gunicorn.conf.py

1. Source: `.config/gunicorn.conf.py`
2. [Gunicorn configuration file documentation](https://docs.gunicorn.org/en/latest/settings.html)

### Routes definition

Endpoints are defined in `demo_project.config.router`. Just simply import your controller and include it to FastAPI router:

```python
from fastapi import APIRouter
from demo_project.app.controllers.api.v1 import ready

router = APIRouter(
    prefix="/api"
)

router.include_router(ready.router, tags=["ready"])
```
