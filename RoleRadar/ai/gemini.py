from django.conf import settings
from google import genai


global_gemini_client = genai.Client(api_key=settings.GEMINI_TOKEN)


def fetch_gemini_response(prompt_content):
    try:
        api_result = global_gemini_client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt_content
        )
        return api_result.text
    except Exception as e:
        print(e)
        return "Please try again later."

