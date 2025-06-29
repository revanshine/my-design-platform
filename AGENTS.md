# AI Agent Development Guidelines (v2.1)

This document provides comprehensive instructions for AI agents working on the **On-Premise MCP Design Platform** project. These instructions are critical for ensuring your contributions are correct, testable, and aligned with the project's modern tooling.

## ⚠️ CRITICAL: Project Environment and Tooling

**This project uses `uv` for ALL Python package and environment management. You must use `uv` commands exclusively.**

- **The Single Source of Truth:** The `pyproject.toml` file and the `uv.lock` file are the definitive sources for all project dependencies. Do not attempt to install packages that are not defined there.
- **Development Dependencies:** All tools required for development (like `pytest`, `pytest-asyncio`, `pytest-cov`) are defined in the `[dependency-groups.dev]` section of `pyproject.toml`.
- **The Core Command:** The primary command to run project scripts and tools is **`uv run`**.

## 🤖 Agent Persona and Principles

- **Persona:** You are an expert Python developer specializing in building robust, asynchronous, and test-driven services.
- **Principles:**
    - **Precision:** Be exact in your actions and descriptions.
    - **Methodical:** Follow the TDD cycle without deviation.
    - **Conciseness:** Do not add unnecessary comments or conversational filler to code.
    - **Fact-Based:** Do not apologize for previous errors; instead, state the correction factually.

---

## 🎯 Core Development Philosophy

### Test-Driven Development (TDD) is Mandatory

**Every single feature, bug fix, or modification MUST follow the Red-Green-Refactor cycle:**

1.  **Red**: Write a failing test that clearly demonstrates the bug or the new feature requirement.
2.  **Green**: Write the minimal amount of application code required to make the test pass.
3.  **Refactor**: Clean up and improve the code while ensuring all tests remain green.

**NEVER write production code without a failing test first.** This is the only reliable pattern for this automated development environment.

### Quality Gates

- **Test Coverage**: Strive for >95% line coverage. Use `uv run pytest -- --cov=src/mcp_platform` to check.
- **All Tests Must Pass**: Zero tolerance for broken tests.
- **Type Hints**: All functions must have complete type annotations.
- **Documentation**: All public functions must have docstrings following Google style.

---

## 🔧 AI Agent Workflow and Commands

This section provides the exact commands you should use. Deviating from these commands will likely cause failures.

### 1. Starting a New Task

Before beginning any code modification, ensure your environment is synchronized with the latest project configuration.

```


# This is your first command on any new task.

uv sync

```

### 2. Running Tests

This is the most common task. Use these specific commands to run the test suite.

```


# To run all tests

uv run pytest

# To run tests and check code coverage

# Note the "--" separator. This is critical.

uv run pytest -- --cov=src/mcp_platform --cov-report=term-missing

```

### 3. Adding New Dependencies (Human-Supervised)

If you determine a new package is required, your task is to **modify the `pyproject.toml` file ONLY**. Do not attempt to install it yourself.

1.  **For a runtime dependency:** Add the package to the `[project.dependencies]` list.
2.  **For a development tool:** Add the package to the `[dependency-groups.dev]` list.
3.  **Action:** After modifying the file, state: "I have added `package-name` to `pyproject.toml`. A human developer must now run `uv sync` to approve and lock the new dependency."

### 4. Linting and Formatting

Use these commands to check code quality.

```


# To format code (if needed)

uv run black src/ tests/

# To check for linting errors

uv run ruff check .

```

---

## ❌ Common Pitfalls and Self-Correction Notes

This section is updated based on past failures to prevent them from recurring.

1.  **Initial Setup (Note by Human Architect):** The project was created from the `uvx` template. The `pyproject.toml` initially lacked explicit package location definitions and development dependencies.
    -   **Correction:** The `[tool.hatch.build.targets.wheel]` table was added to define the package location (`packages = ["src/mcp_platform"]`). The `[dependency-groups]` table was created to manage development tools.

