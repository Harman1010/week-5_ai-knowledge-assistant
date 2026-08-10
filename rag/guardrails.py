class GuardrailError(Exception):

    """Raises error when something is wrong"""

class Guardrails():

    def input_validate(self,query:str):

        """Validates incoming queries"""

        if not query or not query.strip():

            raise GuardrailError(
                "Query cannot be empty."
            )

        if len(query) > 1000:

            raise GuardrailError(
                "Query is too long."
            )

        suspecious_patterns = [
            "ignore previous instructions",
            "reveal system prompt",
            "reveal sensitive information"
        ]

        for pattern in suspecious_patterns:

            if pattern in query.lower():

                raise GuardrailError(
                    "Prompt injection detected"
                )

        return True

    def retrieval_validate(self,documents):

        """Check whether the document retrieval is valid or not"""

        if not documents:

            raise GuardrailError(
                "No valid document was found."
            )

        return True

    def grounding_validate(self,answer:str):

        """Check whether the answer is grounded or not"""

        if not answer or not answer.strip():

            raise GuardrailError(
                "Answer cannot be empty."
            )

        return True

