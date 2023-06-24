import dotenv
import os
dotenv.load_dotenv()

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    'safety_settings': [
        {"category":"HARM_CATEGORY_DEROGATORY","threshold":1},
        {"category":"HARM_CATEGORY_TOXICITY","threshold":1},
        {"category":"HARM_CATEGORY_VIOLENCE","threshold":2},
        {"category":"HARM_CATEGORY_SEXUAL","threshold":2},
        {"category":"HARM_CATEGORY_MEDICAL","threshold":2},
        {"category":"HARM_CATEGORY_DANGEROUS","threshold":2}
    ],
}

SESSION_HEADERS = {
    "accept" : "application/json",
    "content-type" : "application/json",
    "x-api-key" : os.getenv("HYEGEN_API_KEY")
}