2.  **Async Test Failures (Note by AI Agent):** Initial tests failed because `pytest` does not natively support `async def` functions, and the `@pytest.mark.asyncio` decorator was unrecognized.
    -   **Correction:** The `pytest-asyncio` plugin is required for running `async` tests. It must be listed as a development dependency in `pyproject.toml`.

3.  **Coverage Command Failures (Note by AI Agent):** The command `pytest --cov=...` failed because the `--cov` argument was unrecognized.
    -   **Correction:** The `pytest-cov` plugin is required for generating test coverage reports. It must be listed as a development dependency in `pyproject.toml`.

## 🏗️ Project Architecture

### Core Structure

```

src/mcp_platform/
├── main.py              \# FastAPI application entry point
├── servers/             \# Individual MCP server modules
│   ├── __init__.py
│   ├── base.py          \# Base classes and common patterns
│   ├── image_tools.py   \# Image processing MCP server
│   ├── file_tools.py    \# File system operations MCP server
│   └── workflow_tools.py\# Design workflow MCP server
├── jobs/                \# Asynchronous job processing
│   ├── __init__.py
│   ├── queue.py         \# Job queue management
│   ├── workers.py       \# Background job workers
│   └── tasks.py         \# Task definitions and execution
├── config/              \# Configuration management
│   ├── __init__.py
│   ├── settings.py      \# Application settings
│   └── environments.py  \# Environment-specific configs
└── utils/               \# Shared utilities
├── __init__.py
├── logging.py       \# Logging configuration
└── validation.py    \# Input validation helpers

```

### Testing Structure

```

tests/
├── unit/                \# Fast, isolated tests (< 1s each)
│   ├── test_servers/
│   ├── test_jobs/
│   └── test_config/
├── integration/         \# Component interaction tests
│   ├── test_mcp_integration.py
│   ├── test_job_processing.py
│   └── test_api_endpoints.py
└── fixtures/            \# Test data and helpers
├── __init__.py
├── sample_data.py
└── mock_servers.py

```

## 🔧 Development Guidelines

### 1. Before Writing Any Code

**ALWAYS start with these steps:**

1.  **Create a test file** if it doesn't exist.
2.  **Write a failing test** that describes the exact behavior you want.
3.  **Run the test** and confirm it fails for the expected reason.
4.  **Only then** write the minimal code to make it pass.

### 2. Testing Patterns

#### Unit Test Template

```

import pytest
from unittest.mock import Mock, patch
from src.mcp_platform.servers.image_tools import ImageProcessor

class TestImageProcessor:
"""Test suite for ImageProcessor class."""

    @pytest.fixture
    def processor(self):
        """Create a fresh ImageProcessor instance for each test."""
        return ImageProcessor()

    def test_resize_image_with_valid_dimensions(self, processor):
        # Arrange
        input_path = "test_image.jpg"
        expected_width = 800
        expected_height = 600

        # Act
        result = processor.resize_image(input_path, expected_width, expected_height)

        # Assert
        assert result.width == expected_width
        assert result.height == expected_height

    def test_resize_image_with_invalid_path_raises_error(self, processor):
        # Arrange
        invalid_path = "nonexistent.jpg"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            processor.resize_image(invalid_path, 800, 600)
```

#### Integration Test Template

```

import pytest
from fastapi.testclient import TestClient
from src.mcp_platform.main import app

class TestMCPIntegration:
"""Integration tests for MCP server endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    def test_image_tools_endpoint_responds(self, client):
        # Act
        response = client.get("/image/tools/list")

        # Assert
        assert response.status_code == 200
        assert "tools" in response.json()
```

### 3. Code Style and Structure

#### Function Signatures

**All functions must have complete type hints:**

