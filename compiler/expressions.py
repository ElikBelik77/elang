class Statement:
    def compile(self, context):
        pass


class HasValue:
    def get_value(self, context):
        pass


class Return(Statement):
    def __init__(self, var):
        self.return_var = var


class Int(Statement, HasValue):
    def __init__(self, name):
        self.name = name

    def get_value(self, context):
        pass


class ConstantValue(HasValue):
    def __init__(self, value):
        self.value = value

    def get_value(self, context):
        pass
