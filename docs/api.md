# API

## Overview

The API module provides a RESTful interface to the RAG model, allowing for easy integration with external applications. It is built using Flask and exposes endpoints for query processing.

## Endpoints

- **`/generate`** (POST): Accepts a JSON payload with a `query` parameter and returns the generated response.

### Example Request

```json
{
  "query": "Explain quantum mechanics in simple terms."
}
```

### Example Response

```json
{
  "response": "Quantum mechanics is the branch of physics that deals with the behavior of particles on a very small scale."
}
```

## Running the API

To start the API server, run:

```bash
python src/api.py
```

The server will be accessible at `http://0.0.0.0:5000/`.
