class BaseAuthorization(object):

    def __int__(self, config):
        self.config = config

    def check(self, uid: str, pin: str) -> bool:
        raise NotImplementedError()
