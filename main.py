from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import user
from database.connection import DBConnection
from database.database import (MONGO_CONNECTION_URL, DATABASE_NAME)


app = FastAPI(
    # docs_url=None, # Disable docs (Swagger UI)
    # redoc_url=None, # Disable redoc
    title="TechBurst",
    description="API for TechBurst",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    # openapi_tags=tags_metadata
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server",
        },
        {
            "url": "https://techburst.render.com",
            "description": "Production server"
        }
    ]
)

# Set the allowed origins, methods, headers, and other CORS options
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user", tags=["User"])

# Create an instance of DBConnection
db_connection = DBConnection(MONGO_CONNECTION_URL, DATABASE_NAME)

@app.on_event("startup")
async def startup_event():
    """
    Perform startup tasks, such as connecting to the database or initializing services
    """
    db_connection.connect()
    print("\nS E R V E R   S T A R T I N G . . . . . . . . . .\n")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Perform cleanup tasks, such as closing database connections or releasing resources
    """
    db_connection.disconnect()
    print("\nS E R V E R   S H U T D O W N . . . . . . . . . .\n")


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
