def call_callable(data):
    if callable(data):
        return data()
    else:
        return data
