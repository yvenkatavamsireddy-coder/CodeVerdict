from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.ProblemResponse])
def get_problems(db: Session = Depends(get_db)):
    return db.query(models.Problem).all()


@router.get("/{problem_id}", response_model=schemas.ProblemResponse)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.post("/", response_model=schemas.ProblemResponse)
def create_problem(problem: schemas.ProblemCreate, db: Session = Depends(get_db)):
    new_problem = models.Problem(
        title=problem.title,
        description=problem.description,
        difficulty=problem.difficulty,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem


@router.post("/{problem_id}/testcases")
def add_testcase(problem_id: int, testcase: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    new_tc = models.TestCase(
        problem_id=problem_id,
        input=testcase.input,
        expected_output=testcase.expected_output,
        is_hidden=testcase.is_hidden
    )
    db.add(new_tc)
    db.commit()
    db.refresh(new_tc)
    return {"message": "Test case added successfully"}