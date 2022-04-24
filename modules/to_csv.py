import csv
from typing import List


def save_table(file_name: str, headers: List[str], rows: List[any]):
    with open(file_name, "w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
