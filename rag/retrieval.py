from rag.hybridSearch import HybridSearch
from rag.query_transform import QueryTransform
from services.rerank import RerankerService
from utils.config import settings


class RetrievalPipeline:

    def __init__(self):
        self.hybrid_search = HybridSearch()
        self.query_transformer = QueryTransform()
        self.reranker = RerankerService()

    def build(self, documents):
        self.hybrid_search.build_indexes(documents)

    def retrieve(self, query: str):

        queries = self.query_transformer.multi_query(
            query
        )

        # Always retain the original query
        queries.insert(0, query)

        candidates = {}

        for transformed_query in queries:

            results = self.hybrid_search.search(
                transformed_query,
                top_k=settings.top_k
            )

            for document, score in results:

                doc_id = id(document)

                if doc_id not in candidates:
                    candidates[doc_id] = {
                        "document": document,
                        "score": score
                    }
                else:
                    candidates[doc_id]["score"] += score

        candidate_documents = [
            (
                item["document"],
                item["score"]
            )
            for item in candidates.values()
        ]

        candidate_documents.sort(
            key=lambda x: x[1],
            reverse=True
        )

        reranked = self.reranker.rerank(
            query,
            candidate_documents,
            top_k=settings.rerank_top_k
        )

        return reranked