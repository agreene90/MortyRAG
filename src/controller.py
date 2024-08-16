from data_ingestion import preprocess_documents
from knowledge_base import load_knowledge_base
from retrieval import retrieve_documents
from generation import generate_response

def main(query):
    vectorizer, svd, vectors, filenames = load_knowledge_base("./processed_data")
    
    retrieved_docs = retrieve_documents(query, vectorizer, svd, vectors, filenames)
    
    response = generate_response(retrieved_docs)
    
    return response

if __name__ == "__main__":
    query = "What is the history of the Eiffel Tower?"
    response = main(query)
    print("Generated Response:")
    print(response)
