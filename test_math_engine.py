import pytest
from math_engine import validate, question, steps, is_correct

def data(level='Foundation', unknown='c'):
    return dict(level=level,story='Triangle problem',a=3,b=4,c=5,unknown=unknown,hint='Use the formula.',explanation='Apply Pythagoras.')

def test_foundation():
    p=validate(data(),'Foundation')
    assert p.answer==5
    assert is_correct('5',p)
    assert not is_correct('4',p)
    assert '5 cm' in steps(p)[-1]

def test_standard():
    p=validate(data('Standard','a'),'Standard')
    assert p.answer==3
    assert '4 cm' in question(p)

def test_reject_bad_triangle():
    d=data();d['c']=6
    with pytest.raises(ValueError):validate(d,'Foundation')

def test_reject_inappropriate_level():
    with pytest.raises(ValueError):validate(data('Advanced','c'),'Advanced')

def test_reject_non_numeric():
    p=validate(data(),'Foundation')
    assert not is_correct('hello',p)
