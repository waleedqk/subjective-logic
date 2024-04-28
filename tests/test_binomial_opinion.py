from subjective_logic import BinomialOpinion
import pytest

def test_binomial_opinion_initialization():
    opinion = BinomialOpinion(belief=0.5, disbelief=0.3, uncertainty=0.2, base_rate=0.5)
    assert opinion.belief == 0.5
    assert opinion.disbelief == 0.3
    assert opinion.uncertainty == 0.2
    assert opinion.base_rate == 0.5

