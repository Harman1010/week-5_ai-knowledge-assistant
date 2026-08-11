from pathlib import Path

from rag.ingestion import document_ingestion, chunking
from rag.retrieval import RetrievalPipeline
from services.generation_service import GenerationService

from rag.guardrails import Guardrails


class KnowledgeService:

    def __init__(self):
        self.retrieval = RetrievalPipeline()
        self.generation = GenerationService()
        self.ready = False
        self.guardrails = Guardrails()

    def ingest(self, file_path: str):

        documents = document_ingestion(file_path)
        chunks = chunking(documents)

        self.retrieval.build(chunks)

        self.ready = True

        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "source": Path(file_path).name,
        }

    def ask(self, query: str, include_retrieval : bool = False, generate_answer : bool = False):

        self.guardrails.input_validate(query)

        if not self.ready:
            raise RuntimeError(
                "Knowledge base has not been initialized."
            )

        results = self.retrieval.retrieve(query)

        self.guardrails.retrieval_validate(results)

        ans = None

        if generate_answer:

            answer = self.generation.generate_answer(
                query,
                results
            )

            self.guardrails.grounding_validate(answer)

        sources = []

        for document, _ in results:
            sources.append({
                "source": document.metadata.get("source", ""),
                "page": document.metadata.get("page", 0),
            })

        response =  {
            "answer": answer,
            "sources": sources,
        }

        if include_retrieval:

            response["retrieved_documents"] = results

        return response

