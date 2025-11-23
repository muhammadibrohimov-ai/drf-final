import google.generativeai as genai
from environs import Env
from google import genai
from google.genai import types

env = Env()
env.read_env()

def chatting(request_text):
    
    API_TOKEN = env.str("AIzaSyBoCtAEhsm9xf9nRQoVjc21-Das7S1j64Y")

    genai.configure(api_key=API_TOKEN)

    model = genai.GenerativeModel("gemini-2.0-flash")

    chat = model.start_chat()   
    
    responce = chat.send_message(request_text)
    return responce.text


def work_with_image(path: str, request_text: str):
    
    with open(path, 'rb') as f:
        image_bytes = f.read()

    client = genai.Client(api_key='AIzaSyDasglvAL2Ri8vur0b9hw0IgtViZNmIFSw')
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg',
            ),
            request_text
        ]
    )

    return response.text