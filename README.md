# CustomAI

A lightweight **OpenAI-compatible API wrapper for Ollama**, built with FastAPI.

CustomAI exposes a `/v1/chat/completions` endpoint that accepts chat messages in an OpenAI-style format and forwards them to an Ollama model. A configurable system prompt is automatically added to every request.

## Features

* ⚡ FastAPI-based API
* 🤖 Ollama backend
* 🔌 OpenAI-compatible `/v1/chat/completions` endpoint
* 🐳 Docker support
* ⚙️ Simple configuration
* 📝 Request and response logging
* 🧠 Custom system prompt
* 🔄 Async HTTP requests using `httpx`

## Architecture

```text
Client
  │
  │ POST /v1/chat/completions
  ▼
┌─────────────────┐
│    CustomAI     │
│     FastAPI     │
└────────┬────────┘
         │
         │ Ollama API
         ▼
┌─────────────────┐
│     Ollama      │
│  Local LLM      │
└─────────────────┘
```

## Requirements

* Python 3.12+
* Ollama
* An Ollama model

Alternatively, CustomAI can be run using Docker.

## Installation

### Clone the repository

```bash
git clone https://github.com/PepeJEe/customai.git
cd customai
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Ollama

The default configuration is:

```python
OLLAMA_URL = "http://ollama:11434/api/chat"
MODEL_NAME = "gemma4:e2b"
```

These values can be changed in `config.py`.

Make sure the configured model exists in Ollama:

```bash
ollama pull gemma4:e2b
```

### Run CustomAI

```bash
uvicorn main:app --host 0.0.0.0 --port 8010
```

The API will be available at:

```text
http://localhost:8010
```

## Docker

The repository includes a `Dockerfile` that runs the application on port `8010`.

Build the image:

```bash
docker build -t customai .
```

Run it:

```bash
docker run -p 8010:8010 customai
```

When running CustomAI and Ollama in separate containers, the `OLLAMA_URL` should point to the Ollama container, for example:

```text
http://ollama:11434/api/chat
```

Make sure both containers are connected to the same Docker network.

## Configuration

Configuration is currently located in `config.py`.

```python
OLLAMA_URL = "http://ollama:11434/api/chat"
MODEL_NAME = "gemma4:e2b"

SYSTEM_PROMPT = "Your system prompt here"

ha_url = ""
ha_token = ""
```

### Options

| Setting         | Description                                   |
| --------------- | --------------------------------------------- |
| `OLLAMA_URL`    | URL of the Ollama `/api/chat` endpoint        |
| `MODEL_NAME`    | Ollama model to use                           |
| `SYSTEM_PROMPT` | System prompt prepended to every conversation |
| `ha_url`        | Home Assistant URL                            |
| `ha_token`      | Home Assistant authentication token           |

> **Note:** Home Assistant configuration is currently present in the configuration file but is not used by the chat request implementation.

## API

### Chat Completions

**Endpoint**

```http
POST /v1/chat/completions
```

**Request**

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

**Example with cURL**

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

### Response

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

## Using with OpenAI-Compatible Clients

Because CustomAI exposes an OpenAI-style chat completions endpoint, it can be used as a custom API endpoint by applications that support OpenAI-compatible providers.

For example:

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

## Project Structure

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
└── README.md
```

### `main.py`

Defines the FastAPI application and exposes the `/v1/chat/completions` endpoint.

### `llm.py`

Handles communication with Ollama and converts the incoming conversation into an Ollama chat request.

### `config.py`

Contains the Ollama URL, model name, and system prompt.

### `logger.py`

Provides application logging.

### `Dockerfile`

Builds a Python 3.12 container and starts the application with Uvicorn.

## How It Works

1. A client sends a request to `/v1/chat/completions`.
2. CustomAI receives the conversation messages.
3. The configured system prompt is prepended to the messages.
4. The resulting conversation is sent to Ollama.
5. Ollama generates a response using the configured model.
6. CustomAI returns the response using an OpenAI-style response structure.

## Limitations

This project currently implements a minimal subset of the OpenAI Chat Completions API.

Currently, the implementation does not provide:

* Streaming responses
* Token usage statistics
* Tool/function calling
* Vision-specific handling
* Multiple model routing
* Authentication
* Full OpenAI response compatibility

The `model` field is accepted by the API, but the configured `MODEL_NAME` in `config.py` is what is actually sent to Ollama.

## Development

Run the application in development mode:

```bash
uvicorn main:app --host 0.0.0.0 --port 8010 --reload
```

FastAPI's interactive API documentation is then available at:

```text
http://localhost:8010/docs
```

## License

See the repository for licensing information.

## Author

**PepeJEe**

GitHub: https://github.com/PepeJEe/customai
