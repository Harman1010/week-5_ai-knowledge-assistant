from sentence_transformers import CrossEncoder

from utils.config import settings


class RerankerService:

    def __init__(self):
        self.model = CrossEncoder(
            settings.reranker_model
        )

    def rerank(
        self,
        query: str,
        documents,
        top_k: int = 3
    ):
        pairs = [
            (query, document.page_content)
            for document, _ in documents
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            (document, float(score))
            for (document, _), score in ranked[:top_k]
        ]