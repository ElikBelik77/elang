class CompileAsPointer:
    """
    Flag for models that are compiled as a pointer.
    The effect of this flag is that variable values are treated as a pointer, and will be dereferenced automatically.
    """
    pass


class CompileAsValue:
    """
    Flag for modelst that are compiled as a pointer.
    The effect of this flag is equivalent for the absence of the CompileAsPointer flag. Variables that are loaded to
    registers won't be automatically dereferenced.
    """
    pass
