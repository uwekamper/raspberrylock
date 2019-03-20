class BaseAuthorization(object):

    def __init__(self, config):
        self.config = config

    def check(self, uid: str, pin: str) -> bool:
        raise NotImplementedError()
