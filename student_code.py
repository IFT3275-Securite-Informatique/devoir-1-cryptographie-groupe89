import requests
from collections import Counter
import random

def decrypt(C):
    C = getEightBitString(C)
    cypherSymbolFrequency = getFrequency(C)
    return print(hill_climb(sorted_combined_frequencies, cypherSymbolFrequency, M, C))

def cut_string_into_pairs(text):
    pairs = []
    for i in range(0, len(text) - 1, 2):
        pairs.append(text[i:i + 2])
    if len(text) % 2 != 0:
        pairs.append(text[-1] + '_')
    return pairs

def load_text_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading the text: {e}")
        return None

def getEightBitString(cypher):
    return [cypher[i:i + 8] for i in range(0, len(cypher), 8)]

def getFrequency(cypher):
    frequency = Counter(cypher)
    total = len(cypher)
    ratio = {char: frequency[char] / total for char in frequency}
    ratio = sorted(ratio.items(), key=lambda item: item[1], reverse=True)
    return ratio


def apply_key(key, C):
    print(C)
    reversed_key = {v: k for k, v in key.items()}
    decrypted_characters = []
    for symbol in C:
        mapped_char = reversed_key.get(symbol, '?')  # Retrieve the mapped character, or '?' if not found
        # Debug: Print each symbol and its corresponding mapped character
        decrypted_characters.append(mapped_char)
    decrypted_text = ''.join(decrypted_characters)  # Concatenate all characters
    return decrypted_text


def score(decypher, corpus):
    # Split the deciphered text into words by whitespace
    words_in_text = decypher.split()
    
    # Initialize the score
    score = 0

    # Check each word in the decyphered text
    for word in words_in_text:
        # Increment score if the word exists in the French dictionary
        if word.lower() in corpus:
            score += 1

    return score


def hill_climb(frequencies, cypherSymbols,corpus, C, iterations=100000):
    symbols = [symbol for symbol, _ in frequencies]
    cypherSymbols_sorted = [symbol for symbol, _ in cypherSymbols]
    best_key = dict(zip(symbols, cypherSymbols_sorted))
    best_score = score(apply_key(best_key, C), corpus)
    for i in range(iterations):
        new_key = best_key.copy()
        # Randomly select two symbols for swapping
        s1, s2 = random.sample(symbols, 2)
        # Swap values in new_key if both symbols exist in new_key
        if s1 in new_key and s2 in new_key:
            new_key[s1], new_key[s2] = new_key[s2], new_key[s1]
            # Apply the new key to the cipher and calculate the score
            decypher = apply_key(new_key, C)
            current_score = score(decypher, corpus)
            # If the new key improves the score, update best_key and best_score
            if current_score > best_score:
                best_key, best_score = new_key, current_score
                print(f"New best score: {best_score}")

    # Return the deciphered text by applying the best key to the cipher
    deciphered_text = ''.join(apply_key( best_key, C))
    return deciphered_text

urls = [
    "https://www.gutenberg.org/ebooks/13846.txt.utf-8",
    "https://www.gutenberg.org/ebooks/4650.txt.utf-8"
    "https://www.gutenberg.org/cache/epub/72024/pg72024.txt"
    "https://www.gutenberg.org/cache/epub/34648/pg34648.txt"
]

text = ""
for url in urls:
    content = load_text_from_web(url)
    if content:
        text += content


if text:
    caracteres = list(set(text))
    nb_caracteres = len(caracteres)
    nb_bicaracteres = 256 - nb_caracteres
    bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
    symboles = caracteres + bicaracteres
    nb_symboles = len(symboles)
    
    total_characters = len(text)
    total_bi_characters = len(cut_string_into_pairs(text))
    character_frequencies = Counter(text)
    bi_character_frequencies = Counter(cut_string_into_pairs(text))
    
    combined_frequencies = {char: character_frequencies[char] / total_characters for char in caracteres}
    combined_frequencies.update({bi_char: bi_character_frequencies[bi_char] / total_bi_characters for bi_char in bicaracteres})
    sorted_combined_frequencies = sorted(combined_frequencies.items(), key=lambda item: item[1], reverse=True)
    

else:
    print("Failed to load text from all sources.")

def gen_key(symboles):
    random.seed(1337)
    l = len(symboles)
    if l > 256:
        return False

    int_keys = random.sample(list(range(l)), l)
    dictionary = {s: "{:08b}".format(k) for s, k in zip(symboles, int_keys)}
    return dictionary

dictionaire = gen_key(symboles)


def M_vers_symboles(M, K):
    encoded_text = []
    i = 0

    while i < len(M):
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in K:
                encoded_text.append(pair)
                i += 2
                continue

        if M[i] in K:
            encoded_text.append(M[i])
        else:
            encoded_text.append(M[i])
        i += 1

    return encoded_text

def chiffrer(M, K):
    l = M_vers_symboles(M, K)
    l = [K[x] for x in l]
    return ''.join(l)

M = text[2000:10000]
