# RAG LLM Project

## Overview

This project, developed by Ant under HermiTech-LLC, implements a Retrieval-Augmented Generation (RAG) model that combines a document retrieval mechanism with a generative language model. The system is designed to produce witty, informative, and contextually appropriate responses, with a particular focus on physics-related content.

## Directory Structure

```
MortyRAG/
│
├── README.md                 # Project overview and instructions
├── LICENSE                   # BSD 3-Clause License for the project
│
├── data/
│   ├── raw/                  # Raw text files used to build the knowledge base
│   │   └── 01_physics_with_wit_and_wisdom.txt
│   └── processed/            # Processed data including vectors and models
│       ├── reduced_vectors.npy
│       ├── filenames.npy
│       ├── vectorizer.pkl
│       └── svd.pkl
│
├── src/                      # Source code for all modules
│   ├── data_ingestion.py     # Script for data ingestion and preprocessing
│   ├── knowledge_base.py     # Script for managing the knowledge base
│   ├── retrieval.py          # Script for document retrieval
│   ├── generation.py         # Script for generating responses
│   ├── controller.py         # Main script that integrates all components
│   └── api.py                # API script for exposing the model via a REST API
│
├── tests/
│   └── test_module.py        # Unit tests for the RAG model
│
└── docs/                     # Documentation for each module
    ├── introduction.md       # Project introduction and architecture overview
    ├── data_ingestion.md     # Documentation for the data ingestion module
    ├── knowledge_base.md     # Documentation for the knowledge base module
    ├── retrieval.md          # Documentation for the retrieval module
    ├── generation.md         # Documentation for the generation module
    ├── controller.md         # Documentation for the controller module
    └── api.md                # Documentation for the API module
```

## Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/HermiTech-LLC/rag_llm_project.git
cd rag_llm_project
pip install -r requirements.txt
```

## Usage

### 1. Data Ingestion

Before running the model, you need to prepare the knowledge base by processing the raw text data:

```bash
python src/data_ingestion.py
```

Ensure that your raw text files are located in the `data/raw/` directory. This script will preprocess the text data, vectorize it, and store the processed data in the `data/processed/` directory.

### 2. Running the API

To interact with the RAG model, you can start the Flask API server:

```bash
python src/api.py
```

The server will start on `http://0.0.0.0:5000/`. You can send POST requests to the `/generate` endpoint with a JSON payload containing the `query` parameter.

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

### 3. Testing

You can run the unit tests to ensure everything is working correctly:

```bash
python -m unittest discover -s tests
```

## Documentation

Detailed documentation for each module can be found in the `docs/` directory. Each file provides an in-depth explanation of the module's purpose, usage, and key functions.

## License

This project is licensed under the BSD 3-Clause License - see the `LICENSE` file for details.
