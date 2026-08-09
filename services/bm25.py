from rank_bm25 import BM25Okapi

from langchain_core.documents import Document

class Keyword():

    """Service for BM25 , which is a lexical search that is used for terms which are typically unique
    
    and needs exact match"""

    def __init__(self):

        self.bm25 = None
        self.documents : list[Document] = []

    def build_index(self,documents:list[Document]):

        self.documents = documents

        tokenized_documents = [
            document.page_content.lower().split() for document in documents 
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(self, query: str, top_k: int = 10):
        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = scores.argsort()[::-1][:top_k]

        results = []

        for index in ranked_indices:
            results.append(
                (
                    self.documents[index],
                    float(scores[index])
                )
            )

        return results

    