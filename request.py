class Request:
    def __init__(self, request_body):
        self.request_body = request_body

    def __getitem__(self, key):
        return self.request_body[key]
