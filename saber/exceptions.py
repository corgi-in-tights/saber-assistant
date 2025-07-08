class ClassNotFoundInModuleError(ImportError):
    def __init__(self, class_name, module_name):
        msg = f"Class '{class_name}' not found in module '{module_name}'"
        super().__init__(msg)
