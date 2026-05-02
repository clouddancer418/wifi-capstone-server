from fastapi import FastAPI
from database import Base, engine
from routers import measurement
from routers import dashboard
from routers import feedback
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(measurement.router)
app.include_router(dashboard.router, prefix="/dashboard")
app.include_router(feedback.router, prefix="/feedback")

@app.get("/")
def root():
    return {"message": "API 실행 중"}

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/dashboard.html")
def serve_dashboard():
    return FileResponse("dashboard.html")