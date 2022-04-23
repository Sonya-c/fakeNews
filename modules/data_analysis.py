from typing import Dict, Tuple, List
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import csv
import nltk


def init():
    print("Downloading ntlk resources. This may take a few minutes.")
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download('averaged_perceptron_tagger')


def get_stop_words() -> List[str]:
    # get the stopwords
    
    stop_words = set(stopwords.words('english'))
    return stop_words


def clean_row(sentence: str, stop_words):
   #  tokenized = sent_tokenize(sentence)
    tokenizer = nltk.RegexpTokenizer(r"\w+")

    words_list = word_tokenize(sentence)
    words_list = [w for w in words_list if w.isalnum() and not w in stop_words]

    return words_list


def get_word_type(word_type: Dict[str, int], words_list) -> Dict[str, int]:
    tagged = nltk.pos_tag(words_list)
    
    for tag in tagged:
        word_type[tag[1]] = word_type.get(tag[1], 0) + 1

    return word_type


def get_word_count(row: str) -> Dict[str, int]:
    word_count: Dict[str, int] = {}  # Word, count

    for word in row:
        word = word.replace(":", "").replace("'", "")

        if  word != "": 
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


def save_table(file_name: str, headers: List[str], rows: List[any]):
    with open("data/" + file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def analysis():
    init()
    word_count: Dict[str, int] = {}  # word, word conuter, date
    word_date: Dict[str, Tuple[str, int]] = {}  # Date, most used word and the date
    article_date: Dict[str, int] = {}  # Date, number of articles
    word_type: Dict[str, int] = {}  # Word type and the frecuency

    stop_words = get_stop_words()

    with open("./data/data.csv", newline="") as file:  # open file
        reader = csv.reader(file)
        next(reader, None)  # skip the headers

        for row in reader:
            if (row == []): continue  # skips the empy rows
            word_list = clean_row(row[0], stop_words)

            word_type = get_word_type(word_type, word_list)

            wc: Dict[str, int] = get_word_count(word_list)
            word_count = merge_dict(word_count, wc)

            date: str = row[1][:10]  # get the year-month-day

            if (date != "ERROR"):  # Si la fecha es correcta, añadir un articulo a esta fecha
                article_date[date] = article_date.get(date, 0) + 1
                word_date[date] = get_max(date, wc, word_date)  # Contar la palabra mas usada en esa fecha
            
    # print(word_count, word_date, article_date, sep="\n")

    save_table("word_type.csv", ["word type", "count"], list(word_type.items()))
    save_table("word_frecuency.csv", ["word", "frecuency"], list(word_count.items()))
    save_table("word_date.csv", ["date", "words", "frecuency"], list(word_date.items()))
    save_table("article_date.csv", ["date", "words"], list(article_date.items()))