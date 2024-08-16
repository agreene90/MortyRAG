# Knowledge Base

## Overview

The Knowledge Base module is designed to manage the storage and retrieval of vectorized documents. It uses a combination of vectorizer and SVD models to store documents in a reduced vector space, allowing for efficient similarity searches.

## Components

- **Vectorizer**: Converts text into TF-IDF vectors.
- **SVD Model**: Reduces the dimensionality of the vectors.
- **Storage**: The vectors, along with the models and metadata, are saved to disk for quick loading during retrieval.

## Functions

- **`save_knowledge_base`**: Saves the vectorizer, SVD model, and vectors to the specified directory.
- **`load_knowledge_base`**: Loads the vectorizer, SVD model, and vectors from disk.

## Usage

The knowledge base is automatically created during the data ingestion process. To load the knowledge base for retrieval, use:

```python
vectorizer, svd, vectors, filenames = load_knowledge_base("./processed_data")
```
