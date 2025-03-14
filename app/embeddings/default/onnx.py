import os
import requests
import numpy as np
from tokenizers import Tokenizer
import onnxruntime as ort
from typing import List
from loguru import logger

MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
TOKENIZER_URL = "https://raw.githubusercontent.com/chroma-core/onnx-embedding/main/onnx/tokenizer.json"
MODEL_URL = "https://github.com/chroma-core/onnx-embedding/raw/main/onnx/model.onnx?download="

# Function to download files from a URL and save them locally
def download_file(url: str, local_path: str):
    response = requests.get(url)
    response.raise_for_status()  # Check if the download is successful
    with open(local_path, 'wb') as f:
        f.write(response.content)

# Ensure that the directory exists
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Use PyTorch's default epsilon for division by zero
def normalize(v):
    norm = np.linalg.norm(v, axis=1)
    norm[norm == 0] = 1e-12
    return v / norm[:, np.newaxis]

# Sample implementation of the default sentence-transformers model using ONNX
class DefaultEmbeddingModel():

    def __init__(self):
        # Define paths to save the tokenizer and model
        embedding_dir = os.path.join(os.getcwd(), "embeddings", "onnx")
        ensure_dir(embedding_dir)

        tokenizer_path = os.path.join(embedding_dir, "tokenizer.json")
        model_path = os.path.join(embedding_dir, "model.onnx")

        # Download the tokenizer and model from GitHub if they don't exist locally
        if not os.path.isfile(tokenizer_path):
            logger.info("Downloading tokenizer...")
            download_file(TOKENIZER_URL, tokenizer_path)

        if not os.path.isfile(model_path):
            logger.info("Downloading ONNX model...")
            download_file(MODEL_URL, model_path)

        # Load the tokenizer
        self.tokenizer = Tokenizer.from_file(tokenizer_path)
        self.tokenizer.enable_truncation(max_length=256)
        self.tokenizer.enable_padding(pad_id=0, pad_token="[PAD]", length=256)

        # Load the ONNX model
        self.model = ort.InferenceSession(model_path)

    def __call__(self, documents: List[str], batch_size: int = 32):
        all_embeddings = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            encoded = [self.tokenizer.encode(d) for d in batch]
            input_ids = np.array([e.ids for e in encoded])
            attention_mask = np.array([e.attention_mask for e in encoded])
            onnx_input = {
                "input_ids": np.array(input_ids, dtype=np.int64),
                "attention_mask": np.array(attention_mask, dtype=np.int64),
                "token_type_ids": np.array([np.zeros(len(e), dtype=np.int64) for e in input_ids], dtype=np.int64),
            }
            model_output = self.model.run(None, onnx_input)
            last_hidden_state = model_output[0]
            # Perform mean pooling with attention weighting
            input_mask_expanded = np.broadcast_to(np.expand_dims(attention_mask, -1), last_hidden_state.shape)
            embeddings = np.sum(last_hidden_state * input_mask_expanded, 1) / np.clip(input_mask_expanded.sum(1), a_min=1e-9, a_max=None)
            embeddings = normalize(embeddings).astype(np.float32)
            all_embeddings.append(embeddings)
        return np.concatenate(all_embeddings)


