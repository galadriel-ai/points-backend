from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

import settings
from points import api_logger
from points.routers import main_router
from points.routers import routing_utils
from points.service.exception_handlers.exception_handlers import (
    custom_exception_handler,
)
from points.service.middleware.main_middleware import MainMiddleware
from points.service.middleware.request_enrichment_middleware import (
    RequestEnrichmentMiddleware,
)
from points.service.monitoring.prometheus_metrics_endpoint import metrics
from points.service.monitoring.prometheus_middleware import PrometheusMiddleware

logger = api_logger.get()

app = FastAPI()

app.include_router(
    main_router.router,
)

API_TITLE = "Points API"
API_DESCRIPTION = "Points API version 1.0.0"
API_VERSION = "0.1"


class ApiInfo(BaseModel):
    title: str
    description: str
    version: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": API_TITLE,
                "description": API_DESCRIPTION,
                "version": API_VERSION,
            }
        }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
        servers=_get_servers(),
    )
    openapi_schema["info"]["contact"] = {"name": "", "email": ""}
    openapi_schema["info"]["x-logo"] = {"url": ""}
    openapi_schema["x-readme"] = {
        "samples-languages": ["curl", "node", "javascript", "python"]
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def _get_servers():
    servers = []
    if settings.is_production():
        servers.append({"url": "https://points.galadriel.com/"})
    else:
        base_url = settings.API_BASE_URL
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        servers.append({"url": f"{base_url}:{settings.API_PORT}"})
    return servers


app.openapi = custom_openapi

# order of middleware matters! first middleware called is the last one added
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MainMiddleware)
app.add_middleware(RequestEnrichmentMiddleware)
app.add_middleware(PrometheusMiddleware, filter_unhandled_paths=True)

# exception handlers run AFTER the middlewares!
# Handles API error responses
app.add_exception_handler(Exception, custom_exception_handler)


# Overrides FastAPI error responses, eg: authorization, not found
# app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
# Overrides default Pydantic request validation errors
# app.add_exception_handler(RequestValidationError, validation_exception_handler)


def get_api_info() -> ApiInfo:
    return ApiInfo(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)


@app.get(
    "/",
    summary="Returns API information",
    description="Returns API information",
    response_description="API information with title, description and version.",
    response_model=ApiInfo,
)
def root():
    return routing_utils.to_json_response(get_api_info().dict())


app.add_route("/metrics", metrics)

metrics_app_counter = 0


@app.get("/metrics-app", response_class=PlainTextResponse, include_in_schema=False)
def metrics_app():
    global metrics_app_counter
    result = ""
    result += (
        '\nmetrics-app-called '
        + str(metrics_app_counter)
    )
    metrics_app_counter += 1
    return result
