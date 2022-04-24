import csv
from typing import List, Tuple
import random

from numpy import save
from modules.to_csv import save_table


def get_next(next_words):
    total = sum(w for _, w in next_words)
    rand = random.uniform(0, total)  # rand number frm uniform distribution
    cumulative = 0  # Cumulative frecuency

    for next_word, frecuency in next_words:
        cumulative += frecuency

        if cumulative > rand:
            return next_word[1]


def generate_sentence(n_gram, start_word, n=50) -> List[str]:
    sentence: str = start_word

    for _ in range(n):
        next_words = [word for word in n_gram if word[0][0] == start_word]

        if not next_words:
            break

        start_word = get_next(next_words).replace(" ", "")

        if (start_word != ""):
            sentence += " " + start_word

    return sentence


def get_data(file_name: str) -> List[str]:
    data: List[str] = []

    with open(f"data/exp_1/{file_name}", "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip the headers

        for row in reader:
            data.append(row)

    return data


def generate():
    bigrams = [(tuple(row[0].split(" ")), int(row[1]))
               for row in get_data("bigrams.csv")]
    words = [row[0] for row in get_data("word_frecuency.csv")]

    sentences: List[str] = []
    i: int = 0
    j: int = 0
    while (j <= 30 and i < len(words)):
        sentence = generate_sentence(bigrams, words[i], 20)

        if (len(sentence.split(" ")) > 3):
            sentences.append([sentence])
            j += 1

        i += 1

    save_table("./data/exp_2/data.csv", ["title"], sentences)
