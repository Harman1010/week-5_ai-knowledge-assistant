from langchain_core.documents import Document

import numpy as np

import faiss

class VectorService:

    def __init__(self):

        self.index = None
        self.documents : list[Document] = []

    def build_index(self,documents:list[Document],embeddings):

        vectors = np.asarray(
            embeddings,dtype="float32"
        )

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)

        self.documents = documents

    def search(self,query_embed,top_k:int = 10):

        query_vector = np.asarray(
            [query_embed],dtype="float32"
        )

        scores,indices = self.index.search(
            query_vector,top_k
        )

        results = []

        for score,index in zip(scores[0],indices[0]):

            if index == -1:
                continue

            results.append(
                (self.documents[index],float(score))
            )

        return results