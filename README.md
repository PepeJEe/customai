# CustomAI

**A lightweight OpenAI-compatible REST API wrapper for locally hosted Ollama models.**

> ⚠️ **Work in Progress / Learning Project**
>
> CustomAI is an unfinished personal project created primarily for learning and experimentation with **FastAPI, REST APIs, asynchronous HTTP communication, Ollama, Docker, and OpenAI-compatible APIs**.
>
> It is **not intended to be production-ready**.

---

## Overview

CustomAI provides a simple HTTP API around [Ollama](https://ollama.com/), allowing applications that support OpenAI-compatible APIs to communicate with a locally hosted language model through a custom FastAPI service.

The project exposes a `/v1/chat/completions` endpoint that accepts chat messages in an OpenAI-style format, adds a configurable system prompt, sends the conversation to Ollama, and returns the generated response.

The primary purpose of the project is educational: to explore how an AI service can be built around a REST API and how applications communicate with locally hosted language models.

---

## Architecture

```text
┌──────────────────────┐
│      API Client      │
│                      │
│ OpenAI-compatible   │
│ client / application │
└──────────┬───────────┘
           │
           │ POST /v1/chat/completions
           ▼
┌──────────────────────┐
│      CustomAI        │
│                      │
│       FastAPI        │
│    REST API layer    │
└──────────┬───────────┘
           │
           │ HTTP
           ▼
┌──────────────────────┐
│        Ollama        │
│                      │
│     Local LLM        │
└──────────────────────┘
```

### Request flow

1. A client sends a request to `/v1/chat/completions`.
2. CustomAI receives and validates the request.
3. The configured system prompt is added to the conversation.
4. CustomAI sends the conversation to Ollama.
5. Ollama generates the response using the configured model.
6. CustomAI returns the response using an OpenAI-style format.

---

## Features

* **FastAPI REST API**
* **Ollama integration**
* **OpenAI-compatible chat-completions endpoint**
* **Configurable system prompt**
* **Asynchronous HTTP communication with `httpx`**
* **Application logging**
* **Docker support**
* Simple and lightweight architecture
* Compatible with clients that support custom OpenAI API endpoints

---

## Tech Stack

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Core programming language       |
| FastAPI    | REST API framework              |
| Uvicorn    | ASGI application server         |
| Pydantic   | Request validation              |
| httpx      | Asynchronous HTTP communication |
| Ollama     | Local LLM inference             |
| Docker     | Containerization                |

---

# Getting Started

## Prerequisites

Before running CustomAI locally, make sure you have:

* Python 3 installed
* Ollama installed and running
* An Ollama-compatible language model
* Git

---

## Installation

Clone the repository:

```bash
git clone https://github.com/PepeJEe/customai.git
cd customai
```

The repository includes a `setup.sh` script that automatically:

1. Creates a Python virtual environment
2. Activates the virtual environment
3. Installs the required dependencies
4. Starts the CustomAI server

Make the script executable:

```bash
chmod +x setup.sh
```

Then run it:

```bash
./setup.sh
```

### What `setup.sh` does

```bash
#!/bin/bash

set -e

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Execute the server
./main.py
```

> **Note:** `setup.sh` creates the virtual environment every time it is executed. If the `venv` directory already exists, Python will reuse the existing environment.

---

## Ollama Configuration

CustomAI communicates with Ollama using the configuration defined in `config.py`.

For example:

```python
OLLAMA_URL = "http://ollama:11434/api/chat"
MODEL_NAME = "gemma4:e2b"
SYSTEM_PROMPT = "Your system prompt here"
```

Make sure the configured model is available in Ollama:

```bash
ollama pull gemma4:e2b
```

If Ollama is running directly on your host machine rather than in Docker, change `OLLAMA_URL` accordingly.

For example:

```python
OLLAMA_URL = "http://localhost:11434/api/chat"
```

---

## Running the API

After running:

```bash
./setup.sh
```

the API will be available at:

```text
http://localhost:8010
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8010/docs
```

---

# API

## `POST /v1/chat/completions`

CustomAI provides an OpenAI-style chat-completions endpoint.

### Example request

```json
{
  "model": "gemma4:e2b",
  "messages": [
    {
      "role": "user",
      "content": "Hello!"
    }
  ]
}
```

### cURL

```bash
curl http://localhost:8010/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4:e2b",
    "messages": [
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
```

### Example response

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help?"
      },
      "finish_reason": "stop"
    }
  ]
}
```

---

# OpenAI-Compatible Clients

Because CustomAI exposes an OpenAI-style endpoint, it can be used with clients that allow a custom API base URL.

For example, using the OpenAI Python client:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8010/v1",
    api_key="not-required"
)

response = client.chat.completions.create(
    model="gemma4:e2b",
    messages=[
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
)

print(response.choices[0].message.content)
```

