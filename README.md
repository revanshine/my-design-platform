# On-Premise MCP Design Platform

A **professional-grade, containerized Model Context Protocol (MCP) server platform** designed for visual design tool workflows. This project provides a composable, scalable architecture for integrating multiple specialized tools into a unified AI-accessible interface.

Built for developers who want to "stay frosty" and implement cutting-edge technology patterns while maintaining production-quality standards.

## 🎯 Vision

Transform complex, multi-tool visual design workflows into AI-accessible services that can be operated remotely through chat interfaces. This platform serves as a proof of concept for professional MCP server architecture that can scale from hobby projects to enterprise solutions.

### Core Philosophy

- **Test-Driven Development**: Every feature is built with tests first, ensuring reliability and maintainability
- **Surgical Precision**: Focused, modular components that do one thing exceptionally well
- **Container-First**: Built for consistent deployment across development, staging, and production
- **AI-Native**: Designed specifically for AI agent interaction patterns

## 🚀 Features

### Current Capabilities

- **Composable MCP Architecture**: Multiple specialized FastMCP servers mounted under a unified FastAPI application
- **Asynchronous Job Processing**: Built-in support for long-running tasks with job queues and progress tracking
- **Container-First Deployment**: Complete Docker containerization with development and production configurations
- **Professional Testing**: Comprehensive test suite with near 100% coverage using pytest and TDD patterns
- **Modern Python Tooling**: Built with `uv`, `pyproject.toml`, and contemporary Python best practices
- **Plugin Architecture**: Tool servers discovered and mounted dynamically

### Planned Features

- **Visual Design Tool Integration**: Seamless interaction with design software APIs
- **Multi-Environment Support**: Development, staging, and production environment configurations
- **Monitoring & Observability**: Built-in logging, metrics, and health checks
- **Authentication & Authorization**: Secure access control for production deployments

## 🏗️ Architecture

```

┌─────────────────────────────────────────┐
│             LM Studio Client            │
└─────────────────┬───────────────────────┘
│ MCP Protocol
┌─────────────────▼───────────────────────┐
│         FastAPI Main Application        │
│     ┌─────────────────────────────────┐ │
│     │    Image Processing Tools       │ │
│     │    (FastMCP Server)            │ │
│     └─────────────────────────────────┘ │
│     ┌─────────────────────────────────┐ │
│     │    File System Tools           │ │
│     │    (FastMCP Server)            │ │
│     └─────────────────────────────────┘ │
│     ┌─────────────────────────────────┐ │
│     │    Design Workflow Tools        │ │
│     │    (FastMCP Server)            │ │
│     └─────────────────────────────────┘ │
└─────────────────┬───────────────────────┘
│
┌─────────────────▼───────────────────────┐
│          Job Queue System               │
│     (Redis/RabbitMQ + Workers)         │
└─────────────────────────────────────────┘

```

## 📋 Requirements

### Development Environment
- **Python**: 3.11+ (managed with `uv`)
- **Docker**: Latest stable version
- **Container Runtime**: Docker Desktop or compatible

### Target Deployment
- **Windows PC**: NVIDIA GPU-enabled workstation for design tools
- **macOS Client**: i.e. M4 Max with 48GB RAM running LM Studio

## 🚀 Quick Start

### 1. Clone and Setup

```


# Clone the repository

git clone https://github.com/yourusername/mcp-design-platform.git
cd mcp-design-platform

# Create and activate virtual environment with uv

uv venv
source .venv/bin/activate  \# On Windows: .venv\Scripts\activate

# Install dependencies

uv pip install -e .

```

### 2. Development with Docker

```


# Build the development image

docker build -f Dockerfile.dev -t mcp-platform:dev .

# Run with Docker Compose (includes Redis for job queue)

docker-compose -f docker-compose.dev.yml up -d

# The MCP server will be available at http://localhost:8080

```

### 3. Configure LM Studio

Add to your `mcp.json`:

```

{
  "mcpServers": {
    "design-platform": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "--interactive",
        "-p",
        "8080:8080",
        "mcp-platform:latest"
      ]
    }
  }
}

```

## 🧪 Testing

This project follows **strict Test-Driven Development** practices:

```


# Run all tests with coverage

pytest --cov=src --cov-report=html --cov-report=term

# Run tests in watch mode during development

pytest-watch

# Run only unit tests

pytest tests/unit/

# Run integration tests

pytest tests/integration/

```

**Coverage Target**: >95% line coverage, >90% branch coverage

## 📁 Project Structure

```

mcp-design-platform/
├── src/
│   ├── mcp_platform/
│   │   ├── main.py              \# FastAPI application entry point
│   │   ├── servers/             \# Individual MCP server modules
│   │   │   ├── image_tools.py
│   │   │   ├── file_tools.py
│   │   │   └── workflow_tools.py
│   │   ├── jobs/                \# Asynchronous job processing
│   │   │   ├── queue.py
│   │   │   ├── workers.py
│   │   │   └── tasks.py
│   │   └── config/              \# Configuration management
│   │       ├── settings.py
│   │       └── environments.py
├── tests/
│   ├── unit/                    \# Fast, isolated tests
│   ├── integration/             \# Component interaction tests
│   └── fixtures/                \# Test data and helpers
├── docker/
│   ├── Dockerfile               \# Production image
│   ├── Dockerfile.dev           \# Development image
│   └── docker-compose.yml       \# Multi-service orchestration
├── docs/                        \# Documentation
├── AGENTS.md                    \# AI development instructions
├── README.md                    \# This file
└── pyproject.toml              \# Modern Python project configuration

```

## 🗺️ Roadmap

### Phase 1: Foundation (Completed)
- [x] Project scaffolding with modern Python tooling
- [x] Basic FastAPI + FastMCP integration
- [x] Docker containerization
- [x] TDD workflow establishment
- [x] Redis job queue integration
- [x] Basic tool implementations

### Phase 2: Core Platform (In Progress)
- [ ] Complete asynchronous job processing system
- [ ] Progress tracking and status endpoints
- [ ] Comprehensive error handling and logging
- [ ] Production-ready Docker configurations
- [ ] CI/CD pipeline setup

### Phase 3: Design Tool Integration (Following 6-8 weeks)
- [ ] Visual design software API integrations
- [ ] File system operation tools
- [ ] Image processing and manipulation tools
- [ ] Workflow automation capabilities
- [ ] Cross-platform compatibility testing

### Phase 4: Production Features (Future)
- [ ] Authentication and authorization
- [ ] Multi-tenant support
- [ ] Monitoring and observability
- [ ] Performance optimization
- [ ] Enterprise deployment guides

## 🤝 Contributing

This project is designed to be developed collaboratively with AI agents using the patterns described in `AGENTS.md`.

### Development Workflow
1. **Issues First**: All work begins with a GitHub issue describing the requirement
2. **Test-Driven**: Write failing tests before implementing features
3. **Small Increments**: Keep changes focused and atomic
4. **Container Testing**: All tests must pass in containerized environments

### Getting Started
1. Review `AGENTS.md` for AI development guidelines
2. Check open issues for current priorities
3. Follow the TDD cycle: Red → Green → Refactor
4. Submit pull requests with comprehensive tests

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with inspiration from:
- [FastMCP](https://github.com/fastmcp/fastmcp) - The foundation for MCP server development
- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol specification
- Professional software development practices from the Python and containerization communities

---

*This project represents a commitment to professional-grade software development practices while exploring cutting-edge AI integration patterns. It's designed to be both a learning vehicle and a foundation for production systems.*