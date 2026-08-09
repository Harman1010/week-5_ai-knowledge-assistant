from services.llm_service import LLMService

class QueryTransform:

    def __init__(self):

        self.llm = LLMService()

    def multi_query(self,query:str,num:int = 3):

        """Generates multiple queries for a single query by rephrasing while retaining original meaning"""

        prompt = f"""

            Generate {num} alternate queries for the given query.

            Preserve original meaning.

            Do no answer the question

            User question:
            {query}

            Return one query per line.

    """

        response = self.llm.generate(prompt)

        queries = [

            line.strip()
            for line in response.splitlines()
            if line.strip()
        ]

        return queries[:num]