The API key is currently not used for authentication by CustomAI.

---

# Docker

CustomAI also includes Docker configuration for running the application in a containerized environment.

Build the image:

```bash
docker build -t customai .
```

Run the container:

```bash
docker run -p 8010:8010 customai
```

When CustomAI and Ollama run in separate Docker containers, they should be placed on the same Docker network so that CustomAI can communicate with Ollama.

---

# Configuration

Configuration is currently stored in `config.py`.

| Setting         | Description                                  |
| --------------- | -------------------------------------------- |
| `OLLAMA_URL`    | URL of the Ollama API                        |
| `MODEL_NAME`    | Model used for inference                     |
| `SYSTEM_PROMPT` | System prompt added to conversations         |
| `ha_url`        | Reserved Home Assistant configuration        |
| `ha_token`      | Reserved Home Assistant authentication token |

> **Note:** The Home Assistant configuration is currently present for future experimentation and is not part of the current chat implementation.

---

# Project Structure

```text
customai/
├── .github/
│   └── workflows/
├── Dockerfile
├── docker-compose.yml
├── config.py
├── llm.py
├── logger.py
├── main.py
├── requirements.txt
├── setup.sh
└── README.md
```

### Components

**`main.py`**

Defines the FastAPI application and API endpoints.

**`llm.py`**

Handles communication between CustomAI and Ollama using asynchronous HTTP requests.

**`config.py`**

Contains the Ollama endpoint, model configuration, and system prompt.

**`logger.py`**

Provides application logging.

**`Dockerfile`**

Defines the Docker image used to run CustomAI.

**`docker-compose.yml`**

Provides Docker Compose configuration for running the services.

**`setup.sh`**

Automates the local Python environment setup and starts the application.

---

# Current Limitations

CustomAI currently implements only a small subset of the OpenAI API.

The project does **not** currently support:

* Streaming responses
* Token usage statistics
* Tool/function calling
* Full OpenAI API compatibility
* Authentication
* Multiple model routing
* Advanced request parameters
* Production-grade error handling
* Production security configuration

The project is intentionally minimal and is expected to change as development continues.

---

# Learning Goals

This project was created as a practical way to learn about:

### Backend Development

* Building REST APIs with FastAPI
* Request validation with Pydantic
* Running applications with Uvicorn
* Structuring a Python backend

### AI Integration

* Communicating with locally hosted LLMs
* Working with the Ollama API
* Building an abstraction layer around an LLM
* Understanding chat-based API structures

### API Design

* Understanding REST interfaces
* Creating OpenAI-compatible endpoints
* Using custom API base URLs
* Connecting applications to custom AI backends

### Infrastructure

* Containerizing applications with Docker
* Connecting services through Docker networking
* Running an AI backend as a separate service

---

# Future Improvements

Possible future improvements include:

* [ ] Add streaming responses
* [ ] Improve OpenAI API compatibility
* [ ] Add authentication
* [ ] Support configurable model selection
* [ ] Add token usage information
* [ ] Add tool/function calling
* [ ] Move configuration to environment variables
* [ ] Add automated tests
* [ ] Improve Docker Compose configuration
* [ ] Add Home Assistant integration
* [ ] Improve API documentation
* [ ] Expand CI/CD checks

---

# Project Status

## 🚧 Unfinished — Learning Project

CustomAI is an **unfinished personal learning project**.

It is not intended to be a production-ready AI platform, API gateway, or replacement for established AI frameworks.

The project exists primarily to experiment with and gain practical experience in:

```text
FastAPI
   ↓
REST API
   ↓
OpenAI-compatible interface
   ↓
Ollama
   ↓
Local LLM
```

Because this is an experimental project, the implementation may contain incomplete features, limitations, and breaking changes.

---

# Why This Project?

Rather than interacting with Ollama directly, CustomAI explores what is involved in creating an intermediate API layer between an application and a locally hosted language model.

The project provides hands-on experience with the complete request flow:

```text
Application
     │
     ▼
OpenAI-compatible API
     │
     ▼
CustomAI
     │
     ▼
Ollama
     │
     ▼
Local Language Model
```

Building this layer from scratch makes it possible to experiment with API design, asynchronous communication, request validation, Docker networking, and local LLM integration in a single project.

---

# Author

**Perttu Vierimaa**

GitHub: [@PepeJEe](https://github.com/PepeJEe)

Repository: [PepeJEe/customai](https://github.com/PepeJEe/customai)
