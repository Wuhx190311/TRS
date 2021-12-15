class NoItemException(Exception):
    def __init__(self, msg):
        super().__init__(self)
        self.errorInfo = msg

    def __str__(self):
        return self.errorInfo


class NoFlightException(NoItemException):
    def __init__(self):
        super().__init__(self)
        self.errorInfo = 'No Such Flight!'


class NoBusException(NoItemException):
    def __init__(self):
        super().__init__(self)
        self.errorInfo = 'No Such Bus!'


class NoHotelException(NoItemException):
    def __init__(self):
        super().__init__(self)
        self.errorInfo = 'No Such Hotel!'
