import json
import os

from tqdm import tqdm
import pandas as pd

from sklearn.model_selection import train_test_split


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
    complete_dataset = {
        "id": [],
        "translated_dialog": [],
        "og_response": [],
    }
    book_names = os.listdir(DATA_DIR)
    outer_loop = tqdm(book_names, position=0, leave=False)
    for book in outer_loop:
        book_data = build_book_dataset(book)
        complete_dataset = data_dict_merge(complete_dataset, book_data)

    complete_df = pd.DataFrame.from_dict(complete_dataset, orient="columns")
    print(complete_df.iloc[:3, :])
    complete_df_train, complete_df_test = train_test_split(
        complete_df, test_size=0.4, random_state=42
    )
    print(complete_df_train.iloc[:3, :])
    complete_df_train.to_csv(os.path.join(EXPORT_DIR, f"train-v1.csv"), index=False)
    complete_df_test.to_csv(os.path.join(EXPORT_DIR, f"test-v1.csv"), index=False)


if __name__ == "__main__":
    main()
