"""
store.py - pure local vector storage. No LLM calls here at all.
Claude Code itself decides WHAT to remember; this just embeds and stores it.

Requires: pip install chromadb sentence-transformers
"""

import os
import uuid
import chromadb
from sentence_transformers import SentenceTransformer


class LocalStore:
    def __init__(self,
                 persist_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "project_mem_store"),
                 embedder="all-MiniLM-L6-v2", collection="project_memory"):
        self.embedder = SentenceTransformer(embedder)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(collection)

    def _embed(self, text: str):
        return self.embedder.encode(text).tolist()

    def remember(self, fact: str, project_id: str) -> str:
        """Store one fact/decision/convention, namespaced by project."""
        self.collection.add(
            ids=[str(uuid.uuid4())],
            documents=[fact],
            embeddings=[self._embed(fact)],
            metadatas=[{"project_id": project_id}],
        )
        return f"stored: {fact}"

    def recall(self, query: str, project_id: str, top_k: int = 5) -> list[str]:
        """Semantic search over this project's memories only."""
        res = self.collection.query(
            query_embeddings=[self._embed(query)],
            n_results=top_k,
            where={"project_id": project_id},
        )
        if not res["documents"] or not res["documents"][0]:
            return []
        return res["documents"][0]

    def list_all(self, project_id: str, limit: int = 100) -> list[str]:
        """Dump everything stored for this project (e.g. at session start)."""
        res = self.collection.get(where={"project_id": project_id}, limit=limit)
        return res["documents"]
