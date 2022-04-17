from typing import Dict, Tuple, List
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import nltk


def save_table(file_name: str, headers: List[str], rows: List[any]):
    with open("data/" + file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def analysis():
    word_count: Dict[str, int] = {}  # word, word conuter, date

    # Dic of date. Each has a dict of word counts
    word_date: Dict[str, Dict[str, int]] = {}

    article_date: Dict[str, int] = {}

    word_type: Dict[str, int] = {}

    # get the stopwords
    nltk.download("stopwords")
    stop_words = set(stopwords.words('english'))

    with open("./data/data.csv", newline="") as file:  # open file
        reader = csv.reader(file)
        next(reader, None)  # skip the headers

        for row in reader:
            if (row == []):
                continue  # skips the empy rows

            date: str = row[1][:10]  # get the year-month-day
            if (date != "ERROR"):
                article_date[date] = article_date.get(date, 0) + 1

            for word in row[0].split(" "):
                word = word.replace(":", "").replace("'", "")

                if word not in stop_words and word != "":  # Ignore the stops words
                    word_count[word] = word_count.get(word, 0) + 1  # increment

                    if (date != "ERROR"):
                        wd = word_date.get(date, dict())
                        wd[word] = wd.get(word, 0) + 1
                        word_date[date] = wd

    print(word_count, word_date, article_date, sep="\n")

    save_table("word_frecuency.csv", [
               "word", "frecuency"], list(word_count.items()))

    save_table("word_date.csv", [
               "date", "words"], list(word_date.items()))

    save_table("article_date.csv", [
        "date", "words"], list(article_date.items()))
