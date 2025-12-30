import pytest

from lib(pytest)_assert_3 import square #plz remmerber to rename the file beofre running 

def test_pos():
    assert square(2) == 4
    assert square(3) == 9

def test_nev():
    assert square(-2) == 4
    assert square(-3) == 9

def test_zero():
    assert square(0) == 0

def test_str():
    with pytest.raises(TypeError):
        square("cat")

# Note: 
# For running the above file plz use this cmd in terminal: python -m pytest Python_prog/Testing_3.py

