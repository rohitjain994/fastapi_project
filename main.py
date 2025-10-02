from fastapi import FastAPI
from app.rate_limit import InMemoryRateLimiter
import uvicorn
from app.routers.items import router as items_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.exceptions import ResourceNotFoundException, resource_not_found_exception_handler

# Create FastAPI instance
app = FastAPI(
    title="Dummy FastAPI Project",
    description="A simple FastAPI project with CRUD operations",
    version="1.0.0"
)

app.add_exception_handler(ResourceNotFoundException, resource_not_found_exception_handler)
app.add_middleware(InMemoryRateLimiter, requests=60, window_seconds=60)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Dummy FastAPI Project!", "version": "1.0.0"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

app.include_router(items_router)
app.include_router(users_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
