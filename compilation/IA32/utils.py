import uuid


def get_unqiue_id():
    return uuid.uuid4().hex[:6].upper()
