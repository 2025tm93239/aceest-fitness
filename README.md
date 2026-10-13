# ACEest Fitness & Gym

**CSI ZG514 / SEZG514 — Introduction to DevOps (Assignment 1)**.

Assignment Overview: Implementing Automated CI/CD Pipelines for ACEest Fitness & Gym
Objective - This assignment is designed to provide students with comprehensive, hands-on experience in modern DevOps methodologies. By executing this project, students will attain professional proficiency in Version Control (Git/GitHub), Containerization (Docker), and the orchestration of Continuous Integration and Continuous Delivery (CI/CD) pipelines using GitHub Actions and Jenkins.


ACEest is a Flask REST API for gym program management: training plans, calorie estimation, client profiles, and facility metrics. The project demonstrates version control, unit testing, Docker containerization, Jenkins BUILD quality gates, and GitHub Actions CI/CD.

**Git Repository:** https://github.com/2025tm93239/aceest-fitness

---

## Table of contents

- [Overview](#overview)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local setup and execution](#local-setup-and-execution)
- [API reference](#api-reference)
- [Running tests manually](#running-tests-manually)
- [Docker](#docker)
- [GitHub Actions (CI/CD)](#github-actions-cicd)
- [Jenkins (BUILD and quality gate)](#jenkins-build-and-quality-gate)

---

## Overview

| Layer | Technology |
|-------|------------|
| Application | Python 3.9, Flask 3 |
| Tests | Pytest |
| Container | Docker (`python:3.9-slim`, Gunicorn) |
| CI | GitHub Actions (`.github/workflows/main.yml`) |
| BUILD server | Jenkins (`Jenkinsfile`, Pipeline from SCM) |

The API logic is derived from the instructor-provided ACEest desktop scripts (`versions/`), refactored into a modular Flask service under `aceest/`.

---

## Project structure

```
aceest-fitness/
├── app.py                              # Flask application entry point
├── aceest/                             # REST API package
│   ├── __init__.py
│   ├── programs.py                     # Program catalog and gym metrics
│   ├── services.py                     # Business logic (calories, validation)
│   └── storage.py                      # In-memory client store
├── tests/
│   ├── conftest.py                     # Pytest fixtures and shared setup
│   ├── test_app.py                     # API integration tests
│   └── test_services.py                # Unit tests for services
├── versions/                           # Historical Tkinter baseline (Aceestver-*.py)
├── docs/
│   ├── JENKINS-SETUP.md                # Detailed Jenkins configuration guide
│   └── jenkins-docker-fix.sh           # Jenkins agent Docker permission helper
├── Screenshots and Video/              # Assignment evidence (CI/Jenkins logs, screenshots)
├── .github/
│   └── workflows/
│       └── main.yml                    # GitHub Actions CI/CD pipeline
├── Dockerfile                          # Container image (Gunicorn on port 5000)
├── .dockerignore                       # Build context exclusions (e.g. versions/, .venv)
├── Jenkinsfile                         # Jenkins Pipeline from SCM
├── requirements.txt                    # Python dependencies
├── runtime.txt                         # Python version pin (python-3.9.21)
├── pytest.ini                          # Pytest config (pythonpath, testpaths, addopts)
├── README.md
└── ACEest_Assignment1_Deliverables.docx
```

---

## Prerequisites

- **Python 3.9+** (course Linux VM: **3.9.21**)
- **Git**

Verify on the VM:

```bash
python3 --version   # expected: Python 3.9.21
```
- **Docker** (for container build/run and CI parity)
- **Jenkins LTS** (local or lab server) for Assignment Step 5

---

## Local setup and execution

### 1. Clone the repository

```bash
git clone https://github.com/2025tm93239/aceest-fitness.git
cd aceest-fitness
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest --version   # should print pytest 8.3.x
```

Your shell should use the venv interpreter (not `/bin/python3`):

```bash
which python3    # expected: .../aceest-fitness/.venv/bin/python3
```

### 3. Run the Flask development server

With the virtual environment still activated:

```bash
python3 app.py
```

The server listens on **http://127.0.0.1:5000**.

Expected response:

```json
{
  "service": "ACEest Fitness & Gym",
  "status": "ok",
  "version": "1.0.0"
}
```

Stop the server with `Ctrl+C`.

---

## API reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health / service status |
| `GET` | `/metrics` | Gym capacity and break-even metrics |
| `GET` | `/programs` | List available program names |
| `GET` | `/programs/<name>` | Workout, diet, and calorie factor for a program |
| `POST` | `/calories` | Estimate daily calories (JSON body) |
| `GET` | `/clients` | List saved clients |
| `POST` | `/clients` | Create or update a client profile |
| `GET` | `/clients/<name>` | Get one client by name |


---

## Running tests manually

From the **`aceest-fitness/` repository root** (the folder that contains `app.py` and `pytest.ini`), activate the venv and install dependencies if you have not already:

```bash
cd aceest-fitness
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -v
```

Use `python3 -m pytest` (instead of the bare `pytest` command) to match the Jenkins pipeline and avoid “command not found” when the venv `bin` folder is not on your PATH.

Syntax / compile check (same as CI lint stage):

```bash
python3 -m compileall -q app.py aceest tests
```

**Expected result:** `8 passed` (five API tests in `test_app.py`, three service tests in `test_services.py`).

### Troubleshooting

| Symptom | What to do |
|--------|------------|
| `No module named pytest` | You are using system Python (`/bin/python3`). Run `source .venv/bin/activate`, then `python3 -m pip install -r requirements.txt`, and confirm `which python3` points to `.venv/bin/python3`. |
| `pytest` / `python3` not found | Activate `.venv`, then run `python3 -m pytest -v`. |
| `ModuleNotFoundError: app` or `aceest` | `cd` into `aceest-fitness/` before running tests (needs `pytest.ini` `pythonpath = .`). |
| Dependencies missing | `python3 -m pip install -r requirements.txt` inside the activated venv. |

Tests cover:

- Service-layer calorie calculation and payload validation (`tests/test_services.py`)
- HTTP endpoints for health, programs, clients, and calories (`tests/test_app.py`)

Configuration: `pytest.ini` sets `pythonpath = .` so imports resolve correctly.

---

## Docker

Containerization packages the app and dependencies into a portable image (“write once, run anywhere”).

### Build the image

```bash
docker build -t aceest-fitness:latest .
```

### Run the API container

```bash
docker run -d -p 5000:5000 --name aceest aceest-fitness:latest
```

Open http://127.0.0.1:5000/ to verify.

### Run tests inside the image

```bash
docker run --rm aceest-fitness:latest pytest -v
```

### Stop and remove the container

```bash
docker stop aceest
docker rm aceest
```

### Troubleshooting

**`bind: address already in use` on port 5000** — Something else on the VM is already listening on `5000` (often a leftover `aceest` container, another Docker mapping, or the Flask dev server from `python3 app.py`). Check and free the port:

```bash
docker ps -a --filter name=aceest
docker stop aceest 2>/dev/null; docker rm aceest 2>/dev/null
ss -tlnp | grep ':5000'    # or: sudo lsof -i :5000
```

Stop the process shown (e.g. `Ctrl+C` in the terminal running Flask), then run the container again.

**Or** map the API to another host port (container still uses 5000 internally):

```bash
docker run -d -p 5001:5000 --name aceest aceest-fitness:latest
curl http://127.0.0.1:5001/
```

If `docker run` failed after creating a container, remove the broken instance before retrying: `docker rm -f aceest`.

**Image notes:**

- Base image: `python:3.9-slim` (aligned with lab VM Python 3.9.21)
- Application runs as non-root user `appuser`
- Production process: Gunicorn binding `0.0.0.0:5000`

---

## GitHub Actions (CI/CD)

Workflow file: **`.github/workflows/main.yml`**

### Triggers

- Every **push** to `main`
- Every **pull_request** targeting `main`

### Pipeline stages

1. **Build and lint** — Install `requirements.txt`, run `python -m compileall` on `app.py`, `aceest/`, and `tests/` to catch syntax errors.
2. **Docker image assembly** — `docker build -t aceest-fitness:ci .`
3. **Automated testing** — `docker run --rm aceest-fitness:ci pytest -v` (tests run in the containerized environment).

View run history: GitHub → **Actions** → workflow **Aceest Fitness CI/CD**.

```mermaid
flowchart LR
  A[Push / PR] --> B[Checkout]
  B --> C[compileall]
  C --> D[docker build]
  D --> E[pytest in container]
```

---

## Jenkins (BUILD and quality gate)

Jenkins provides a **secondary, controlled BUILD environment** on a dedicated server (separate from GitHub-hosted runners).

Configuration file: **`Jenkinsfile`** (Pipeline script from SCM).

### Jenkins job setup (summary)

1. Create a **Pipeline** job (e.g. `aceest-fitness-build`).
2. **Pipeline script from SCM** → Git → `https://github.com/2025tm93239/aceest-fitness.git`
3. Branch: `*/main` (or your integration branch).
4. Script Path: `Jenkinsfile`
5. Run **Build Now**.

# Troubleshooting steps
## Please note that when I ran first time, then build got failed with below error: 

#### Docker is not usable by this Jenkins user.

### We need to run below commnad to resolve the above error.  
Fix A (preferred) — on the Jenkins server as sudo:
          
          sudo systemctl enable --now docker

          sudo usermod -aG docker jenkins
          
          sudo systemctl restart jenkins
          
          sudo -u jenkins docker ps

### Jenkins pipeline stages

| Stage | Purpose |
|-------|---------|
| Checkout | Pull latest code from GitHub |
| Install dependencies | Clean `pip install -r requirements.txt` |
| Build (compile / syntax) | `compileall` quality check |
| Quality gate — unit tests | `pytest -v` on the Jenkins agent |
| Docker build | Tag image `aceest-fitness:<BUILD_NUMBER>` |
| Tests in container | `pytest` inside the built image |

After each run, the workspace is cleaned (`deleteDir`) so the next build starts fresh.

**Integration logic (GitHub Actions vs Jenkins):**

| Aspect | GitHub Actions | Jenkins |
|--------|----------------|---------|
| When it runs | On GitHub push/PR | On Jenkins schedule, webhook, or manual build |
| Where it runs | GitHub `ubuntu-latest` runner | Your Jenkins agent (Linux or macOS recommended for Bash/`sh` stages) |
| Config | `.github/workflows/main.yml` | `Jenkinsfile` + job UI |
| Role | Continuous integration on every change | Primary **BUILD** and quality gate in a controlled lab environment |

Detailed Jenkins installation steps: [`docs/JENKINS-SETUP.md`](docs/JENKINS-SETUP.md).

---