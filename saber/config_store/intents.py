import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

import anyio

from saber import SaberIntentTemplate

logger = logging.getLogger("saber")


async def load_json_file_async(filepath: str) -> dict[str, Any] | None:
    try:
        async with await anyio.open_file(filepath, "r") as f:
            content = await f.read()
            if not content.strip():
                logger.warning("File %s is empty", filepath)
                return None

            return json.loads(content)

    except (OSError, json.JSONDecodeError):
        logger.exception("Error reading %s for intents", filepath)
    return None


async def list_dir(path: str) -> list[str]:
    return await asyncio.to_thread(os.listdir, path)


async def walk_subdirectories(parent_path: str, process_fn):
    result = {}
    for entry in await list_dir(parent_path):
        entry_path = Path(parent_path) / entry
        if entry_path.is_dir():
            result[entry] = await process_fn(str(entry_path))
    return result


async def build_intents_tree(base_dir):
    async def process_category(curr_path):
        category = {
            "description": "",
            "intents": [],
            "subcategories": {},
            "context_providers": [],
        }

        # load _category.json if it exists
        category_file = Path(curr_path) / "_category.json"
        if category_file.is_file():
            try:
                data = await load_json_file_async(str(category_file))
                category["description"] = data.get("description", "")
                category["context_providers"] = data.get("context_providers", [])
            except (OSError, json.JSONDecodeError):
                logger.exception("Error loading category %s", curr_path)

        # process intents and subcategories
        for entry in await list_dir(curr_path):
            entry_path = Path(curr_path) / entry
            if entry_path.is_dir():
                continue

            if entry.endswith(".json") and entry != "_category.json":
                category["intents"].append(entry[:-5])

        category["subcategories"] = await walk_subdirectories(curr_path, process_category)

        return category

    return await walk_subdirectories(base_dir, process_category)



async def flatten_tree_into_templates(
    intent_tree: dict,
    base_dir: str,
    prefix: str = "",
    path_prefix: str = "",
) -> dict:
    result = {}

    for category_name, data in intent_tree.items():
        full_prefix = f"{prefix}.{category_name}" if prefix else category_name
        category_path = f"{path_prefix}/{category_name}" if path_prefix else category_name


        for intent in data.get("intents", []):
            # load intent template
            try:
                intent_template_data = await load_json_file_async(f"{base_dir}/{category_path}/{intent}.json")
            except (OSError, json.JSONDecodeError, FileNotFoundError):
                logger.debug("Failed to load intent template for %s", intent)
                continue

            if not intent_template_data:
                logger.debug("Intent template for %s is empty", intent)
                continue

            intent_name_full = f"{full_prefix}.{intent}"
            template = SaberIntentTemplate(
                intent_name_full,
                intent_template_data.get("slots", {}),
                intent_template_data.get("skill", None),
            )

            result[intent_name_full] = template

        # recurse into subcategories
        subcategories = data.get("subcategories", {})
        if subcategories:
            sub_result = await flatten_tree_into_templates(
                subcategories,
                base_dir,
                full_prefix,
                category_path,
            )
            result.update(sub_result)

    return result

# {
#     "timer": {
#         "description": "",
#         "intents": {
#             "start",
#             "stop"
#         },
#         "subcategories": {
            
#         }
#     }
# }

# {
#     "command.device.set": IntentTemplate()
# }