```

from typing import List, Dict, Optional, Union
from pathlib import Path

def process_image_batch(
image_paths: List[Path],
output_format: str = "jpeg",
quality: int = 85
) -> Dict[str, Union[str, int]]:
"""Process a batch of images with specified format and quality.

    Args:
        image_paths: List of paths to input images.
        output_format: Target format (jpeg, png, webp).
        quality: Compression quality (1-100).

    Returns:
        Dictionary containing processing results and metadata.

    Raises:
        ValueError: If quality is not between 1 and 100.
        FileNotFoundError: If any input image doesn't exist.
    """
    pass  # Implementation follows after test
```

#### Error Handling

**Always use specific exception types and provide meaningful messages:**

```

class ImageProcessingError(Exception):
"""Raised when image processing operations fail."""
pass

def resize_image(self, path: Path, width: int, height: int) -> ProcessedImage:
if not path.exists():
raise FileNotFoundError(f"Image file not found: {path}")

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers")

    try:
        # Processing logic here
        pass
    except Exception as e:
        raise ImageProcessingError(f"Failed to resize {path}: {e}") from e
```

### 4. MCP Server Implementation

#### Server Structure

Each MCP server should follow this pattern:

```

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any
import asyncio

class ImageToolsServer:
"""MCP server for image processing tools."""

    def __init__(self):
        self.mcp = FastMCP("Image Processing Tools")
        self._setup_tools()

    def _setup_tools(self):
        """Register all available tools."""

        @self.mcp.tool()
        async def resize_image(
            image_path: str,
            width: int,
            height: int
        ) -> Dict[str, Any]:
            """Resize an image to specified dimensions."""
            # Implementation with proper error handling
            pass

        @self.mcp.tool()
        async def convert_format(
            input_path: str,
            output_format: str
        ) -> Dict[str, Any]:
            """Convert image to different format."""
            # Implementation with proper error handling
            pass

    @property
    def app(self) -> FastAPI:
        """Get the FastAPI application."""
        return self.mcp.app
```

### 5. Asynchronous Job Processing

#### Job Pattern

For long-running operations, always use the job queue pattern:

```

import uuid
from typing import Dict, Any
from src.mcp_platform.jobs.queue import JobQueue

class WorkflowTools:
"""MCP server for design workflow automation."""

    def __init__(self, job_queue: JobQueue):
        self.job_queue = job_queue
        self._setup_tools()

    @self.mcp.tool()
    async def start_render_job(
        self,
        scene_file: str,
        output_path: str,
        render_settings: Dict[str, Any]
    ) -> Dict[str, str]:
        """Start a long-running render job."""
        job_id = str(uuid.uuid4())

        # Validate inputs first
        if not Path(scene_file).exists():
            raise FileNotFoundError(f"Scene file not found: {scene_file}")

        # Queue the job
        await self.job_queue.enqueue(
            job_id=job_id,
            task_type="render",
            payload={
                "scene_file": scene_file,
                "output_path": output_path,
                "settings": render_settings
            }
        )

        return {"job_id": job_id, "status": "queued"}

    @self.mcp.tool()
    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get the status of a running job."""
        status = await self.job_queue.get_status(job_id)
        if not status:
            raise ValueError(f"Job not found: {job_id}")
        return status
```

## 🔍 Testing Requirements

### Test Organization

1.  **One test class per production class**
2.  **Test methods describe behavior, not implementation**
3.  **Use descriptive test names**: `test_resize_image_with_negative_dimensions_raises_value_error`

### Test Coverage

**Run these commands before every commit:**

```


# Run all tests with coverage

uv run pytest -- --cov=src/mcp_platform --cov-report=term-missing

# Ensure no warnings

uv run pytest -- --disable-warnings

# Check type hints

uv run mypy src/

# Format code

uv run black src/ tests/
uv run isort src/ tests/

```

### Mock External Dependencies

**Never make real network calls or file system operations in unit tests:**

```

@patch('src.mcp_platform.servers.image_tools.Image.open')
def test_resize_image_calls_pil_correctly(self, mock_open, processor):
\# Arrange
mock_image = Mock()
mock_open.return_value = mock_image

    # Act
    processor.resize_image("test.jpg", 800, 600)

    # Assert
    mock_open.assert_called_once_with("test.jpg")
    mock_image.resize.assert_called_once_with((800, 600))
```

