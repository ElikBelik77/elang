import uuid


def get_unique_id() -> str:
    """
    This function returns a unique id for loc jumping.
    :return: a unique string id
    """
    return uuid.uuid4().hex[:6].upper()
