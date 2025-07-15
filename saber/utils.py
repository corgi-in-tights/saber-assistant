import json
from pathlib import Path


def load_json_file(filepath: str) -> dict:
    """
    Load a JSON file synchronously.
    :param filepath: The path to the JSON file.
    :return: The loaded JSON data as a dictionary.
    """
    with Path(filepath).open("r") as fp:
        return json.load(fp)
