# Data Ingestion

## Overview

The Data Ingestion module is responsible for loading raw text data, preprocessing it, and converting it into vectorized form that can be stored in the knowledge base. It leverages techniques like TF-IDF for text vectorization and Truncated SVD for dimensionality reduction.

## Steps

1. **Loading Documents**: Reads text files from the specified directory.
2. **Preprocessing**: Cleans and processes text data, including lowering case, removing special characters, and tokenization.
3. **Vectorization**: Transforms the processed text into numerical vectors using TF-IDF.
4. **Dimensionality Reduction**: Applies Truncated SVD (also known as LSA) to reduce the dimensionality of the TF-IDF vectors, making the retrieval process more efficient.
5. **Saving Data**: Stores the vectorized data and associated metadata in the `processed_data` directory.

## Usage

Run the `data_ingestion.py` script to process your data:

```bash
python src/data_ingestion.py
```

Ensure that your raw text files are located in the `data/raw/` directory.
