from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from judge.runner import run_code
import time

router = APIRouter()


@router.post("/", response_model=schemas.SubmissionResponse)
def submit_code(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    # check problem exists
    problem = db.query(models.Problem).filter(models.Problem.id == submission.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # get test cases
    test_cases = db.query(models.TestCase).filter(models.TestCase.problem_id == submission.problem_id).all()
    if not test_cases:
        raise HTTPException(status_code=400, detail="No test cases found for this problem")

    # run judge
    verdict = "AC"
    total_runtime = 0

    for tc in test_cases:
        start = time.time()
        result = run_code(submission.code, tc.input, problem.time_limit)
        elapsed = int((time.time() - start) * 1000)  # milliseconds
        total_runtime += elapsed

        if result["verdict"] == "TLE":
            verdict = "TLE"
            break

        if result["verdict"] == "RE":
            verdict = "RE"
            print("RE ERROR:", result["output"])  # add this line
            break

        if result["output"] != tc.expected_output.strip():
            verdict = "WA"
            break

    # save submission
    new_submission = models.Submission(
        user_id=1,  # hardcoded for now, will fix with auth later
        problem_id=submission.problem_id,
        code=submission.code,
        verdict=verdict,
        runtime=total_runtime
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission


@router.get("/{submission_id}", response_model=schemas.SubmissionResponse)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


@router.get("/me/all", response_model=list[schemas.SubmissionResponse])
def my_submissions(db: Session = Depends(get_db)):
    return db.query(models.Submission).filter(models.Submission.user_id == 1).all()