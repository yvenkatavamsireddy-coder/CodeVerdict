# CodeVerdict ⚖️

## Live Demo
🔗 https://codeverdict.onrender.com/docs

An online code judging platform — submit code, get a verdict. Built with FastAPI, Docker, and SQLite.

---

## What It Does

CodeVerdict is a backend system that judges code submissions against test cases, similar to how CodeForces, LeetCode or HackerRank work under the hood.

- Users register and log in
- Admins create problems and add test cases
- Users submit Python code solutions via API
- Code runs inside an isolated Docker container
- Verdict is returned: **AC / WA / TLE / RE**

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | SQLite + SQLAlchemy |
| Auth | JWT (JSON Web Tokens) |
| Judge Engine | Docker + subprocess |
| Password Hashing | bcrypt + passlib |

---

## Project Structure

```
CodeVerdict/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── database.py      # DB connection and session
│   ├── models.py        # SQLAlchemy table models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # JWT auth and dependencies
│   └── routes/
│       ├── users.py     # Register and login
│       ├── problems.py  # Problem CRUD
│       └── submissions.py # Submit code, get verdict
├── judge/
│   └── runner.py        # Docker-based code execution engine
└── requirements.txt
```

---

## How the Judge Works

```
User submits code via POST /submissions/
        ↓
Fetch test cases for the problem from DB
        ↓
Write code to a unique temp file
        ↓
Run inside Docker container with:
    - Memory limit: 128MB
    - CPU limit: 0.5 cores
    - Time limit: configurable per problem
    - Network: disabled
        ↓
Compare output against expected output
        ↓
Return verdict and save to DB
```

---

## Verdicts

| Verdict | Meaning |
|---|---|
| **AC** | Accepted — all test cases passed |
| **WA** | Wrong Answer — output didn't match |
| **TLE** | Time Limit Exceeded — ran too long |
| **RE** | Runtime Error — code crashed |

---

## API Routes

### Auth
| Method | Route | Access | Description |
|---|---|---|---|
| POST | `/auth/register` | Public | Register a new user |
| POST | `/auth/login` | Public | Login and get JWT token |

### Problems
| Method | Route | Access | Description |
|---|---|---|---|
| GET | `/problems/` | Public | List all problems |
| GET | `/problems/{id}` | Public | Get a single problem |
| POST | `/problems/` | Admin only | Create a problem |
| POST | `/problems/{id}/testcases` | Admin only | Add test cases |

### Submissions
| Method | Route | Access | Description |
|---|---|---|---|
| POST | `/submissions/` | Logged in | Submit code |
| GET | `/submissions/{id}` | Logged in | Get submission by ID |
| GET | `/submissions/me/all` | Logged in | Get all my submissions |

---

## Setup and Run Locally

### Prerequisites
- Python 3.11+
- Docker Desktop running

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/CodeVerdict.git
cd CodeVerdict

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

---

## Testing the API

### 1. Register
```bash
POST /auth/register
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

### 2. Login
```bash
POST /auth/login
{
  "username": "john",
  "password": "secret123"
}
```

Copy the `access_token` from the response.

### 3. Authorize
In `/docs`, click the **Authorize** button and paste your token.

### 4. Submit Code
```bash
POST /submissions/
{
  "problem_id": 1,
  "code": "print('[0,1]')"
}
```

---

## Security

- User code runs inside an isolated Docker container
- Network access is disabled inside the container
- Memory and CPU are strictly limited
- Each submission uses a unique temp file to prevent conflicts
- Passwords are hashed with bcrypt
- Routes are protected with JWT authentication

---

## Author

Built by Venkat as an internship portfolio project.
