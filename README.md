# CustomAI

**An experimental OpenAI-compatible API gateway for working with locally hosted and cloud-based LLMs.**

> ⚠️ **Work in Progress / Learning Project**
>
> CustomAI is an unfinished personal project created primarily for learning and experimentation with **FastAPI, REST APIs, API compatibility, asynchronous HTTP communication, LLM providers, and Docker**.
>
> The current implementation is intentionally simple and does **not yet provide significant advantages over using Ollama or an LLM provider directly**. The project is a foundation for experimenting with a provider-independent AI API layer.

---

## Overview

CustomAI is a lightweight FastAPI service that exposes an **OpenAI-compatible chat-completions API** and forwards requests to an LLM backend.

The initial implementation was built around **Ollama**, allowing a client to communicate with a locally hosted model through CustomAI.

The long-term goal is to turn CustomAI into a more useful abstraction layer that can sit between an application and multiple LLM providers.

For example:

```text
                         ┌── Ollama
                         │    └── Qwen / local models
                         │
Client ── OpenAI API ── CustomAI ── OpenAI
                         │    └── GPT models
                         │
                         └── Other providers
```

The application using CustomAI would only need to communicate with one API, while CustomAI could determine which backend should handle each request.

---

## Current Architecture

At the moment, CustomAI primarily acts as an API adapter:

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

This means that CustomAI currently provides an OpenAI-compatible interface on top of Ollama, but does not yet add substantial functionality that would make it preferable to using Ollama directly.

This limitation is intentional: the current version is primarily a **learning exercise and foundation for future development**.

---

# Planned Architecture

The intended direction is to make CustomAI a provider-independent gateway.

```text
                         ┌──────────────┐
                         │   Ollama     │
                         │ Local Models │
                         └──────▲───────┘
                                │
                                │
┌──────────────┐        ┌───────┴───────┐
│              │        │               │
│   API Client ├───────►│   CustomAI    │
│              │        │               │
└──────────────┘        │ Provider      │
                        │ Abstraction   │
                        └───────┬───────┘
                                │
                         ┌──────▼───────┐
                         │    OpenAI    │
                         │  Cloud LLMs  │
                         └──────────────┘
```

This would allow the same application interface to work with different providers without requiring the application itself to implement provider-specific integrations.

---

# Features

### Current

* **FastAPI REST API**
* **OpenAI-compatible chat-completions endpoint**
* **Ollama integration**
* **Configurable system prompt**
* **Asynchronous HTTP communication with `httpx`**
* **Application logging**
* **Docker support**
* Simple API abstraction layer

### Planned

* Multiple LLM provider support
* Provider/model routing
* Local/cloud model selection
* Automatic provider fallback
* Centralized configuration
* Request logging and monitoring
* Rate limiting
* Authentication
* Provider-specific configuration
* Additional OpenAI-compatible functionality

---

# Tech Stack

| Technology   | Purpose                         |
| ------------ | ------------------------------- |
| **Python**   | Core programming language       |
| **FastAPI**  | REST API framework              |
| **Uvicorn**  | ASGI application server         |
| **Pydantic** | Request validation              |
| **httpx**    | Asynchronous HTTP communication |
| **Ollama**   | Local LLM inference             |
| **Docker**   | Containerization                |

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

The repository includes a `setup.sh` script that automates the local setup process.

Make the script executable:

```bash
chmod +x setup.sh
```

Run it:

```bash
./setup.sh
```

The script will:

1. Create a Python virtual environment
2. Activate the virtual environment
3. Install the dependencies from `requirements.txt`
4. Start the CustomAI server

### `setup.sh`

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

---

# Ollama Configuration

CustomAI currently uses Ollama as its LLM backend.

The configuration is defined in `config.py`.

Example:

```python
OLLAMA_URL = "http://ollama:11434/api/chat"
MODEL_NAME = "qwen3"
SYSTEM_PROMPT = "Your system prompt here"
```

Make sure the configured model is available in Ollama:

```bash
ollama pull qwen3
```

If Ollama is running directly on the host instead of inside Docker, configure the appropriate URL:

```python
OLLAMA_URL = "http://localhost:11434/api/chat"
```

---

# Running the API

After running:

```bash
./setup.sh
```

the API will be available at:

```text
http://localhost:8010
```

FastAPI's interactive documentation can be accessed at:

```text
http://localhost:8010/docs
```

---

# API

## `POST /v1/chat/completions`

CustomAI exposes an OpenAI-style chat-completions endpoint.

### Example request

```json
{
  "model": "qwen3",
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
    "model": "qwen3",
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

Because CustomAI exposes an OpenAI-compatible endpoint, applications that support a configurable API base URL can communicate with it using an OpenAI-style client.

For example:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8010/v1",
    api_key="not-required"
)

response = client.chat.completions.create(
    model="qwen3",
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

# Why an OpenAI-Compatible API?

OpenAI-compatible APIs provide a common interface for applications that interact with language models.

Different providers can expose similar request structures, allowing applications to change their backend without completely rewriting their integration.

For example:

```text
Application
     │
     ▼
OpenAI-compatible interface
     │
     ▼
   CustomAI
     │
     ├──────────► Ollama
     │             │
     │             └── Qwen
     │
     └──────────► OpenAI
                   │
                   └── GPT
```

The goal of CustomAI is to eventually make this abstraction useful by adding functionality on top of the provider APIs.

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

Handles communication between CustomAI and the configured LLM backend.

**`config.py`**

Contains the backend URL, model configuration, and system prompt.

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

CustomAI is currently a small experimental project and has several limitations.

It does **not** currently provide:

* Multiple LLM providers
* Provider/model routing
* Streaming responses
* Token usage statistics
* Tool/function calling
* Full OpenAI API compatibility
* Authentication
* Advanced request parameters
* Production-grade error handling
* Production security configuration
* A significant abstraction layer beyond forwarding requests

In particular, **Ollama already provides an OpenAI-compatible API**, so the current implementation can often be replaced by communicating with Ollama directly.

This is a known limitation of the current project and one of the main areas for future development.

---

# Future Improvements

The main goal for future development is to make CustomAI more than a simple proxy.

Potential improvements include:

* [ ] Support multiple LLM providers
* [ ] Add OpenAI backend support
* [ ] Add provider/model routing
* [ ] Allow switching between local and cloud models
* [ ] Add automatic fallback between providers
* [ ] Add streaming responses
* [ ] Improve OpenAI API compatibility
* [ ] Add authentication
* [ ] Add token usage tracking
* [ ] Add request logging and monitoring
* [ ] Add rate limiting
* [ ] Move configuration to environment variables
* [ ] Add automated tests
* [ ] Improve Docker Compose configuration
* [ ] Add Home Assistant integration
* [ ] Improve API documentation

---

# Learning Goals

CustomAI was created as a practical way to learn about several areas of software and AI development.

### Backend Development

* Building REST APIs with FastAPI
* Request validation with Pydantic
* Running applications with Uvicorn
* Structuring a Python backend
* Asynchronous HTTP communication

### AI Integration

* Communicating with locally hosted LLMs
* Working with the Ollama API
* Understanding LLM provider APIs
* Building an abstraction layer around an LLM

### API Design

* Understanding REST interfaces
* Designing OpenAI-compatible endpoints
* Using configurable API base URLs
* Understanding provider-independent API interfaces

### Infrastructure

* Containerizing applications with Docker
* Connecting services through Docker networking
* Running an AI backend as a separate service

---

# Project Status

## 🚧 Unfinished — Learning Project

CustomAI is an **unfinished personal learning project**.

The current implementation should not be considered production-ready, and its current role as an Ollama API wrapper provides limited additional functionality compared to using Ollama directly.

The purpose of the project is to provide a foundation for learning how to build an AI API service and, eventually, how to build a useful abstraction layer across multiple LLM providers.

The project may contain incomplete features, experimental code, and breaking changes.

---

# Author

**Perttu Vierimaa**

GitHub: [@PepeJEe](https://github.com/PepeJEe)

Repository: [PepeJEe/customai](https://github.com/PepeJEe/customai)
