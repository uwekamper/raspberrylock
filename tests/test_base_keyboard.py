import pytest

from raspberrylock.keyboards.base_keyboard import BaseKeyboard


def test_open_door():
    bk = BaseKeyboard()
    with pytest.raises(NotImplementedError):
        bk.read_buttons()