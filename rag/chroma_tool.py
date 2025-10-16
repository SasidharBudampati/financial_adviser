# chroma_tool.py
from beeai_framework.tools import Tool
from pydantic import BaseModel
from beeai_framework.tools import StringToolOutput
from bge_embedder import BGEEmbedder
from chromadb import Client
from chromadb.config import Settings

class RAGQuery(BaseModel):
    query: str

class ChromaRetrieverTool(Tool):
    name = "retrieve_from_chromadb"
    description = "Retrieves relevant documents from ChromaDB using BGE embeddings"
    input_schema = RAGQuery

    def __init__(self):
        super().__init__()
        self.embedder = BGEEmbedder()
        self.collection = Client(Settings(persist_directory="./chroma_store")) \
            .get_or_create_collection(name="financial_docs")

    async def _run(self, input: RAGQuery, options, context) -> StringToolOutput:
        res = await self.embedder.create([input.query])
        results = self.collection.query(query_embeddings=res.vectors, n_results=5)
        docs = results['documents'][0]
        return StringToolOutput("\n---\n".join(docs))

    def _create_emitter(self):
        return None