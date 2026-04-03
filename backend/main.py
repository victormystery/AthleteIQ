"""
Career Recommender API - Main Entry Point
FastAPI backend with MVC architecture for sports career recommendations

Run with: uvicorn main:app --reload
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import configuration and utilities
from app.config.settings import get_settings
from app.utils.logger import setup_logging
from app.utils.exceptions import register_exception_handlers

# Import routers
from app.routes.auth_routes import router as auth_router
from app.routes.profile_routes import router as profile_router
from app.routes.career_routes_v2 import router as career_router_v2
from app.routes.questionnaire_routes import router as questionnaire_router
from app.routes.feedback_routes import router as feedback_router
from app.routes.progress_routes import router as progress_router
from app.routes.roadmap_routes import router as roadmap_router
from app.routes.feedback_loop_routes import router as feedback_loop_router

# Setup logging
settings = get_settings()
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Application factory pattern for creating FastAPI app instance
    """
    settings = get_settings()
    app = FastAPI(
        title=settings.APP_NAME,
        description="AI-Powered Sports Career Pathway Recommendation System",
        version=settings.VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Include routers
    app.include_router(auth_router)  # Authentication
    app.include_router(profile_router)  # Profile management
    app.include_router(career_router_v2)  # Career recommendations (database-backed)
    app.include_router(questionnaire_router)  # Questionnaire management
    app.include_router(feedback_router)  # Feedback management
    app.include_router(progress_router)  # Progress tracking
    app.include_router(roadmap_router)  # Personalized development roadmaps
    app.include_router(feedback_loop_router)  # Continuous improvement feedback loop

    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        if settings.ENVIRONMENT.lower() in {"production", "prod"}:
            settings.validate_secrets()
        logger.info("="*60)
        logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
        logger.info(f"Environment: {settings.ENVIRONMENT}")
        logger.info(f"Model Path: {settings.MODEL_PATH}")
        logger.info(f"Database: {settings.DATABASE_URL}")
        logger.info("="*60)
        
        # Initialize database
        from app.database.session import init_db
        from app.services.database_service import init_database_data
        try:
            logger.info("Initializing database...")
            init_db()
            logger.info("✓ Database tables created")
            
            # Seed initial data (career pathways)
            logger.info("Seeding initial data...")
            from app.database.session import SessionLocal
            db = SessionLocal()
            try:
                init_database_data(db)
                logger.info("✓ Database seeded with career pathways")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"✗ Database initialization failed: {str(e)}")
        
        # Pre-load ML model
        from app.services.ml_service import ml_service
        try:
            if ml_service.model is not None:
                logger.info("✓ ML Model loaded successfully")
            else:
                logger.warning("⚠ ML Model not loaded")
        except Exception as e:
            logger.error(f"✗ Failed to load ML model: {str(e)}")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("="*60)
        logger.info(f"Shutting down {settings.APP_NAME}")
        logger.info("="*60)

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": f"{settings.APP_NAME}",
            "version": settings.VERSION,
            "status": "healthy",
            "docs": "/api/docs"
        }

    @app.get("/health", tags=["Health"])
    async def health_check():
        from app.services.ml_service import ml_service
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.VERSION,
            "model_loaded": ml_service.is_model_loaded(),
            "environment": settings.ENVIRONMENT
        }

    return app


# Create FastAPI application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
