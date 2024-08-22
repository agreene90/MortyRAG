import os
import logging
import sys
import re
from pathlib import Path
from typing import Optional
from transformers import T5Tokenizer, T5ForConditionalGeneration
from generator import T5RAGWithLocalFiles
from retriever import ensure_dir

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_answer(
    query: str,
    file_path: Optional[Path] = None,
    max_length: int = 200,
    num_return_sequences: int = 1,
    temperature: float = 0.7,
    top_p: float = 0.95,
    model_version: str = "v1.0",
    save_model: bool = False,
    load_saved_model: bool = False,
    do_sample: bool = False,
    repetition_penalty: float = 1.0,
    length_penalty: float = 1.0,
    regex_filter: Optional[str] = None  # Optional regex filter parameter
) -> None:
    """
    Generate an answer using T5RAG with local file content and speak only the generated response.
    """
    try:
        if not query.strip():
            logger.error("Query cannot be empty or just whitespace.")
            raise ValueError("Query cannot be empty or just whitespace.")

        tokenizer = T5Tokenizer.from_pretrained("t5-base")
        generator = T5ForConditionalGeneration.from_pretrained("t5-base")
        logger.debug("Initialized tokenizer and generator model.")

        if load_saved_model:
            model_save_path = Path(f"./custom_t5_rag_local_model_{model_version}")
            if model_save_path.exists():
                try:
                    generator = T5ForConditionalGeneration.from_pretrained(model_save_path)
                    tokenizer = T5Tokenizer.from_pretrained(model_save_path)
                    logger.info(f"Loaded model version: {model_version} successfully.")
                except Exception as e:
                    logger.error(f"Error loading the model: {e}")
                    raise RuntimeError(f"Error loading the model: {e}")
            else:
                logger.error(f"Model path {model_save_path} does not exist.")
                raise FileNotFoundError(f"Model path {model_save_path} does not exist.")

        t5_rag_local_model = T5RAGWithLocalFiles(generator=generator, tokenizer=tokenizer)
        logger.debug("Initialized T5RAGWithLocalFiles model.")

        base_directory = Path('./data/raw/')
        context_documents = []
        for file_path in base_directory.rglob('*.txt'):
            content = file_path.read_text(encoding='utf-8')
            if regex_filter:
                content = ' '.join(re.findall(regex_filter, content))
            context_documents.append(content)
            if len(context_documents) >= 2:  # Limit number of documents for memory efficiency
                break
        
        combined_context = ' '.join(context_documents)[:1000]  # Limit to 1000 characters
        
        inputs = tokenizer(query + combined_context, return_tensors="pt")

        output_sequences = t5_rag_local_model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            repetition_penalty=repetition_penalty,
            length_penalty=length_penalty,
        )

        generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
        logger.info("Generated Answer: %s", generated_text)

        os.system(f'espeak "{generated_text}"')

        if save_model:
            model_save_path = Path(f"./custom_t5_rag_local_model_{model_version}")
            ensure_dir(model_save_path)
            generator.save_pretrained(model_save_path)
            tokenizer.save_pretrained(model_save_path)
            logger.info(f"Model and tokenizer saved at {model_save_path}.")

    except Exception as e:
        logger.critical(f"Failed to generate an answer: {e}")
        raise RuntimeError(f"Failed to generate an answer: {e}")

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        logger.error("Usage: python3 rag.py '<the query>' [optional: '<regex_filter>']")
        sys.exit(1)

    query = sys.argv[1]
    regex_filter = sys.argv[2] if len(sys.argv) == 3 else None

    generate_answer(query, regex_filter=regex_filter)
