# mortyRAG

## Overview

This project, developed by Ant under HermiTech-LLC, implements a Retrieval-Augmented Generation (RAG) model that combines a document retrieval mechanism with a generative language model. The system is designed to produce witty, informative, and contextually appropriate responses, with a particular focus on physics-related content.

___
![mortspeak](https://github.com/agreene90/MortyRAG/blob/main/Screenshot%20from%202024-08-19%2023-18-01.png)
___

## Directory Structure

```plaintext
MortyRAG-main/
├── .github/workflows/           # GitHub Actions workflows
│   └── ci_cd.yml                # CI/CD pipeline configuration
├── custom_t5_rag_local_model_v1.0/
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
├── docs/
│   ├── api.md
│   ├── controller.md
│   ├── generation.md
│   ├── introduction.md
│   └── retrieval.md
├── LICENSE
├── README.md
├── Screenshot from 2024-08-19 23-18-01.png
├── generator.py
├── main.py            # Entry point script
├── rag.py
├── requirements.txt
└── retriever.py
```

## Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/HermiTech-LLC/MortyRAG.git
cd MortyRAG-main
pip install -r requirements.txt
```

### Requirements

Ensure your `requirements.txt` includes the following dependencies:

```plaintext
tkintertable
transformers
torch
Pillow
pyinstaller
```

These packages cover all necessary functionalities, including numerical operations, machine learning, API serving, testing, and text-to-speech.

## Usage

### 1. Data Ingestion

Before running the model, you need to prepare the knowledge base by processing the raw text data:

```bash
python src/data_ingestion.py
```

Ensure that your raw text files are located in the `data/raw/` directory. This script will preprocess the text data, vectorize it, and store the processed data in the `data/processed/` directory.

### 2. Creating the SQLite Database

If your project relies on document retrieval from a database, you need to create the SQLite database from your project files:

```bash
python src/create_file_database.py
```

This script will scan the `data/files/` directory, extract file metadata and content, and store it in an SQLite database located in `data/files/resources/project_files.db`.

### 3. Running the Application with Gunicorn

For production environments, it is recommended to use Gunicorn as your WSGI server. The system is already configured for this using the provided Docker setup:

#### **Using Docker:**

1. **Build the Docker Image**:
   ```bash
   docker build -t your-rag-system .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d -p 5000:5000 --name rag-system your-rag-system
   ```

   - The entrypoint script `entrypoint.sh` will handle database initialization and start the Gunicorn server.
   - The server will start on `http://0.0.0.0:5000/`. You can send POST requests to the `/generate` endpoint with a JSON payload containing the `query` parameter.

#### **Without Docker (Manual Setup):**

```bash
gunicorn --workers 3 --bind 0.0.0.0:5000 main:create_app
```

- `--workers 3`: Specifies the number of worker processes for handling requests. Adjust based on your server's CPU cores.
- `--bind 0.0.0.0:5000`: Binds the server to all available IP addresses on port 5000.

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

### 4. Text-to-Speech Functionality

Your system includes text-to-speech conversion for the generated responses. The speech output will be handled by the `pyttsx3` library, which operates locally without the need for an internet connection.

### 5. Testing

You can run the unit tests to ensure everything is working correctly:

```bash
python -m unittest discover -s tests
```

This command will automatically discover and run all the test modules in the `tests/` directory.

## Documentation

Detailed documentation for each module can be found in the `docs/` directory. Each file provides an in-depth explanation of the module's purpose, usage, and key functions.

## License

This project is licensed under the BSD 3-Clause License - see the `LICENSE` file for details.
