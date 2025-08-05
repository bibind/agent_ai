from urllib.parse import parse_qsl


def parse_options_header(value):
    return value, {}


class QuerystringParser:
    def __init__(self, callbacks):
        self.callbacks = callbacks

    def write(self, data):
        for name, value in parse_qsl(data.decode()):
            self.callbacks["on_field_start"]()
            self.callbacks["on_field_name"](name.encode(), 0, len(name))
            self.callbacks["on_field_data"](value.encode(), 0, len(value))
            self.callbacks["on_field_end"]()

    def finalize(self):
        self.callbacks["on_end"]()


class MultipartParser:
    def __init__(self, boundary, callbacks):
        self.callbacks = callbacks

    def write(self, data):
        pass

    def finalize(self):
        self.callbacks.get("on_end", lambda: None)()
