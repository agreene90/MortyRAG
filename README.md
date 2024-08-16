# mortyRAG

## Overview

This project, developed by Ant under HermiTech-LLC, implements a Retrieval-Augmented Generation (RAG) model that combines a document retrieval mechanism with a generative language model. The system is designed to produce witty, informative, and contextually appropriate responses, with a particular focus on physics-related content.
___
![mortspeak](https://github.com/HermiTech-LLC/MortyRAG/blob/main/Mortspeak.jpg)
___

## Directory Structure

```
MortyRAG-main/
├── data/
│   ├── raw/
│   │   ├── 01_physics_with_wit_and_wisdom.txt
│   │   ├── 02_science_with_a_twist.txt
│   │   ├── 03_sci_fi_and_reality.txt
│   │   ├── 04_black_holes_fact_vs_fiction.txt
│   │   ├── 05_quantum_computing_future.txt
│   │   ├── 06_time_travel_fact_vs_fiction.txt
│   │   ├── 07_gods_of_thunder_mythology.txt
│   │   ├── 08_hidden_wonders_of_earth.txt
│   │   ├── 09_calculus_derivatives.txt
│   │   ├── 10_strange_but_true_history.txt
│   │   ├── 11_rise_of_ai_fiction_vs_reality.txt
│   │   ├── 12_exploring_alien_civilizations.txt
│   │   └── 13_pop_culture_tech_influence.txt
│   └── files/
│       ├── documentation/
│       ├── resources/
│       └── logs/
├── docs/
│   ├── api.md
│   ├── controller.md
│   ├── data_ingestion.md
│   ├── generation.md
│   ├── introduction.md
│   ├── knowledge_base.md
│   └── retrieval.md
├── src/
│   ├── api.py
│   ├── controller.py
│   ├── data_ingestion.py
│   ├── generation.py
│   ├── knowledge_base.py
│   └── retrieval.py
├── tests/
│   ├── Placeholder
│   └── test_module.py
├── LICENSE
├── Mortspeak.jpg
├── README.md
├── requirements.txt
└── main.py
```

## Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/HermiTech-LLC/MortyRAG.git
cd MortyRAG-main
pip install -r requirements.txt
```

## Usage

### 1. Data Ingestion

Before running the model, you need to prepare the knowledge base by processing the raw text data:

```bash
python src/data_ingestion.py
```

Ensure that your raw text files are located in the `data/raw/` directory. This script will preprocess the text data, vectorize it, and store the processed data in the `data/processed/` directory.

### 2. Running the API with Gunicorn

To interact with the RAG model, you can start the Flask API server using Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 main:create_app
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
