from fastapi import FastAPI
from app.database import engine, Base
from app.routes import users, problems, submissions

# creates all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CodeVerdict")

# register routes
app.include_router(users.router, prefix="/auth", tags=["Auth"])
app.include_router(problems.router, prefix="/problems", tags=["Problems"])
app.include_router(submissions.router, prefix="/submissions", tags=["Submissions"])

@app.get("/")
def root():
    return {"message": "Welcome to CodeVerdict!"}