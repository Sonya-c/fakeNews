
import pandas as pd


def table(data_file: str, title: str):
    data = pd.read_csv(data_file, encoding='unicode_escape')  # Get the data
    print(F"TABLE: {title}")

    # more options can be specified also
    with pd.option_context('display.max_rows', None):
        # Display all the information
        print(data)


def visualizate():
    table("./data/data.csv", "raw data")
