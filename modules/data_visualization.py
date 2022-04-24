from typing import List
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import textwrap


def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)


def word_graph(data: List[any]):
    """Analisis de palabras
    """

    fig = plt.figure(1)
    fig.canvas.set_window_title(
        "Figura 1: Análisis de palabras (de los articulos obtenidos)")
    grid_spec = GridSpec(4, 3)
    grid_spec.update(wspace=0.4, hspace=0.8)

    ax1 = fig.add_subplot(grid_spec[:2, :2])  # Frecuencia de palabras
    ax1.set_title("Las 10 palabras más usadas")
    sns.barplot(x=data[0].word, y=data[0].frecuency, ax=ax1)

    ax2 = fig.add_subplot(grid_spec[2:, :2])  # tipos de palabra
    ax2.set_title("Tipos de palabras")
    sns.barplot(data=data[1], x="word_type", y="count", ax=ax2)

    ax3 = fig.add_subplot(grid_spec[:2, 2:])  # bigramas
    ax3.set_title("10 Bigramas más comunes")
    wrap_labels(ax3, 5)
    ax3.figure
    sns.barplot(data=data[2], x="bigram", y="frecuency", ax=ax3)

    ax4 = fig.add_subplot(grid_spec[2:, 2:])  # trigramas
    ax4.set_title("10 Trigramas más comunes")
    wrap_labels(ax4, 5)
    ax4.figure
    sns.barplot(data=data[3], x="trigram", y="frecuency", ax=ax4)

    fig.suptitle("Datos de las palabras (de los articulos)", fontsize=16)


def articles_graph(data):
    fig = plt.figure(2)
    fig.canvas.set_window_title("Figura 2: Información de los ariticulos")

    grid_spec = GridSpec(1, 2)
    grid_spec.update(wspace=0.4, hspace=0.8)

    ax1 = fig.add_subplot(grid_spec[0, 0])  # Frecuencia de palabras
    ax1.set_title("Palabra más usada por fecha")
    ax1.axis('off')
    ax1.axis('tight')
    table = ax1.table(cellText=data[0].values,
                      colLabels=data[1].columns, loc='center')

    # modify table
    table.set_fontsize(14)

    ax2 = fig.add_subplot(grid_spec[0, 1])  # frecuencia de articulos
    ax2.set_title("Frecuencia de articulos")
    ax2.tick_params(rotation=45)
    sns.barplot(x=data[1].date, y=data[1].articles, ax=ax2)

    fig.suptitle("Datos de los articulos", fontsize=16)


def print_table(data, title: str):
    print(f"\nTable: {title}")
    with pd.option_context('display.max_rows', None):
        # Display all the information
        print(data)


def visualizate():
    raw_data = pd.read_csv("./data/data.csv", encoding="unicode_escape")
    word_frecuency = pd.read_csv(
        "./data/word_frecuency.csv", encoding='unicode_escape')
    word_type_frecuency = pd.read_csv(
        "./data/Word_type.csv", encoding='unicode_escape')
    mode_per_date = pd.read_csv(
        "./data/word_date.csv", encoding='unicode_escape')
    articles_per_date = pd.read_csv(
        "./data/article_date.csv", encoding='unicode_escape')
    bigrams = pd.read_csv(
        "./data/bigrams.csv", encoding='unicode_escape')
    trigrams = pd.read_csv(
        "./data/trigrams.csv", encoding='unicode_escape')

    print_table(raw_data, "Raw data")

    word_graph([
        word_frecuency[:10],  # is this sorted?
        word_type_frecuency,
        bigrams[:5],
        trigrams[:5]
    ])

    articles_graph([
        mode_per_date,
        articles_per_date
    ])

    plt.show()
