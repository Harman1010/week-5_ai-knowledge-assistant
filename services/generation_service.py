from services.llm_service import LLMService


class GenerationService:

    def __init__(self):
        self.llm = LLMService()

    def generate_answer(self, query: str, documents):

        context_parts = []

        for document, score in documents:
            context_parts.append(
                f"""
Source: {document.metadata.get("source")}
Page: {document.metadata.get("page")}

Content:
{document.page_content}
"""
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an enterprise knowledge base assistant.

Your task is to answer the user's question using the provided
document context.

IMPORTANT RULES:
1. Use the provided context as the source of truth.
2. Do not use outside knowledge.
3. If the answer is explicitly present in the context, answer it.
4. Only say "I don't have enough information in the provided documents"
   if the context genuinely does not contain the answer.
5. Do not assume that the user's wording must exactly match the wording
   in the document.
6. Give a concise answer.

USER QUESTION:
{query}

DOCUMENT CONTEXT:
{context}

ANSWER:
"""

        return self.llm.generate(prompt)