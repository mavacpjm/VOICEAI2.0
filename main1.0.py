import requests
import json
import tempfile
import os
from gtts import gTTS
import pygame

def fetch_response_from_api(prompt):
    api_url = "http://localhost:11434/api/generate"  # Replace with the actual API URL
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API Key
        "Content-Type": "application/json",
    }
    payload = {
        "question": prompt,
    }

    try:
        response = requests.post(api_url, json={"model": "tinyllama", "stream": False, "prompt": prompt}, stream=True)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error occurred: {http_err.response.text}"
    except Exception as err:
        return f"An error occurred: {err}"

    try:
        response_lines = response.text.splitlines()
        complete_response = ""
        for line in response_lines:
            json_response = json.loads(line)
            complete_response += json_response.get('response', '')
            if json_response.get('done', False):
                break
        return complete_response
    except json.JSONDecodeError:
        return "Error processing one of the response lines."

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(temp_file.name)
    temp_file.close()
    
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file.name)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    os.unlink(temp_file.name)

def main():
    while True:
        prompt = input("Ask a question (or type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        response = fetch_response_from_api(prompt)
        print("Response:", response)
        text_to_speech(response)

if __name__ == "__main__":
    main()