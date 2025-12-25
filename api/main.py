from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Based Automated Content Marketing Optimizer API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "TrendForgeAI API",
        "version": settings.VERSION,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Import and include routers
from .routers import content, sentiment, metrics, ab_testing
app.include_router(content.router, prefix=f"{settings.API_V1_PREFIX}/content", tags=["content"])
app.include_router(sentiment.router, prefix=f"{settings.API_V1_PREFIX}/sentiment", tags=["sentiment"])
app.include_router(metrics.router, prefix=f"{settings.API_V1_PREFIX}/metrics", tags=["metrics"])
app.include_router(ab_testing.router, prefix=f"{settings.API_V1_PREFIX}/ab", tags=["ab_testing"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
