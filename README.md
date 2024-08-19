# Mock vLLM API

This project provides a mock implementation of an OpenAI-compatible API, simulating a vLLM service.

## Features

- OpenAI-compatible API endpoints for chat completions and text completions
- Streaming and non-streaming response support
- Docker support for easy deployment

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`

## Usage

### Running the server

```bash
python ./main.py
```

Or using Docker:

```bash
docker build -t mock-vllm .
docker run -p 8000:8000 mock-vllm
```

### Testing with the client

```bash
python ./client.py
```

## API Endpoints

- `/chat/completions`: Chat completions endpoint
- `/completions`: Text completions endpoint
- `/test`: Simple test endpoint
