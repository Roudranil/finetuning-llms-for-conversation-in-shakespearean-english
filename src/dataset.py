import json
import os

from tqdm import tqdm
import pandas as pd


DATA_DIR = "../raw-data"
EXPORT_DIR = "../processed-data"


def format_data(data, book, chapter):
    new_data = {
        "id": [],
        "translated_dialog": [],
        "og_response": [],
    }
    for i, (current_row, next_row) in enumerate(zip(data, data[1:])):
        id = f"{book}-{chapter}-line-{i}"
        new_data["id"].append(id)
        new_data["translated_dialog"].append(current_row["translated"])
        new_data["og_response"].append(next_row["original"])
    return new_data


def data_dict_merge(old_dict, new_dict):
    for k in old_dict.keys():
        old_dict[k].extend(new_dict[k])
    return old_dict


def build_book_dataset(book):
    chapter_names = os.listdir(os.path.join(DATA_DIR, book))
    inner_loop = tqdm(chapter_names, position=1, leave=False, desc=f"==> Book {book}")
    book_data = {
        "id": [],
        "translated_dialog": [],
        "og_response": [],
    }
    for chapter in inner_loop:
        with open(os.path.join(DATA_DIR, book, chapter), "r") as f:
            data = json.load(f)["dialogs"]
        formatted_data = format_data(data, book, chapter)
        book_data = data_dict_merge(book_data, formatted_data)

    return book_data


def main():
    book_names = os.listdir(DATA_DIR)
    outer_loop = tqdm(book_names, position=0, leave=False)
    for book in outer_loop:
        book_data = build_book_dataset(book)
        book_df = pd.DataFrame.from_dict(book_data, orient="columns")
        book_df.to_csv(os.path.join(EXPORT_DIR, f"{book}.csv"), index=False)


if __name__ == "__main__":
    main()
