import pytest

from raspberrylock.keyboards.matrix_keyboard import MatrixKeyboard


def test_read_buttons():
    bk = MatrixKeyboard()
    assert bk.read_buttons() == ''