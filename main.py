from fastapi import FastAPI
#from routes import user_routes

app = FastAPI(title="Simple FastAPI App")

# Register routers
# app.include_router(health_routes.router)
# app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI app!"}
