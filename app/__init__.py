from fastapi import FastAPI
from .database import create_db, SessionLocal
from .routes.auth import router as auth_router
from .routes.categories import router as categories_router
from .routes.products import router as products_router
from .routes.orders import router as orders_router
from .routes.inventory import router as inventory_router
from .routes.supplier import router as supplier_router
from .middlewares import CustomMiddleware
from .config import DATABASE_URL
from databases import Database

# Initialize database connection
database = Database(DATABASE_URL)

def create_app() -> FastAPI:
    app = FastAPI()

    # Include routers
    app.include_router(auth_router, prefix="/auth", tags=["users"])
    app.include_router(categories_router, prefix="/categories", tags=["categories"])
    app.include_router(products_router, prefix="/products", tags=["products"])
    app.include_router(orders_router, prefix="/orders", tags=["orders"])
    app.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
    app.include_router(supplier_router, prefix="/supplier", tags=["supplier"])

    # Add custom middleware
    app.add_middleware(CustomMiddleware)

    @app.on_event("startup")
    async def startup_event():
        await database.connect()
        create_db()

    @app.on_event("shutdown")
    async def shutdown_event():
        await database.disconnect()

    return app

app = create_app()
