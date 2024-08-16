# Retrieval

## Overview

The Retrieval module is responsible for finding the most relevant documents in the knowledge base based on a user's query. It uses cosine similarity to measure the relevance of documents in the reduced vector space.

## Process

1. **Query Vectorization**: The user query is transformed into a TF-IDF vector using the loaded vectorizer.
2. **Dimensionality Reduction**: The query vector is reduced using the pre-trained SVD model.
3. **Similarity Calculation**: Cosine similarity is computed between the query vector and all document vectors.
4. **Ranking**: Documents are ranked by their similarity to the query, with the top K documents being selected for response generation.

## Usage

To retrieve documents, use the `retrieve_documents` function:

```python
retrieved_docs = retrieve_documents(query, vectorizer, svd, vectors, filenames)
```

This will return a list of tuples containing the filenames and their corresponding similarity scores.
