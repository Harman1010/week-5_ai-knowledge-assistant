from google import genai

from utils.config import settings

class LLMService:

    """This function only has to generate whatever the prompt is given, according to any LLM SDK we use"""

    def __init__(self):

        self.client = genai.Client(
            api_key = settings.gemini_api_key
        )

    def generate(self,prompt:str):

        response = self.client.models.generate_content(
            model = settings.model_name,
            contents = prompt
        )

        return response.text