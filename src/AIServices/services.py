import requests
import numpy as np

# Endpoint URL

server_url = 'http://10.24.105.32:4245/tokenize'
test_url = 'http://10.24.18.15:4245/tokenize'


def get_sentences_encoding(sentences: list[str], url=None) -> np.array:
    if not all(isinstance(s, str) for s in sentences):
        raise TypeError("Input must be a list of strings.")
    # Input data
    if url is None:
        url = server_url
    data = {
        'sentences': sentences
    }

    # Send POST request
    response = requests.post(url, json=data)

    # Check the response status code
    if response.status_code == 200:
        # Extract the response JSON data
        response_data = response.json()

        # Process the response data
        embeddings = response_data['embeddings']
        embeddings = np.array(embeddings)

    else:
        raise Exception(f"'Request failed with status code:', {response.status_code}")
    return embeddings
