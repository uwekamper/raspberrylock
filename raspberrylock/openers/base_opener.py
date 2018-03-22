class BaseOpener(object):

    async def open_door(self):
        raise NotImplementedError('Please implement open_door')

    async def close_door(self):
        raise NotImplementedError('Please implement close_door')