class Export:
    def __init__(self, name):
        self.name = name

    def resolve(self, program) -> "Compilable":
        for obj in program.functions + program.classes + program.globals:
            if obj.name == self.name:
                return obj
            pass


class Include:
    def __init__(self, file_name):
        self.file_name = file_name
        self.module_name = file_name.split('/')[-1].split('.')[0]

