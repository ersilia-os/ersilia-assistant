import os
import requests
import json

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def read_models():
    with open(os.path.join(DATA_DIR, "ersilia-models.txt"), "r") as f:
        models = f.readlines()
    return models


def read_metadata(model):
    METADATA_FILE_URL = (
        f"https://raw.githubusercontent.com/ersilia-os/{model}/main/metadata.json"
    )
    response = requests.get(METADATA_FILE_URL)
    print(response.status_code)
    if response.status_code != 200:
        return None
    return response.json()


def store_metadata(metadata, model):
    with open(os.path.join(DATA_DIR, "models-metadata", f"{model}.json"), "w") as f:
        json.dump(metadata, f, indent=4)


def run():
    models = read_models()

    for mdl in models:
        print("Processing model:", mdl)
        metadata = read_metadata(mdl.strip())
        store_metadata(metadata, mdl.strip())


if __name__ == "__main__":
    run()
