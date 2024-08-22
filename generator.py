import torch
import logging
from transformers import T5Tokenizer, T5ForConditionalGeneration
from pathlib import Path
from typing import Optional, Tuple
from retriever import read_local_file

logger = logging.getLogger(__name__)

class T5RAGWithLocalFiles(torch.nn.Module):
    """
    Integrates the T5 model with local file data for enhanced text generation.
    """

    def __init__(self, generator: T5ForConditionalGeneration, tokenizer: T5Tokenizer):
        """
        Initializes the T5RAGWithLocalFiles model.

        Args:
            generator (T5ForConditionalGeneration): The pre-trained T5 model for text generation.
            tokenizer (T5Tokenizer): The tokenizer associated with the T5 model.
        """
        super(T5RAGWithLocalFiles, self).__init__()
        self.generator = generator
        self.tokenizer = tokenizer

    def forward(self, input_ids: torch.Tensor, attention_mask: Optional[torch.Tensor] = None, labels: Optional[torch.Tensor] = None) -> Tuple[Optional[torch.Tensor], torch.Tensor]:
        """
        Forward pass through the T5 model.
        """
        try:
            outputs = self.generator(input_ids, attention_mask=attention_mask, labels=labels)
            return outputs.loss, outputs.logits
        except Exception as e:
            logger.critical(f"Forward pass failed: {e}")
            raise

    def generate(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        file_path: Optional[Path] = None,
        max_length: int = 200,
        num_return_sequences: int = 1,
        temperature: float = 1.0,
        top_p: float = 0.9,
        do_sample: bool = False,
        repetition_penalty: float = 1.0,
        length_penalty: float = 1.0
    ) -> torch.Tensor:
        """
        Generates text using the T5 model, optionally integrating content from a local file.
        """
        try:
            file_content = read_local_file(file_path) if file_path else ""
            if file_content:
                file_content_tokens = self.tokenizer(file_content, return_tensors="pt", truncation=True, padding=True)
                input_ids = torch.cat((input_ids, file_content_tokens['input_ids']), dim=-1)
                attention_mask = torch.cat((attention_mask, file_content_tokens['attention_mask']), dim=-1)

            output_sequences = self.generator.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                repetition_penalty=repetition_penalty,
                length_penalty=length_penalty,
            )

            logger.debug(f"Generated {num_return_sequences} sequence(s) with max length {max_length}.")
            return output_sequences

        except Exception as e:
            logger.critical(f"Generation failed: {e}")
            raise
