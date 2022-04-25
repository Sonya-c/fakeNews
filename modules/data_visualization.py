from typing import List
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def word_graph(fig_num: int = 1, fig_title: str = "", data: List[any] = []):
    """Analisis de palabras
    """

    fig = plt.figure(fig_num)
    fig.canvas.set_window_title(
        f"Figura {fig_num}: {fig_title}")
    grid_spec = GridSpec(4, 3)
    grid_spec.update(wspace=0.4, hspace=0.8)

    ax1 = fig.add_subplot(grid_spec[:2, :2])  # Frecuencia de palabras
    ax1.set_title("Las 10 palabras más usadas")
    sns.barplot(x=data[0].word, y=data[0].frecuency, ax=ax1)

    ax2 = fig.add_subplot(grid_spec[2:, :2])  # tipos de palabra
    ax2.set_title("Tipos de palabras")
    sns.barplot(data=data[1], x="word_type", y="count", ax=ax2)

    ax3 = fig.add_subplot(grid_spec[:1, 2:])  # bigramas
    ax3.set_title("10 Bigramas más comunes")
    ax3.tick_params(rotation=45)
    sns.barplot(data=data[2], x="bigram", y="frecuency", ax=ax3)

    ax4 = fig.add_subplot(grid_spec[2, 2:])  # trigramas
    ax4.set_title("10 Trigramas más comunes")
    ax4.tick_params(rotation=45)
    sns.barplot(data=data[3], x="trigram", y="frecuency", ax=ax4)

    fig.suptitle(fig_title, fontsize=16)


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
                      colLabels=data[0].columns, loc='center')

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
    exp1_raw_data = pd.read_csv(
        "./data/exp_1/data.csv", encoding="unicode_escape")
    exp1_word_frecuency = pd.read_csv(
        "./data/exp_1/word_frecuency.csv", encoding='unicode_escape')
    exp1_word_type_frecuency = pd.read_csv(
        "./data/exp_1/word_type.csv", encoding='unicode_escape')
    mode_per_date = pd.read_csv(
        "./data/exp_1/word_date.csv", encoding='unicode_escape')
    articles_per_date = pd.read_csv(
        "./data/exp_1/article_date.csv", encoding='unicode_escape')
    exp1_bigrams = pd.read_csv(
        "./data/exp_1/bigrams.csv", encoding='unicode_escape')
    exp1_trigrams = pd.read_csv(
        "./data/exp_1/trigrams.csv", encoding='unicode_escape')

    exp2_raw_data = pd.read_csv(
        "./data/exp_2/data.csv", encoding="unicode_escape")
    exp2_word_frecuency = pd.read_csv(
        "./data/exp_2/word_frecuency.csv", encoding='unicode_escape')
    exp2_word_type_frecuency = pd.read_csv(
        "./data/exp_2/word_type.csv", encoding='unicode_escape')
    exp2_bigrams = pd.read_csv(
        "./data/exp_2/bigrams.csv", encoding='unicode_escape')
    exp2_trigrams = pd.read_csv(
        "./data/exp_2/trigrams.csv", encoding='unicode_escape')

    print_table(exp1_raw_data, "Datos sin procedar")
    print_table(exp2_raw_data, "Titulares generados")

    word_graph(
        fig_title="Análisis de palabras (de los articulos obtenidos)",
        data=[
            exp1_word_frecuency[:10],  # is this sorted?
            exp1_word_type_frecuency,
            exp1_bigrams[:10],
            exp1_trigrams[:10]
        ]
    )

    articles_graph([
        mode_per_date,
        articles_per_date
    ])

    word_graph(
        fig_num=3,
        fig_title="Análisis de palabras (de los titulares generados)",
        data=[
            exp2_word_frecuency[:10],  # is this sorted?
            exp2_word_type_frecuency,
            exp2_bigrams[:5],
            exp2_trigrams[:5]
        ]
    )

    plt.show()
