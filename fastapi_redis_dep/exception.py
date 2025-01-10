class RedisException(Exception):
    def __init__(self, message: str):
        self.msg = message


class RedisDepException(RedisException):
    def __init__(self, message: str):
        self.msg = message



class LockError(RedisException):
    def __init__(self, message: str):
        self.msg = message
