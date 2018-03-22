import pytest

from raspberrylock.openers.base_opener import BaseOpener


def test_open_door(event_loop):
    bo = BaseOpener()
    with pytest.raises(NotImplementedError):
        event_loop.run_until_complete(bo.open_door())

def test_close_door(event_loop):
    bo = BaseOpener()
    with pytest.raises(NotImplementedError):
        event_loop.run_until_complete(bo.close_door())