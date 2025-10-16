from sentence_transformers import SentenceTransformer
from beeai_framework.backend.types import EmbeddingModelOutput

class BGEEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    async def create(self, values: list[str]) -> EmbeddingModelOutput:
        vectors = self.model.encode(values, normalize_embeddings=True)
        return EmbeddingModelOutput(values=values, embeddings=vectors.tolist())