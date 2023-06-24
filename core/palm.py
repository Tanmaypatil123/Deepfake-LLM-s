import os
import dotenv
import google.generativeai as palm
from constants import defaults

dotenv.load_dotenv()

class Palm:
    def __init__(self):
        palm.configure(api_key=os.getenv("PALM_API_KEY"))
        
    def generate(prompt:str):
        response = palm.generate_text(
            **defaults,
            prompt=prompt
        )
        return response.result
