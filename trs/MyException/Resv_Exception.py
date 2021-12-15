class RegisteredUserException(Exception):
    def __init__(self):
        self.errorInfo = '用户名已被注册'

    def __str__(self):
        return self.errorInfo


class ReservedItemException(Exception):
    def __init__(self):
        self.errorInfo = '已预定该项目'

    def __str__(self):
        return self.errorInfo


class NoAvailSeatException(Exception):
    def __init__(self):
        super().__init__(self)
        self.errorInfo = 'no available seats'
