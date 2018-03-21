import pytest

from raspberrylock.openers.base_opener import BaseOpener


def test_open_door():
    bo = BaseOpener()
    with pytest.raises(NotImplementedError):
        bo.open_door()

def test_close_door():
    bo = BaseOpener()
    with pytest.raises(NotImplementedError):
        bo.close_door()