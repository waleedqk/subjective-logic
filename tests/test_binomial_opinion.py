from subjective_logic import BinomialOpinion
import pytest

def test_binomial_opinion_initialization():
    opinion = BinomialOpinion(belief=0.5, disbelief=0.3, uncertainty=0.2, base_rate=0.5)
    assert opinion.belief == 0.5
    assert opinion.disbelief == 0.3
    assert opinion.uncertainty == 0.2
    assert opinion.base_rate == 0.5

# write a test to compare opinion when using json serialization
def test_binomial_opinion_to_from_json():
    opinion1 = BinomialOpinion(belief=0.5, disbelief=0.3, uncertainty=0.2, base_rate=0.5)
    opinion2 = BinomialOpinion.from_json(opinion1.to_json())
    
    compare_opinions(opinion1, opinion2)


def compare_opinions(opinion1, opinion2):
    """
    Compare two BinomialOpinion instances.
    """
    assert opinion1.belief == opinion2.belief
    assert opinion1.disbelief == opinion2.disbelief
    assert opinion1.uncertainty == opinion2.uncertainty
    assert opinion1.base_rate == opinion2.base_rate