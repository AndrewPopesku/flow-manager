# Flow Manager

A flow manager system for executing tasks sequentially with conditions to evaluate task success or failure and determine the flow's progression.

## Features

- Execute tasks sequentially based on defined flows
- Conditional task execution based on success/failure
- RESTful API for flow management
- Generic support for any number of tasks and conditions

## Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and virtual environment manager.

#### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

#### Set up the project

```bash
uv sync
```

#### Run commands with uv

```bash
# Run the development server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest
```

### Using traditional pip

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install .
```

## Running the Application

### Development Server

```bash
# With uv
uv run uvicorn app.main:app --reload

# Or with traditional approach
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker

The easiest way to run the application is using Docker:

```bash
# Build and run with docker-compose
docker-compose up

# Stop the application
docker-compose down
```

Or using Docker directly:

```bash
# Build the image
docker build -t flow-manager .

# Run the container
docker run -p 8000:8000 flow-manager
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
# With uv
uv run pytest

# Or traditional approach
pytest
```

## Project Structure

```
flow-manager/
├── app/
│   ├── engine.py       # Flow execution engine
│   ├── main.py         # FastAPI application entry point
│   ├── routes.py       # API route definitions
│   ├── schemas.py      # Pydantic models
│   └── tasks.py        # Task implementations
├── tests/
│   ├── test_api.py     # API tests
│   └── test_core.py    # Core engine tests
├── .dockerignore       # Docker build exclusions
├── .gitignore          # Git exclusions
├── .python-version     # Python version for uv
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker image definition
├── pyproject.toml      # Project metadata and dependencies
└── README.md
```
