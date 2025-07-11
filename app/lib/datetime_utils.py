def dump_date(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")


def dump_datetime(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")
