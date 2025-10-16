# ingest.py
import asyncio
from chromadb import Client
from chromadb.config import Settings
from rag.bge_embedder import BGEEmbedder
from llama_index.core.schema import Document
from datetime import datetime
from typing import List
from beeai_framework.backend import search_web

# Step 1: Setup ChromaDB
chroma_client = Client(Settings(persist_directory="D:\\projects\\chromadb"))
collection = chroma_client.get_or_create_collection(name="stock_docs")

# Step 2: Define stock symbols to fetch
STOCK_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "JPM", "V"]

# Step 3: Fetch stock details from the web
async def fetch_stock_descriptions(symbols: List[str]) -> List[str]:
    tasks = [
        search_web({"query": f"{symbol} stock profile"}) for symbol in symbols
    ]
    results = await asyncio.gather(*tasks)
    descriptions = []
    for result in results:
        if result and result.get("web_results"):
            top = result["web_results"][0]
            descriptions.append(f"{top['title']}\n{top['snippet']}")
        else:
            descriptions.append("No data found.")
    return descriptions

# Step 4: Embed and persist
async def ingest_stocks():
    embedder = BGEEmbedder()
    descriptions = await fetch_stock_descriptions(STOCK_SYMBOLS)
    embedding_res = await embedder.create(descriptions)

    # Add to ChromaDB
    collection.add(
        documents=descriptions,
        embeddings=embedding_res.vectors,
        ids=STOCK_SYMBOLS,
        metadatas=[{"symbol": s, "timestamp": str(datetime.utcnow())} for s in STOCK_SYMBOLS]
    )

if __name__ == "__main__":
    asyncio.run(ingest_stocks())