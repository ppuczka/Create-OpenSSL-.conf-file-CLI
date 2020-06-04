class ApiException(Exception):
    def __init__(self, code, message=None):
        if message is None:
            message = f'Error while sending request, response code is {code}'
        super(ApiException, self).__init__(message)
        self.code = code


