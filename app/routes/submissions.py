from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user
from judge.runner import run_code
import time

router = APIRouter()


@router.post("/", response_model=schemas.SubmissionResponse)
def submit_code(
    submission: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
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
        elapsed = int((time.time() - start) * 1000)
        total_runtime += elapsed

        if result["verdict"] == "TLE":
            verdict = "TLE"
            break

        if result["verdict"] == "RE":
            verdict = "RE"
            break

        if result["output"] != tc.expected_output.strip():
            verdict = "WA"
            break

    # save submission with actual user id
    new_submission = models.Submission(
        user_id=current_user.id,
        problem_id=submission.problem_id,
        code=submission.code,
        verdict=verdict,
        runtime=total_runtime
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission


@router.get("/me/all", response_model=list[schemas.SubmissionResponse])
def my_submissions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Submission).filter(models.Submission.user_id == current_user.id).all()


@router.get("/{submission_id}", response_model=schemas.SubmissionResponse)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission