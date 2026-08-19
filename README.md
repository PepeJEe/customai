# CustomAI

**An experimental AI backend for controlling and interacting with Home Assistant using natural language.**

> ⚠️ **Work in Progress / Learning Project**
>
> CustomAI is an unfinished personal project created primarily for learning and experimentation with **LLMs, FastAPI, REST APIs, Home Assistant, asynchronous communication, Docker, and AI tool integration**.
>
> The project is **not production-ready** and many planned features are still incomplete.

---

## Overview

CustomAI is an experimental AI service designed to provide a more flexible, natural-language interface for **Home Assistant**.

The idea is to allow an LLM to interact with a Home Assistant instance through its API, giving users the ability to control and query their smart home without being restricted to the standard Home Assistant interface.

For example, instead of manually navigating Home Assistant, a user could eventually interact with CustomAI using requests such as:

> "Turn off all the lights downstairs."

> "What's the temperature in the bedroom?"

> "I'm going to bed."

> "Make the living room cozy."

CustomAI can then use the LLM to understand the request, inspect the available Home Assistant entities, and perform the appropriate actions.

---

## Concept

The long-term goal is to create an architecture where the LLM acts as a natural-language interface to Home Assistant.

```text
┌─────────────────┐
│      User       │
│                 │
│ "I'm going to   │
│      bed."      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    CustomAI     │
│                 │
│    FastAPI      │
│   AI Backend    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│       LLM       │
│                 │
│   Qwen / Ollama │
└────────┬────────┘
         │
         │ Tool / API calls
         ▼
┌─────────────────┐
│ Home Assistant  │
│                 │
│ Lights          │
│ Sensors         │
│ Climate         │
│ Media           │
│ Switches        │
└─────────────────┘
```

The LLM is responsible for interpreting the user's intent, while CustomAI provides the interface between the model and Home Assistant.

---

# Current Architecture

The current implementation is still relatively simple.

```text
┌──────────────┐
│              │
│    Client    │
│              │
└──────┬───────┘
       │
       │ OpenAI-compatible API
       ▼
┌──────────────────┐
│                  │
│     CustomAI     │
│                  │
│     FastAPI      │
│                  │
└────────┬─────────┘
         │
         │ LLM request
         ▼
┌──────────────────┐
│      Ollama      │
│                  │
│   Qwen / LLM     │
└──────────────────┘
```

Home Assistant integration is part of the project's intended architecture and is still under development.

The goal is eventually:

```text
                         ┌───────────────┐
                         │ Home Assistant│
                         │               │
                         │ Devices       │
                         │ Sensors       │
                         │ Automations   │
                         │ Services      │
                         └───────▲───────┘
                                 │
                          HA API / WebSocket
                                 │
                                 │
┌──────────────┐          ┌──────┴──────┐
│              │          │             │
│    User      ├─────────►│  CustomAI   │
│              │          │             │
└──────────────┘          │  AI Backend │
                          └──────┬──────┘
                                 │
                                 ▼
                          ┌─────────────┐
                          │ LLM Backend │
                          │             │
                          │ Qwen/Ollama │
                          │ Other LLMs  │
                          └─────────────┘
```

---

# Why CustomAI?

Home Assistant already provides powerful automation and control capabilities.

The purpose of CustomAI is not to replace Home Assistant, but to provide another way of interacting with it.

Instead of requiring users to know exactly which entity, service, automation, or device they need to interact with, an LLM can translate natural language into the appropriate Home Assistant actions.

For example:

```text
User:
"Turn off everything except the bedroom light."

             ↓

             LLM

             ↓

Identify relevant entities
             ↓
Call Home Assistant services
             ↓

Lights OFF
Bedroom light ON
```

This makes it possible to experiment with more flexible and context-aware smart-home interactions.

---

# Features

### Current

* **FastAPI REST API**
* **OpenAI-compatible chat-completions endpoint**
* **Ollama integration**
* **Local LLM support**
* **Configurable system prompt**
* **Asynchronous HTTP communication**
* **Application logging**
* **Docker support**

### Planned

* Home Assistant entity discovery
* Reading Home Assistant entity states
* Calling Home Assistant services
* Natural-language device control
* LLM tool/function calling
* Context-aware Home Assistant interactions
* Multiple LLM providers
* Local/cloud model selection
* Provider/model routing
* Conversation history
* Permission controls for potentially dangerous actions

---

# Tech Stack

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| **Python**         | Core programming language       |
| **FastAPI**        | REST API framework              |
| **Uvicorn**        | ASGI application server         |
| **Pydantic**       | Request validation              |
| **httpx**          | Asynchronous HTTP communication |
| **Ollama**         | Local LLM inference             |
| **Qwen**           | Current LLM experimentation     |
| **Home Assistant** | Smart-home platform             |
| **Docker**         | Containerization                |

---

# Getting Started

## Prerequisites

Before running CustomAI locally, make sure you have:

* Python 3 installed
* Ollama installed and running
* An Ollama-compatible model
* A Home Assistant instance if you want to experiment with the Home Assistant integration
* Git

---

## Installation

Clone the repository:

```bash
git clone https://github.com/PepeJEe/customai.git
cd customai
```

The repository includes a `setup.sh` script that automates the local Python setup.

Make it executable:

```bash
chmod +x setup.sh
```

Run the setup script:

```bash
./setup.sh
```

The script will:

1. Create a Python virtual environment
2. Activate the virtual environment
3. Install dependencies from `requirements.txt`
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

Configuration is defined in `config.py`.

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

# Home Assistant Integration

Home Assistant is one of the main goals of the project.

The intended integration is for CustomAI to communicate with Home Assistant through its API and eventually allow the LLM to interact with Home Assistant entities and services.

The planned flow is:

```text
User request
     │
     ▼
CustomAI
     │
     ▼
LLM interprets request
     │
     ▼
Determine required Home Assistant action
     │
     ▼
Home Assistant API
     │
     ▼
Device / Entity
```

For example:

```text
"Turn on the living room lights."

        ↓

LLM identifies:
light.living_room

        ↓

CustomAI calls Home Assistant

        ↓

light.turn_on
```

The Home Assistant integration is currently **unfinished** and should be considered experimental.

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

CustomAI exposes an OpenAI-compatible endpoint, allowing clients that support a configurable API base URL to communicate with the service.

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

The OpenAI-compatible interface is useful because it keeps the client side independent from the specific LLM backend.

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

Contains backend configuration, model configuration, and system prompts.

**`logger.py`**

Provides application logging.

**`Dockerfile`**

Defines the Docker image used to run CustomAI.

**`docker-compose.yml`**

Provides Docker Compose configuration for running the application and its services.

**`setup.sh`**

Automates the local Python environment setup and starts the server.

---

# Current Limitations

CustomAI is currently a small experimental project.

The current implementation does **not yet provide**:

* Full Home Assistant control
* LLM tool/function calling
* Home Assistant entity discovery
* Home Assistant state awareness
* Streaming responses
* Multiple LLM providers
* Provider/model routing
* Token usage statistics
* Authentication
* Full OpenAI API compatibility
* Production-grade error handling
* Production security configuration
* Persistent conversation memory

Additionally, Ollama already provides an OpenAI-compatible API, meaning the current CustomAI implementation can often be replaced by communicating with Ollama directly.

This is a known limitation of the current implementation.

The project's intended value comes from the planned **Home Assistant integration and AI-driven interaction layer**, rather than simply forwarding requests to Ollama.

---

# Future Improvements

The main goal is to evolve CustomAI from a simple LLM API wrapper into an AI interface for Home Assistant.

### Home Assistant

* [ ] Connect to Home Assistant API
* [ ] Authenticate with Home Assistant
* [ ] Discover available entities
* [ ] Read entity states
* [ ] Call Home Assistant services
* [ ] Control lights, switches, climate, media, etc.
* [ ] Provide relevant entity information to the LLM
* [ ] Add permission controls for sensitive actions

### LLM

* [ ] Implement tool/function calling
* [ ] Allow the LLM to invoke Home Assistant actions
* [ ] Add conversation context
* [ ] Support multiple LLM providers
* [ ] Support local and cloud models
* [ ] Add model/provider routing
* [ ] Add fallback providers

### API

* [ ] Improve OpenAI API compatibility
* [ ] Add streaming responses
* [ ] Add authentication
* [ ] Add token usage tracking
* [ ] Improve error handling
* [ ] Add automated tests
* [ ] Improve API documentation

### Infrastructure

* [ ] Improve Docker Compose configuration
* [ ] Improve configuration management
* [ ] Add environment-variable based secrets
* [ ] Improve CI/CD
* [ ] Add monitoring and request logging

---

# Learning Goals

CustomAI was created as a practical project for learning about modern backend and AI development.

### Backend Development

* Building REST APIs with FastAPI
* Request validation with Pydantic
* Running applications with Uvicorn
* Structuring a Python backend
* Asynchronous HTTP communication

### AI Development

* Working with locally hosted LLMs
* Communicating with Ollama
* Understanding LLM APIs
* Prompt engineering
* Exploring LLM tool/function calling
* Connecting LLMs to external systems

### Home Automation

* Working with the Home Assistant API
* Reading entity states
* Calling Home Assistant services
* Translating natural language into device actions
* Building an AI-driven smart-home interface

### API Design

* Understanding REST interfaces
* Designing OpenAI-compatible endpoints
* Creating provider-independent interfaces
* Building abstractions around external services

### Infrastructure

* Containerizing applications with Docker
* Connecting multiple services
* Managing configuration and secrets
* Running AI services locally

---

# Project Status

## 🚧 Unfinished — Learning Project

CustomAI is an **unfinished personal learning project**.

The current implementation is primarily an experimental FastAPI layer around an Ollama-hosted LLM. It should **not** be considered production-ready.

The main long-term goal is to connect an LLM with Home Assistant and create a flexible natural-language interface for controlling and querying a smart home.

The project is intended to be a practical learning exercise covering:

```text
FastAPI
   │
   ├── REST API
   │
   ├── LLM Integration
   │      └── Ollama / Qwen
   │
   ├── Home Assistant API
   │
   └── AI Tool Integration
```

Expect incomplete functionality, experimental code, and breaking changes as development continues.

---

# Author

**Perttu Vierimaa**

GitHub: [@PepeJEe](https://github.com/PepeJEe)

Repository: [PepeJEe/customai](https://github.com/PepeJEe/customai)
