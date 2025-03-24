# Task Queue System

A simple task queue system built with FastAPI and Redis.

## Features

- Task queue management with Redis
- Automatic task retry mechanism
- Task status tracking (pending, processing, completed, failed)
- Docker support
- RESTful API endpoints
- Unit tests with pytest
- CI/CD pipeline with GitHub Actions
- Code coverage reporting with Codecov

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (if running locally)
- GitHub account (for CI/CD)
- Codecov account (for coverage reporting)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd task-queue
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Build and run with Docker:
```bash
docker-compose up --build
```

## Development Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies and package in development mode:
```bash
pip install -r requirements.txt
pip install -e .  # Install package in development mode
```

3. Run the application:
```bash
python main.py
```

4. Run tests:
```bash
pytest
```

## API Endpoints

- `GET /`: Health check endpoint
- `POST /tasks/`: Create a new task
- `GET /tasks/`: List all tasks (including pending, completed, and failed tasks)

## Example Usage

1. Create a new task:
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"id": "task1", "data": "test task"}'
```

2. List all tasks:
```bash
curl http://localhost:8000/tasks/
```

## Project Structure

- `task_queue/`: Main package directory
  - `__init__.py`: Package initialization
  - `main.py`: FastAPI application and API endpoints
  - `task_queue.py`: Redis-based task queue implementation
  - `worker.py`: Task processing worker
- `tests/`: Test files
  - `__init__.py`: Test package initialization
  - `test_main.py`: API endpoint tests
  - `conftest.py`: Test fixtures and configuration
- `.github/workflows/`: CI/CD configuration
  - `ci.yml`: Main CI pipeline
  - `docker-publish.yml`: Docker image publishing
- `setup.py`: Package configuration
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `docker-compose.yml`: Service orchestration
- `.env`: Environment variables (not committed to git)

## Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run locally:
```bash
python main.py
```

3. Run tests:
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run tests with coverage report
pytest --cov=.
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Continuous Integration
- Runs on every push and pull request
- Executes unit tests with coverage reporting
- Uploads coverage reports to Codecov
- Builds Docker image

### Continuous Deployment
- Deploys to Docker Hub on successful tests
- Tags Docker images with:
  - Git commit SHA
  - Semantic version (when tags are pushed)
  - Latest tag (for main branch)

### Setup CI/CD

1. Fork the repository
2. Add the following secrets to your GitHub repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token
   - `CODECOV_TOKEN`: Your Codecov repository upload token

3. Enable GitHub Actions in your repository settings

### Manual Deployment

To manually deploy a new version:

```bash
# Create and push a new tag
git tag v1.0.0
git push origin v1.0.0
```

## Code Coverage

The project uses Codecov for code coverage reporting. To view coverage reports:

1. Visit https://codecov.io/
2. Sign in with your GitHub account
3. Select your repository
4. View coverage reports and trends
