import asyncio
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer
import uuid
from ..config.settings import settings


class RAGService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )

        # Initialize sentence transformer model for embeddings
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

        # Collection name for textbook content
        self.collection_name = "textbook_content"

        # Create collection if it doesn't exist
        self._init_collection()

    def _init_collection(self):
        """Initialize the Qdrant collection for storing textbook content"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),  # 384 is the size for all-MiniLM-L6-v2
            )

    def add_content(self, content_id: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """Add content to the vector store"""
        try:
            # Generate embedding for the content
            embedding = self.encoder.encode([content])[0].tolist()

            # Prepare the point
            point = models.PointStruct(
                id=content_id,
                vector=embedding,
                payload={
                    "content": content,
                    "metadata": metadata or {}
                }
            )

            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            return True
        except Exception as e:
            print(f"Error adding content to vector store: {e}")
            return False

    def search_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant content based on the query"""
        try:
            # Generate embedding for the query
            query_embedding = self.encoder.encode([query])[0].tolist()

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "metadata": hit.payload.get("metadata", {}),
                    "score": hit.score
                })

            return results
        except Exception as e:
            print(f"Error searching content in vector store: {e}")
            return []

    def delete_content(self, content_id: str) -> bool:
        """Delete content from the vector store"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[content_id]
                )
            )
            return True
        except Exception as e:
            print(f"Error deleting content from vector store: {e}")
            return False

    def update_content(self, content_id: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """Update content in the vector store"""
        try:
            # Delete the old content
            self.delete_content(content_id)

            # Add the updated content
            return self.add_content(content_id, content, metadata)
        except Exception as e:
            print(f"Error updating content in vector store: {e}")
            return False

    def get_content_by_id(self, content_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve content by its ID"""
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[content_id]
            )

            if records:
                record = records[0]
                return {
                    "id": record.id,
                    "content": record.payload.get("content", ""),
                    "metadata": record.payload.get("metadata", {})
                }
            return None
        except Exception as e:
            print(f"Error retrieving content by ID: {e}")
            return None

    def batch_add_content(self, contents: List[Dict[str, Any]]) -> bool:
        """Add multiple content items to the vector store"""
        try:
            points = []
            for item in contents:
                content_id = item.get("id", str(uuid.uuid4()))
                content = item["content"]
                metadata = item.get("metadata", {})

                # Generate embedding for the content
                embedding = self.encoder.encode([content])[0].tolist()

                point = models.PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "metadata": metadata
                    }
                )
                points.append(point)

            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            return True
        except Exception as e:
            print(f"Error batch adding content to vector store: {e}")
            return False


# Global instance of RAG service
rag_service = RAGService()