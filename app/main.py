from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routes import users, problems, submissions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CodeVerdict")

# register routes
app.include_router(users.router, prefix="/auth", tags=["Auth"])
app.include_router(problems.router, prefix="/problems", tags=["Problems"])
app.include_router(submissions.router, prefix="/submissions", tags=["Submissions"])

# serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")