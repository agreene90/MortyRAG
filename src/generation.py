import os
import logging
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class ResponseGenerator:
    def __init__(self, model_name=None, max_input_length=None, max_output_length=None):
        """
        Initialize the ResponseGenerator with environment-configured parameters.

        Parameters:
        - model_name: The name of the pretrained model to use (fallback to env if None).
        - max_input_length: Maximum length of the input sequence for the model.
        - max_output_length: Maximum length of the generated output sequence.
        """
        self.model_name = model_name or os.getenv("MODEL_NAME", "t5-base")
        self.max_input_length = int(max_input_length or os.getenv("MAX_INPUT_LENGTH", 512))
        self.max_output_length = int(max_output_length or os.getenv("MAX_OUTPUT_LENGTH", 150))
        
        try:
            logger.info(f"Loading model and tokenizer for '{self.model_name}'...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            logger.info("Model and tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model '{self.model_name}': {str(e)}")
            raise

    def generate_response(self, retrieved_docs, num_beams=5):
        """
        Generate a response based on the retrieved documents.

        Parameters:
        - retrieved_docs: A list of tuples, where each tuple contains a document name and its content.
        - num_beams: Number of beams for beam search (default is 5).

        Returns:
        - response: The generated response as a string.
        """
        try:
            input_text = " ".join([f"{doc[0]}: {doc[1]}" for doc in retrieved_docs])
            logger.info("Encoding input text...")
            inputs = self.tokenizer.encode(input_text, return_tensors="pt", max_length=self.max_input_length, truncation=True)

            logger.info("Generating response...")
            with torch.no_grad():
                outputs = self.model.generate(inputs, max_length=self.max_output_length, num_beams=num_beams, early_stopping=True)

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.info("Response generated successfully.")
            return response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        # Set up logging
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(level=log_level)
        logger = logging.getLogger(__name__)

        # Example retrieved documents
        retrieved_docs = [
            ("Document1", "This is content from document 1."),
            ("Document2", "This is content from document 2.")
        ]

        logger.info("Initializing response generator...")
        generator = ResponseGenerator()

        logger.info("Generating response from retrieved documents...")
        response = generator.generate_response(retrieved_docs)

        print("Generated Response:")
        print(response)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
