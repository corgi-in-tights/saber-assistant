import json
import logging
import os
from pathlib import Path
from typing import Any

import anyio

INTENTS_DIR = os.environ.get("INTENTS_DIR", "config/intents")
logger = logging.getLogger("saber")


async def load_json_file(filepath: str) -> dict[str, Any] | None:
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


async def fetch_flattened_intents(base_dir: str) -> dict:
    result = {}
    base_dir = Path(base_dir).resolve()

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith("_desc.json"):
                continue

            if file.endswith(".json"):
                abs_path = Path(root) / file
                rel_path = os.path.relpath(abs_path, base_dir)
                # Remove .json extensions yk
                dotted_key = rel_path.replace(os.sep, ".")
                if "." in dotted_key:
                    dotted_key = ".".join(dotted_key.split(".")[:-1])
                try:
                    intent_data = await load_json_file(str(abs_path))
                    if intent_data:
                        result[dotted_key] = intent_data.get("description", "")
                except (OSError, json.JSONDecodeError):
                    logger.exception("Failed to load %s", abs_path)
    return result


async def build_category_tree(base_dir: str) -> dict:
    base_dir = Path(base_dir).resolve()

    async def recurse(current_path: str) -> dict:
        tree = {}
        try:
            for entry in os.scandir(current_path):
                if entry.is_dir():
                    name = entry.name
                    desc_file = Path(entry.path) / "_category.json"
                    children = await recurse(entry.path)
                    if desc_file.exists():
                        desc_data = await load_json_file(desc_file)
                        description = desc_data.get("description", "") if desc_data else ""
                    else:
                        description = ""
                    tree[name] = {"description": description, "children": children}
        except OSError:
            logger.exception("Error reading directory %s", current_path)
        return tree

    return await recurse(base_dir)

class FilesStore:
    flattened_intents = None
    category_tree = None

async def refresh_files_store():
    """Refresh the files store with the latest intents and categories."""
    logger.debug("Refreshing files store...")
    FilesStore.flattened_intents = await fetch_flattened_intents(INTENTS_DIR)
    FilesStore.category_tree = await build_category_tree(INTENTS_DIR)
    logger.debug("Files store refreshed successfully.")

async def get_flattened_intents() -> dict:
    """Get the flattened intents."""
    if not FilesStore.flattened_intents:
        await refresh_files_store()
    return FilesStore.flattened_intents

async def get_category_tree() -> dict:
    """Get the category tree."""
    if not FilesStore.category_tree:
        await refresh_files_store()
    return FilesStore.category_tree
