import torch
import logging
from transformers import T5Tokenizer, T5ForConditionalGeneration
from pathlib import Path
from typing import Optional, Tuple
from retriever import read_local_file

logger = logging.getLogger(__name__)

class T5RAGWithLocalFiles(torch.nn.Module):
    """
    T5RAGWithLocalFiles integrates the T5 model with local file data for enhanced text generation.

    This class extends T5ForConditionalGeneration to incorporate content from local files into the text generation
    process, allowing for more contextually rich and informed responses.
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

        Args:
            input_ids (torch.Tensor): The input token IDs.
            attention_mask (torch.Tensor, optional): The attention mask for the input. Defaults to None.
            labels (torch.Tensor, optional): The labels for computing the loss. Defaults to None.

        Returns:
            Tuple[Optional[torch.Tensor], torch.Tensor]: The loss (if labels are provided) and logits from the model.
        """
        try:
            outputs = self.generator(input_ids, attention_mask=attention_mask, labels=labels)
            return outputs.loss, outputs.logits
        except Exception as e:
            logger.critical(f"Failed to forward pass through the model: {e}")
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

        Args:
            input_ids (torch.Tensor): The input token IDs.
            attention_mask (torch.Tensor): The attention mask for the input.
            file_path (Path, optional): Path to a local file whose content will be integrated into the input. Defaults to None.
            max_length (int): Maximum length of the generated sequences. Defaults to 200.
            num_return_sequences (int): Number of sequences to return. Defaults to 1.
            temperature (float): Sampling temperature for diversity. Defaults to 1.0.
            top_p (float): Nucleus sampling parameter for diversity. Defaults to 0.9.
            do_sample (bool): Whether to use sampling for text generation. Defaults to False.
            repetition_penalty (float): Penalty for repeating phrases during text generation. Defaults to 1.0.
            length_penalty (float): Penalty applied to the length of generated sequences. Defaults to 1.0.

        Returns:
            torch.Tensor: The generated sequences from the T5 model.
        """
        try:
            # Optionally read and integrate content from a local file
            file_content = read_local_file(file_path) if file_path else ""

            if file_content:
                # Tokenize the file content
                file_content_tokens = self.tokenizer(file_content, return_tensors="pt", truncation=True, padding=True)
                # Concatenate retrieved file content with the input query
                input_ids = torch.cat((input_ids, file_content_tokens['input_ids']), dim=-1)
                attention_mask = torch.cat((attention_mask, file_content_tokens['attention_mask']), dim=-1)

            # Generate output sequences using the T5 model
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
            logger.critical(f"Failed during text generation: {e}")
            raise