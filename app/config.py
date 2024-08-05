import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file if available

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 14400))

TORTOISE_ORM = {
    "connections": {
        # Your database connection details go here
        "default": "sqlite:///db.sqlite3",  # Example for SQLite
        # For other databases, adjust the connection string accordingly
    },
    "apps": {
        "models": {
            "models": [
                "app.models.Category",
                "app.models.Product",
                "app.models.Inventory",
                "app.models.Order",
                "app.models.Supplier",
                "app.models.User",
            ],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "UTC",
}

async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()