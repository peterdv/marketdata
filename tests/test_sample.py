# -*- coding: utf-8; mode: python-mode; -*-

def test_always_passes():
    assert True

# def test_always_fails():
#     assert False

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4
