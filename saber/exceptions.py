class ClassNotFoundInModuleError(ImportError):
    def __init__(self, class_name, module_name):
        msg = f"Class '{class_name}' not found in module '{module_name}'"
        super().__init__(msg)

class InvalidIntentSlotError(Exception):
    def __init__(self, slot_name, intent_name):
        msg = f"Invalid slot '{slot_name}' for intent '{intent_name}'"
        super().__init__(msg)
