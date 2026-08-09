from services.embeddings import Embeddings
from services.vectorService import VectorService
from services.bm25 import Keyword


class HybridSearch:

    def __init__(self):
        self.embedding_service = Embeddings()
        self.vector_service = VectorService()
        self.bm25_service = Keyword()

    def build_indexes(self, documents):

        self.bm25_service.build_index(documents)

        texts = [
            document.page_content
            for document in documents
        ]

        embeddings = self.embedding_service.embed_doc(texts)

        self.vector_service.build_index(
            documents,
            embeddings
        )

    def search(
        self,
        query: str,
        top_k: int = 10,
        rrf_k: int = 60
    ):
       
        query_embedding = self.embedding_service.embed_query(query)

        vector_results = self.vector_service.search(
            query_embedding,
            top_k=top_k
        )

  
        bm25_results = self.bm25_service.search(
            query,
            top_k=top_k
        )

        rrf_scores = {}

        for rank, (document, _) in enumerate(vector_results, start=1):
            doc_id = id(document)

            rrf_scores[doc_id] = {
                "document": document,
                "score": 1 / (rrf_k + rank)
            }

        for rank, (document, _) in enumerate(bm25_results, start=1):
            doc_id = id(document)

            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = {
                    "document": document,
                    "score": 0.0
                }

            rrf_scores[doc_id]["score"] += (
                1 / (rrf_k + rank)
            )

        ranked_results = sorted(
            rrf_scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        return [
            (item["document"], item["score"])
            for item in ranked_results[:top_k]
        ]