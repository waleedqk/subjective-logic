from subjective_logic import BinomialOpinion
import pytest

# Helper functions

def validate_binomial_opinion(opinion: "BinomialOpinion"):
    assert 0 <= opinion.belief <= 1
    assert 0 <= opinion.disbelief <= 1
    assert 0 <= opinion.uncertainty <= 1
    assert 0 <= opinion.base_rate <= 1
    assert 0.999 <= opinion.belief + opinion.disbelief + opinion.uncertainty <= 1.001

def compare_binomial_opinions(opinion1, opinion2):
    """
    Compare two BinomialOpinion instances.
    """
    assert opinion1.belief == pytest.approx(opinion2.belief, rel=1e-2)
    assert opinion1.disbelief == pytest.approx(opinion2.disbelief, rel=1e-2)
    assert opinion1.uncertainty == pytest.approx(opinion2.uncertainty, rel=1e-2)
    assert opinion1.base_rate == pytest.approx(opinion2.base_rate, rel=1e-2)

# Unit Tests

def test_binomial_opinion_initialization():
    opinion = BinomialOpinion(belief=0.5, disbelief=0.3, uncertainty=0.2, base_rate=0.5)
    assert opinion.belief == pytest.approx(0.5)
    assert opinion.disbelief == pytest.approx(0.3)
    assert opinion.uncertainty == pytest.approx(0.2)
    assert opinion.base_rate == pytest.approx(0.5)

def test_binomial_opinion_to_from_json():
    opinion1 = BinomialOpinion(belief=0.5, disbelief=0.3, uncertainty=0.2, base_rate=0.5)
    opinion2 = BinomialOpinion.from_json(opinion1.to_json())
    
    compare_binomial_opinions(opinion1, opinion2)

def test_binomial_opinion_from_evidence():
    opinion = BinomialOpinion.from_evidence(r=2, s=1, base_rate=0.5, W=2)
    assert opinion.belief == pytest.approx(0.4)
    assert opinion.disbelief == pytest.approx(0.2)
    assert opinion.uncertainty == pytest.approx(0.4)
    assert opinion.base_rate == pytest.approx(0.5)

def test_binomial_opinion_cumulative_fusion():
    opinion1 = BinomialOpinion(belief=0.5, disbelief=0.3, uncertainty=0.2, base_rate=0.5)
    opinion2 = BinomialOpinion(belief=0.6, disbelief=0.2, uncertainty=0.2, base_rate=0.5)
    fused_opinion = opinion1.cumulative_fusion(opinion2)

    validate_binomial_opinion(fused_opinion)
    
    # specify a custom tolerance for the comparison - sets the relative tolerance to 1% of the expected value
    assert fused_opinion.belief == pytest.approx(0.611, rel=1e-2)
    assert fused_opinion.disbelief == pytest.approx(0.278, rel=1e-2)
    assert fused_opinion.uncertainty == pytest.approx(0.111, rel=1e-2)
    assert fused_opinion.base_rate == pytest.approx(0.5, rel=1e-2)

def test_binomial_opinion_trust_discounting():
    opinion1 = BinomialOpinion(belief=0.2, disbelief=0.4, uncertainty=0.4, base_rate=0.75)
    opinion2 = BinomialOpinion(belief=0.45, disbelief=0.35, uncertainty=0.2, base_rate=0.25)
    trust_discounted_opinion = opinion1.trust_discounting(opinion2)

    validate_binomial_opinion(trust_discounted_opinion)
    
    # specify a custom tolerance for the comparison - sets the relative tolerance to 1% of the expected value
    # Eq: 14.8
    assert trust_discounted_opinion.belief == pytest.approx(0.225, rel=1e-2)
    assert trust_discounted_opinion.disbelief == pytest.approx(0.175, rel=1e-2)
    assert trust_discounted_opinion.uncertainty == pytest.approx(0.600, rel=1e-2)
    assert trust_discounted_opinion.base_rate == pytest.approx(0.250, rel=1e-2)

def test_binomial_opinion_average_fusion():
    opinion1 = BinomialOpinion(belief=0.55, disbelief=0.21, uncertainty=0.24, base_rate=0.28)
    opinion2 = BinomialOpinion(belief=0.16, disbelief=0.64, uncertainty=0.2, base_rate=0.82)
    average_fused_opinion = opinion1.average_fusion(opinion2)

    validate_binomial_opinion(average_fused_opinion)
    
    # specify a custom tolerance for the comparison - sets the relative tolerance to 1% of the expected value
    assert average_fused_opinion.belief == pytest.approx(0.34, rel=1e-2)
    assert average_fused_opinion.disbelief == pytest.approx(0.4445, rel=1e-2)
    assert average_fused_opinion.uncertainty == pytest.approx(0.22, rel=1e-2)
    assert average_fused_opinion.base_rate == pytest.approx(0.55, rel=1e-2)
