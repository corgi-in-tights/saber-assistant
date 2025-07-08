from .utils import lazy_import_class_by_path
from .utils import load_json_file_async


async def load_lazy_list_into_dict(filepath: str) -> list:
    """
    Load a lazy list from a JSON file asynchronously.
    :param filepath: The path to the JSON file.
    :return: The loaded list.
    """
    data = await load_json_file_async(filepath)
    imported_dict = {}

    for item in data:
        if isinstance(item, dict) and "name" in item and "path" in item:
            imported_data = {
                "class": lazy_import_class_by_path(item["path"]),
                "kwargs": item.get("kwargs", {}),
            }
            # get the important stuff and add remaining data if there is any
            imported_data.update({k: v for k, v in item.items() if k not in ["name", "path", "kwargs"]})

            imported_dict[item["name"]] = imported_data
        else:
            msg = f"Invalid item format in lazy list {filepath}: {item}"
            raise ValueError(msg)

    return imported_dict

async def load_lazy_list_into_list(filepath: str) -> list:
    """
    Load a lazy list from a JSON file asynchronously.
    :param filepath: The path to the JSON file.
    :return: The loaded list.
    """
    data = await load_json_file_async(filepath)
    imported_list = []

    for item in data:
        if isinstance(item, dict) and "name" in item and "path" in item:
            item["class"] = lazy_import_class_by_path(item["path"])
            del item["path"]
            imported_list.append(item)
        else:
            msg = f"Invalid item format in lazy list {filepath}: {item}"
            raise ValueError(msg)

    return imported_list
