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
├── generator.py         # Custom T5 model class for RAG with local file support
├── main.py              # Entry point script for the Optimization and Query handling GUI
├── rag.py               # Core logic for generating responses using the T5 model
├── requirements.txt     # Required Python packages
└── retriever.py         # Functions for reading and processing different file types
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

These packages cover all necessary functionalities, including GUI, machine learning, file processing, and packaging the application.

## Usage

### 1. Running the GUI Application

The main interface for interacting with the RAG model and performing optimizations is provided by the `main.py` script, which launches a user-friendly Tkinter-based GUI.

To start the application, simply run:

```bash
python main.py
```

### 2. Script Functionalities

#### `main.py`
- **Purpose**: Serves as the entry point for the Tkinter-based GUI, allowing users to perform optimization tasks and query handling through a simple interface.
- **Features**:
  - **Optimization Mode**: Runs iterative optimization to find the best possible response for a given query.
  - **Query Mode**: Handles single queries and returns an immediate response.
  - **File Integration**: Optionally includes local file contents as part of the query context.
  - **GUI Components**: Provides a polished, user-friendly interface with tooltips, placeholders, and progress indicators.

#### `generator.py`
- **Purpose**: Defines the `T5RAGWithLocalFiles` class, which integrates the T5 model with local file data for enhanced text generation.
- **Features**:
  - Extends `T5ForConditionalGeneration` to support additional context from local files.
  - Supports configuration of generation parameters such as maximum length, temperature, and sampling.

#### `rag.py`
- **Purpose**: Implements the core logic for generating responses using the T5 model.
- **Features**:
  - Handles text generation using the T5 model with support for local file integration.
  - Provides functions to generate answers, manage model loading/saving, and handle query processing.

#### `retriever.py`
- **Purpose**: Provides utilities for reading and processing content from various file formats.
- **Features**:
  - Supports reading from PDF, DOCX, CSV, JSON, ZIP, and image files.
  - Extracts text using appropriate methods (e.g., OCR for images, PyPDF2 for PDFs).

### Example Usage

After launching the GUI with `main.py`, you can:
- **Enter a query**: Type your question in the query input field.
- **Select a mode**: Choose between Optimization Mode or Query Mode.
- **(Optional) Specify a file path**: If you have a relevant document, provide its path to include its content in the context.
- **Start the process**: Click the "Start" button to run the query or optimization task.

### 3. Packaging the Application

You can package the application into an executable using PyInstaller. Run the following command:

```bash
pyinstaller --onefile --noconsole main.py
```

This will generate a standalone executable for your application, which can be distributed without requiring users to install Python.

## Documentation

Detailed documentation for each module can be found in the `docs/` directory. Each file provides an in-depth explanation of the module's purpose, usage, and key functions.

## License

This project is licensed under the BSD 3-Clause License - see the `LICENSE` file for details.
