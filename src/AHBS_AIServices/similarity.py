import string
import requests
import numpy as np

server_url = 'http://10.24.105.160:4245/tokenize'
test_url = 'http://10.24.18.15:4245/tokenize'


def get_sentences_encoding(sentences: list, url=None) -> np.array:
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


def sentences_dot_product(sentences_matrix1: np, sentences_matrix2: np):
    """
    calculate similarity between matrix 1 and matrix 2
    :param: sentences_matrix1 numpy matrix (no_sentences,features_dim)
    :param: sentences_matrix2: numpy matrix (no_sentences,features_dim)
    :return: dot product similarity between sentences of matrix 1 with matrix 2
    """
    assert sentences_matrix1.shape[1] == sentences_matrix2.shape[1]
    return np.dot(sentences_matrix1, np.transpose(sentences_matrix2))


def sentences_cosine_similarity(sentences_matrix1: np, sentences_matrix2: np):
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


def get_topk(np_array: np, k=10):
    sorted_indices = np.argsort(np_array)[::-1]
    return sorted_indices[:k + 1]


def clean_txt(txt: str, to_lower=False, strip=False, all_except=None, replace_with: str = None):
    if txt is None or len(txt) == 0:
        return txt
    txt = str(txt)
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
        elif replace_with:
            new_txt.append(replace_with)

    if len(new_txt) > 0:
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


def get_sentences_similarity(sentence_list_1, sentence_list_2: list = None, sentence_list_2_enc: np = None,
                             get_score=True, keep_special_chars: list = None,
                             url=None) -> list:
    """
    get similarity score between two list of sentences
    :param sentence_list_1: list of strings
    :param sentence_list_2: list of strings
    :param get_score: bool set to true if you want to get the similarity score
    :param keep_special_chars: list of special characters to keep while cleaning the text
    :param url: url to the server of bert-tokenizer ip:port/route
    :return: list of matches [[sent_list_1[i],matched text in list of sent-2,score (optional) ]]
    """
    if url is None:
        url = server_url
    if sentence_list_2 is None and sentence_list_2_enc is None:
        raise Exception("target not passed sentence_list_2 or sentence_list_2_encodings")

    sentence_list_1_prep = [clean_txt(sent, strip=True, to_lower=True, all_except=keep_special_chars) for sent in
                            sentence_list_1]
    sentence_list_1_enc = get_sentences_encoding(sentence_list_1_prep, url)

    if sentence_list_1_enc is None:
        sentence_list_2_prep = [clean_txt(sent, strip=True, to_lower=True, all_except=keep_special_chars) for sent in
                                sentence_list_2]
        sentence_list_2_enc = get_sentences_encoding(sentence_list_2_prep, url)

    similarity_matrix = sentences_cosine_similarity(sentence_list_1_enc, sentence_list_2_enc)

    no_sentences = len(sentence_list_1)

    top_match_result = []
    for sent_idx in range(no_sentences):
        top_sent_idx = get_topk(similarity_matrix[sent_idx], k=1)[0]

        top_match_sent = sentence_list_2[top_sent_idx]
        top_match_score = similarity_matrix[sent_idx, top_sent_idx]
        match_row = [sentence_list_1[sent_idx], top_match_sent]
        if get_score:
            match_row.append(top_match_score)
        top_match_result.append(match_row)
    return top_match_result
