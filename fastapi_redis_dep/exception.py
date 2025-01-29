class RedisException(Exception):
    def __init__(self, message: str):
        self.message = message


class RedisDepException(RedisException):
    def __init__(self, message: str):
        self.message = message


class LockError(RedisException):
    def __init__(self, message: str):
        self.message = message

