class BaseOpener(object):

    def open_door(self):
        raise NotImplementedError('Please implement open_door')

    def close_door(self):
        raise NotImplementedError('Please implement close_door')