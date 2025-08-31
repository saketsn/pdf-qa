import os
import requests
import json

# Replace with the actual model you want to test
# Change the model here
API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_TOKEN:
    print("Error: HF_API_TOKEN environment variable is not set.")
else:
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": "The answer to the universe is"}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raises an HTTPError if the response was an error
        
        print(f"Status Code: {response.status_code}")
        print("API Call Successful! The API is working correctly.")
        print("Response:", response.json())
        
    except requests.exceptions.HTTPError as e:
        print(f"API Call Failed with an HTTP error: {e}")
        print("Please check your token or your internet connection.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")