from typing import Dict, Tuple, List, Set

import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from modules.to_csv import save_table


def init() -> None:
    """Downloand the resource of nltk
    """
    print("Downloading ntlk resources. This may take a few minutes.")

    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download('averaged_perceptron_tagger')


def get_stop_words() -> Set[str]:
    """
    Get the stop words in english
    """
    stop_words = set(stopwords.words('english'))
    return stop_words


def clean_row(sentence: str, stop_words: Set[str]) -> List[str]:
    """
    Remove the stops words from a sentences
    """
    words_list = word_tokenize(sentence)
    words_list = [w for w in words_list if w.isalnum() and w not in stop_words]

    return words_list


def get_word_type(word_type: Dict[str, int], words_list) -> Dict[str, int]:
    tagged = nltk.pos_tag(words_list)  # tag the words list

    for tag in tagged:  # count the word type
        word_type[tag[1]] = word_type.get(tag[1], 0) + 1

    return word_type


def get_word_count(row: str) -> Dict[str, int]:
    word_count: Dict[str, int] = {}  # Word, count

    for word in row:  # count the word
        word = word.replace(":", "").replace("'", "")

        if word != "":
            word_count[word] = word_count.get(word, 0) + 1  # increment

    return word_count


def merge_dict(d1: Dict[str, int], d2: Dict[str, int]) -> Dict[str, int]:
    for key in d2:
        d1[key] = d2[key] + d1.get(key, 0)

    return d1


def get_max(date: str, word_count: Dict[str, int], word_date: Tuple[str, int]) -> Tuple[str, int]:
    max_word = max(word_count, key=word_count.get)
    max_value = max(word_count.values())

    wd = word_date.get(date, ["", 0])  # Get the word count

    if (max_word == wd[0]):
        max_value += wd[1]
        wd = [max_word, max_value]

    elif (max_value > wd[1]):
        wd = [max_word, max_value]

    return wd


def dict_to_list(d: Dict[str, List[any]]) -> List[any]:
    l = []

    for key in d:
        l.append(
            [key] + d[key]
        )
    return l


def n_grams(ngrams, word_list, n=1):
    temp = zip(*[word_list[i:] for i in range(0, n)])
    ng = [' '.join(ngram) for ngram in temp]

    for ngram in ng:
        ngrams[ngram] = ngrams.get(ngram, 0) + 1

    return ngrams


def sort_dict(d: Dict[any, any]):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))


def analysis(file_folder: str = "exp_1", date: bool = False):
    init()

    word_count: Dict[str, int] = {}  # word, word conuter, date
    # Date, most used word and the date
    word_date: Dict[str, Tuple[str, int]] = {}
    article_date: Dict[str, int] = {}  # Date, number of articles
    word_type: Dict[str, int] = {}  # Word type and the frecuency

    bigram: Dict[str, List[int]] = {}
    trigram: Dict[str, List[int]] = {}

    stop_words = get_stop_words()

    with open(f"./data/{file_folder}/data.csv", newline="") as file:  # open file
        reader = csv.reader(file)
        next(reader, None)  # skip the headers

        for row in reader:
            if (row == []):
                continue  # skips the empy rows
            word_list = clean_row(row[0], stop_words)

            bigram = n_grams(bigram, word_list, 2)
            trigram = n_grams(trigram, word_list, 3)

            word_type = get_word_type(word_type, word_list)

            wc: Dict[str, int] = get_word_count(word_list)
            word_count = merge_dict(word_count, wc)

            if not date: continue  # If there's no date register, continue

            date: str = row[1]  # get the year-month-day

            if (date != "TIME ERROR"):  # Si la fecha es correcta, añadir un articulo a esta fecha
                article_date[date] = article_date.get(date, 0) + 1
                # Contar la palabra mas usada en esa fecha
                word_date[date] = get_max(date, wc, word_date)

    # print(word_count, word_date, article_date, sep="\n")
    word_count = sort_dict(word_count)
    bigram = sort_dict(bigram)
    trigram = sort_dict(trigram)

    save_table(f"./data/{file_folder}/word_type.csv", ["word_type",
               "count"], list(word_type.items()))
    save_table(f"./data/{file_folder}/word_frecuency.csv", [
               "word", "frecuency"], list(word_count.items()))
    save_table(f"./data/{file_folder}/bigrams.csv", [
               "bigram", "frecuency"], list(bigram.items()))
    save_table(f"./data/{file_folder}/trigrams.csv", [
               "trigram", "frecuency"], list(trigram.items()))

    if not date: return

    save_table(f"./data/{file_folder}/word_date.csv", [
               "date", "word", "frecuency"], dict_to_list(word_date))
    save_table(f"./data/{file_folder}/article_date.csv", [
               "date", "articles"], list(article_date.items()))
