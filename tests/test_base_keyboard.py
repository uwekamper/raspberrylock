import pytest

from raspberrylock.keyboards.base_keyboard import BaseKeyboard


def test_read_buttons():
    bk = BaseKeyboard()
    with pytest.raises(NotImplementedError):
        bk.read_buttons()
        # event_loop.run_until_complete(bk.read_buttons())