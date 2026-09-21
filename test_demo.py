def somme (x, y):
    return x + y

def my_min(a, b):
    return a - b

def test_somme():
    assert somme(5, 6) == 11
    assert somme(-5, 5) == 0
    assert somme(0, 8) == 8

def test_my_min():
    assert my_min(8, 5) == 3
    assert my_min(8, 8) == 0
    assert my_min(0, 5) == -5