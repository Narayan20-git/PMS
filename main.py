from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import property_routes

app = FastAPI(title="Property Management System App")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(property_routes.router)


@app.get("/")
def root():
    return {"message": "Property Management System App is running"}
