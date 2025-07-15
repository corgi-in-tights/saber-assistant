import inspect
import logging
import os

from .intents import build_intents_tree
from .intents import flatten_tree_into_templates
from .lazy_list import load_lazy_list_into_dict
from .lazy_list import load_lazy_list_into_list

CLASSIFIERS_PATH = os.environ.get("CLASSIFIERS_PATH", "config/intent_classifiers.json")
INTENTS_DIR = os.environ.get("INTENTS_DIR", "config/intents")
CONTEXT_PROVIDERS_PATH = os.environ.get("CONTEXT_PROVIDERS_DIR", "config/context_providers.json")
SKILLS_PATH = os.environ.get("SKILLS_DIR", "config/skills.json")


logger = logging.getLogger("saber")

class ConfigsStore:
    def __init__(self):
        self.configs = {}

    def set_data(self, config_name: str, config_data: dict) -> dict:
        """
        Load a configuration into the store.
        :param config_name: The name of the configuration.
        :param config_data: The configuration data as a dictionary.
        """
        self.configs[config_name] = config_data

    def get_data(self, config_name: str) -> dict:
        """
        Retrieve a configuration from the store.
        :param config_name: The name of the configuration to retrieve.
        :return: The configuration data as a dictionary.
        """
        return self.configs.get(config_name, {})

    def reset_data(self, config_name: str):
        """
        Reset a configuration in the store.
        :param config_name: The name of the configuration to reset.
        """
        if config_name in self.configs:
            del self.configs[config_name]

    async def load_config(self, key: str, method, *args, **kwargs):
        """
        Load the configuration asynchronously from the config store.
        This function should be called at startup to initialize the configuration.
        """
        key_config_data = self.get_data(key)
        if not key_config_data:
            if inspect.iscoroutinefunction(method):
                data = await method(*args, **kwargs)
            else:
                data = method(*args, **kwargs)

            self.set_data(key, data)
            return data

        return key_config_data

configs_store = ConfigsStore()

def get_config(x):
    return configs_store.get_data(x)

async def initialize_configs():
    """
    Initialize all configurations at startup.
    This function should be called once during the ap plication startup.
    """
    logger.info("Initializing configurations...")

    config_items = [
        ("intent_classifiers", load_lazy_list_into_list, CLASSIFIERS_PATH),
        ("context_providers", load_lazy_list_into_dict, CONTEXT_PROVIDERS_PATH),
        ("skills", load_lazy_list_into_dict, SKILLS_PATH),
    ]
    for key, method, path in config_items:
        await configs_store.load_config(key, method, path)

    intent_tree = await build_intents_tree(INTENTS_DIR)
    logger.debug("Intent tree built: %r", intent_tree)
    configs_store.set_data("intent_tree", intent_tree)

    intent_templates = await flatten_tree_into_templates(intent_tree, INTENTS_DIR)
    logger.debug("Intent templates generated: %r", intent_templates)
    configs_store.set_data("intent_templates", intent_templates)

    logger.info("All configurations loaded successfully.")