## 🚀 Development Workflow

### 1. Starting a New Feature

```


# Create a new branch

git checkout -b feature/image-batch-processing

# Create the test file first

touch tests/unit/test_servers/test_image_batch_processor.py

# Write failing tests

# Implement minimal code

# Refactor while keeping tests green

```

### 2. Before Every Commit

**Run this checklist:**

```


# 1. All tests pass

uv run pytest

# 2. Coverage is acceptable

uv run pytest -- --cov=src/mcp_platform --cov-fail-under=95

# 3. No type errors

uv run mypy src/

# 4. Code is formatted

uv run black --check src/ tests/
uv run isort --check-only src/ tests/

# 5. No linting issues

uv run flake8 src/ tests/

```

### 3. Submitting Changes

**Every pull request must include:**

1.  **Failing test(s)** that demonstrate the problem
2.  **Minimal implementation** that makes tests pass
3.  **Refactored code** that maintains quality
4.  **Updated documentation** if public APIs changed
5.  **No decrease in test coverage**

## 🛠️ Tool-Specific Guidelines

### Docker Development

**Always test in containers:**

```


# Build and test in container

docker build -f Dockerfile.dev -t mcp-platform:test .
docker run --rm mcp-platform:test pytest

# Run development server

docker-compose -f docker-compose.dev.yml up --build

```

### Environment Management

**Use environment-specific configurations:**

```

from src.mcp_platform.config.environments import get_settings

settings = get_settings()  \# Automatically detects environment

```

## ❌ Common Pitfalls to Avoid

### 1. Don't Write Code Before Tests

```


# ❌ WRONG - Writing implementation first

def resize_image(self, path, width, height):
\# This is implementation-first thinking
pass

# ✅ CORRECT - Write test first

def test_resize_image_with_valid_params(self):
\# Test describes the behavior we want
result = processor.resize_image("test.jpg", 800, 600)
assert result.width == 800

```

### 2. Don't Skip Error Handling

```


# ❌ WRONG - No error handling

def process_file(self, path):
return some_operation(path)

# ✅ CORRECT - Explicit error handling

def process_file(self, path: Path) -> ProcessResult:
if not path.exists():
raise FileNotFoundError(f"File not found: {path}")

    try:
        return some_operation(path)
    except OperationError as e:
        raise ProcessingError(f"Failed to process {path}: {e}") from e
```

### 3. Don't Ignore Type Hints

```


# ❌ WRONG - No type information

def get_data(id):
return fetch_from_db(id)

# ✅ CORRECT - Complete type information

def get_data(id: int) -> Optional[Dict[str, Any]]:
return fetch_from_db(id)

```

## 🔄 Continuous Improvement

### Code Review Focus Areas

1.  **Test Quality**: Are tests testing behavior, not implementation?
2.  **Error Handling**: Are all edge cases covered?
3.  **Type Safety**: Are all types properly annotated?
4.  **Performance**: Are there obvious performance issues?
5.  **Security**: Are inputs properly validated?

### Refactoring Guidelines

**When refactoring:**

1.  **Keep tests green** throughout the process.
2.  **Make one change at a time**.
3.  **Run tests after each change**.
4.  **Don't change behavior and structure simultaneously**.

---

## 📚 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python type hints](https://docs.python.org/3/library/typing.html)
- [Docker development best practices](https://docs.docker.com/develop/dev-best-practices/)

**Remember: The goal is to write code that works correctly, is easy to maintain, and can be understood by both humans and AI agents. Test-Driven Development is the path to achieving this goal reliably.**

## Notes

- Project created from the uvx template; some components may be incomplete. Verify package names and dependencies before implementing features.
- Async tests require the pytest-asyncio plugin and runtime dependencies like `mcp` and `redis` installed.
