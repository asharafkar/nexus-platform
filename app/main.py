import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.api.router import api_router
from app.core.config import Settings, get_settings
from app.database.engine import create_database_engine

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        logger.info(
            "Starting %s in %s mode",
            app_settings.service_name,
            app_settings.environment,
        )

        application.state.settings = app_settings

        database_engine: AsyncEngine | None = None

        try:
            application.state.db_engine = None
            application.state.db_session_factory = None

            if app_settings.database_url:
                database_engine = create_database_engine(
                    app_settings.database_url,
                )

                application.state.db_engine = database_engine
                application.state.db_session_factory = async_sessionmaker(
                    database_engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                )

                logger.info("Database engine initialized")

            yield

        finally:
            if database_engine is not None:
                await database_engine.dispose()
                logger.info("Database engine disposed")

            logger.info("Shutting down %s", app_settings.service_name)

    application = FastAPI(
        title=app_settings.service_name,
        description=app_settings.service_description,
        version=app_settings.app_version,
        debug=app_settings.debug,
        lifespan=lifespan,
    )

    application.include_router(api_router)

    return application


app = create_app()