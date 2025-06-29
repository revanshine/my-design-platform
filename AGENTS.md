# AI Agent Development Guidelines

This document provides comprehensive instructions for AI agents (like OpenAI Codex) working on the **On-Premise MCP Design Platform** project. These guidelines ensure consistent, high-quality code that follows Test-Driven Development practices and maintains architectural integrity.

## 🎯 Core Development Philosophy

### Test-Driven Development (TDD) is Mandatory

**Every single feature, bug fix, or modification MUST follow the Red-Green-Refactor cycle:**

1. **Red**: Write a failing test that describes the desired behavior
2. **Green**: Write the minimal code to make the test pass
3. **Refactor**: Clean up the code while keeping tests green

**NEVER write production code without a failing test first.** This is the only reliable pattern for automated development environments.

### Quality Gates

- **Test Coverage**: Minimum 95% line coverage, 90% branch coverage
- **All Tests Must Pass**: Zero tolerance for broken tests
- **No Skipped Tests**: Tests marked with `@pytest.mark.skip` are technical debt
- **Type Hints**: All functions must have complete type annotations
- **Documentation**: All public functions must have docstrings following Google style

## 🏗️ Project Architecture

### Core Structure

```

src/mcp_platform/
├── main.py                 \# FastAPI application entry point
├── servers/               \# Individual MCP server modules
│   ├── __init__.py
│   ├── base.py           \# Base classes and common patterns
│   ├── image_tools.py    \# Image processing MCP server
│   ├── file_tools.py     \# File system operations MCP server
│   └── workflow_tools.py \# Design workflow MCP server
├── jobs/                 \# Asynchronous job processing
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
└── fixtures/           \# Test data and helpers
├── __init__.py
├── sample_data.py
└── mock_servers.py

```

## 🔧 Development Guidelines

### 1. Before Writing Any Code

**ALWAYS start with these steps:**

1. **Create a test file** if it doesn't exist
2. **Write a failing test** that describes the exact behavior you want
3. **Run the test** and confirm it fails for the expected reason
4. **Only then** write the minimal code to make it pass

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
        image_paths: List of paths to input images
        output_format: Target format (jpeg, png, webp)
        quality: Compression quality (1-100)

    Returns:
        Dictionary containing processing results and metadata

    Raises:
        ValueError: If quality is not between 1 and 100
        FileNotFoundError: If any input image doesn't exist
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

1. **One test class per production class**
2. **Test methods describe behavior, not implementation**
3. **Use descriptive test names**: `test_resize_image_with_negative_dimensions_raises_value_error`

### Test Coverage

**Run these commands before every commit:**

```


# Run all tests with coverage

pytest --cov=src --cov-report=html --cov-report=term-missing

# Ensure no warnings

pytest --disable-warnings

# Check type hints

mypy src/

# Format code

black src/ tests/
isort src/ tests/

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

pytest

# 2. Coverage is acceptable

pytest --cov=src --cov-fail-under=95

# 3. No type errors

mypy src/

# 4. Code is formatted

black --check src/ tests/
isort --check-only src/ tests/

# 5. No linting issues

flake8 src/ tests/

```

### 3. Submitting Changes

**Every pull request must include:**

1. **Failing test(s)** that demonstrate the problem
2. **Minimal implementation** that makes tests pass
3. **Refactored code** that maintains quality
4. **Updated documentation** if public APIs changed
5. **No decrease in test coverage**

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

1. **Test Quality**: Are tests testing behavior, not implementation?
2. **Error Handling**: Are all edge cases covered?
3. **Type Safety**: Are all types properly annotated?
4. **Performance**: Are there obvious performance issues?
5. **Security**: Are inputs properly validated?

### Refactoring Guidelines

**When refactoring:**

1. **Keep tests green** throughout the process
2. **Make one change at a time**
3. **Run tests after each change**
4. **Don't change behavior and structure simultaneously**

---

## 📚 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python type hints](https://docs.python.org/3/library/typing.html)
- [Docker development best practices](https://docs.docker.com/develop/dev-best-practices/)

**Remember: The goal is to write code that works correctly, is easy to maintain, and can be understood by both humans and AI agents. Test-Driven Development is the path to achieving this goal reliably.**
