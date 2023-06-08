import numpy
import string
import requests
import numpy as np

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


def sentences_dot_product(sentences_matrix1: numpy, sentences_matrix2: numpy):
    """
    calculate similarity between matrix 1 and matrix 2
    :param: sentences_matrix1 numpy matrix (no_sentences,features_dim)
    :param: sentences_matrix2: numpy matrix (no_sentences,features_dim)
    :return: dot product similarity between sentences of matrix 1 with matrix 2
    """
    assert sentences_matrix1.shape[1] == sentences_matrix2.shape[1]
    return np.dot(sentences_matrix1, np.transpose(sentences_matrix2))


def sentences_cosine_similarity(sentences_matrix1: numpy, sentences_matrix2: numpy):
    """
    calculate similarity between matrix 1 and matrix 2
    :param: sentences_matrix1 numpy matrix (no_sentences,features_dim)
    :param: sentences_matrix2: numpy matrix (no_sentences,features_dim)
    :return: cosine similarity between sentences of matrix 1 with matrix 2
    """

    similarity_dot_prod_mat = sentences_dot_product(sentences_matrix1, sentences_matrix2)
    sentences_matrix1_mag = np.linalg.norm(sentences_matrix1, axis=1)
    sentences_matrix2_mag = np.linalg.norm(sentences_matrix2, axis=1)
    magnitudes_matrix = np.expand_dims(sentences_matrix1_mag, axis=1) * sentences_matrix2_mag.reshape(1, -1)
    similarity_cos_mat = similarity_dot_prod_mat / magnitudes_matrix

    return similarity_cos_mat  # %%


def get_topk(np_array: numpy, k=10):
    sorted_indices = np.argsort(np_array)[::-1]
    return sorted_indices[:k + 1]


def clean_txt(txt: str, to_lower=False, strip=False, all_except=None):
    if all_except is not None:
        punc_set = set([c for c in string.punctuation if c not in all_except])
    else:
        punc_set = set([c for c in string.punctuation])
    new_txt = []
    for char in txt:
        if char not in punc_set:
            if to_lower:
                new_txt.append(char.lower())
            else:
                new_txt.append(char)
    if strip:
        start = 0
        end = None
        if new_txt[0] == ' ':
            start = 1
        if new_txt[-1] == ' ':
            end = -1

        if end is None:
            new_txt = new_txt[start:]
        else:
            new_txt = new_txt[start:end]

    return "".join(new_txt)
