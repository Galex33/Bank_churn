import pytest
from utils.prediction import *
import sklearn 
def test_true():
    a = True
    assert a == True

def test_to_recover_model():
    typeModel = get_model('France')
    assert type(typeModel) == sklearn.pipeline.Pipeline

