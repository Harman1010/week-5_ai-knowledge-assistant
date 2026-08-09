from sentence_transformers import SentenceTransformer

from utils.config import settings

class Embeddings():

    """A blueprint that defines the document embeddings as well as query embeddings"""

    def __init__(self):

        self.model = SentenceTransformer(settings.embedding_model)

        self.index = None
        self.document = None

    def embed_doc(self,texts:list[str]):

        return self.model.encode(
            texts,normalize_embeddings=True
        )

    def embed_query(self,query:str):

        return self.model.encode(
            [query],normalize_embeddings=True
        )[0]