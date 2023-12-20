import pytest
from project import compare, validate, assign

def test_compare():
    d, s = compare("games", "games")
    assert s == 5
    d, s = compare("earth", "eamop")
    assert s == 2
    d, s = compare("utopi", "amojk")
    assert s == 1

def test_validate():
    assert validate("earth") == True
    assert validate("aaaaa") == False
    assert validate("EaRTh") == True

def test_assign():
    assert assign("earth") == {0: 'e', 1: 'a', 2: 'r', 3: 't', 4: 'h'}
    assert assign("oogle") == {0: 'o', 1: 'o', 2: 'g', 3: 'l', 4: 'e'}
