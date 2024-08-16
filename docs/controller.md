# Controller

## Overview

The Controller module integrates the various components of the RAG model into a cohesive workflow. It handles the end-to-end process from receiving a user query to returning the generated response.

## Workflow

1. **Load Knowledge Base**: Loads the vectorizer, SVD model, and vectors from the knowledge base.
2. **Retrieve Documents**: Uses the retrieval module to find the most relevant documents for the query.
3. **Generate Response**: Feeds the retrieved documents into the generation module to produce a final response.

## Usage

The main function in this module is the entry point for processing queries:

```python
response = main(query)
```

This function handles all steps, from loading the knowledge base to generating the final response.
