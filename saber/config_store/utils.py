import json

import aiofiles

from saber.exceptions import ClassNotFoundInModuleError


def lazy_import_class_by_path(path: str):
    """
    Dynamically import a class by its path.
    :param path: The full path to the class.
    :return: The imported class.
    """
    components = path.split(".")
    module_name = ".".join(components[:-1])
    class_name = components[-1]

    module = __import__(module_name, fromlist=[class_name])
    if not hasattr(module, class_name):
        raise ClassNotFoundInModuleError(class_name, module_name)
    return getattr(module, class_name)


async def load_json_file_async(filepath: str) -> dict:
    """
    Load a JSON file asynchronously.
    :param filepath: The path to the JSON file.
    :return: The loaded JSON data as a dictionary.
    """
    async with aiofiles.open(filepath) as fp:
        content = await fp.read()
        return json.loads(content)
