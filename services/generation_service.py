from services.llm_service import LLMService

class GenerationService:

    def __init__(self):
        self.llm = LLMService()

    def generate_answer(self, query: str, documents):

        context_parts = []

        for document, _ in documents:
            context_parts.append(
                f"Source: {document.metadata.get('source')}\n"
                f"Page: {document.metadata.get('page')}\n"
                f"Content: {document.page_content}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an enterprise knowledge base assistant.

Answer the user's question using ONLY the provided context.

If the answer is not present in the context, say:
"I don't have enough information in the provided documents."

Do not invent facts.

User question:
{query}

Context:
{context}

Provide a concise and accurate answer.
"""

        return self.llm.generate(prompt)