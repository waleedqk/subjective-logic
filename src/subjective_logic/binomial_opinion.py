import math
from decimal import Decimal, ROUND_HALF_UP
from typing import Annotated, Union

class BinomialOpinion:
    """
    Represents a binomial opinion in subjective logic.
    """

    belief: Annotated[int | float, "The belief value."]
    disbelief: Annotated[int | float, "The disbelief value."]
    uncertainty: Annotated[int | float, "The uncertainty value."]
    base_rate: Annotated[int | float, " The base rate (a priori probability)."]    

    def __init__(self, belief, disbelief, uncertainty, base_rate=0.5):
        """
        Initializes a BinomialOpinion instance.

        Args:
            belief (float): The belief component of the opinion.
            disbelief (float): The disbelief component of the opinion.
            uncertainty (float): The uncertainty component of the opinion.
            base_rate (float): The base rate (default 0.5).
        """

        self._belief = None
        self._disbelief = None
        self._uncertainty = None
        self._base_rate = None

        self.set_param('belief', belief)
        self.set_param('disbelief', disbelief)
        self.set_param('uncertainty', uncertainty)
        self.set_param('base_rate', base_rate)
        self.validate_opinion()

    def set_param(self, attribute, value):
        """
        Set the value of a parameter of the opinion object.
        """
        # 1.000000 means we want to keep up to 6 decimal places.
        value = Decimal(value).quantize(Decimal("1.000000"), rounding=ROUND_HALF_UP)
        setattr(self, f'_{attribute}', self._validate_value(self._set_to_zero_if_close(value, n_decimal_places=6)))


    def _set_to_zero_if_close(self, value, n_decimal_places=6):
        # Threshold for closeness to zero
        threshold = Decimal(10) ** (-n_decimal_places)
        if abs(value) < threshold:
            return Decimal(0)
        else:
            return value
        
    def _validate_value(self, value):
        # Validate that the input is a Decimal between 0 and 1
        if not isinstance(value, Decimal):
            raise ValueError("Value must be a Decimal.")
        if not Decimal(0) <= value <= Decimal(1):
            raise ValueError("Value must be between 0 and 1.")
        return value

    def validate_opinion(self):
        """
        Validates the opinion to ensure the sum of belief, disbelief, and uncertainty equals 1.
        Raises an exception if the validation fails.
        """
        total = self._belief + self._disbelief + self._uncertainty
        if not (Decimal("0.999999") <= total <= Decimal("1.000001")):  # Allows a small margin for floating-point errors
            raise ValueError("The sum of belief, disbelief, and uncertainty must equal 1.")

    @property
    def belief(self):
        return float(self._belief)

    @belief.setter
    def belief(self, value):
        self.set_param('belief', value)

    @property
    def disbelief(self):
        return float(self._disbelief)

    @disbelief.setter
    def disbelief(self, value):
        self.set_param('disbelief', value)

    @property
    def uncertainty(self):
        return float(self._uncertainty)

    @uncertainty.setter
    def uncertainty(self, value):
        self.set_param('uncertainty', value)

    @property
    def base_rate(self):
        return float(self._base_rate)

    @base_rate.setter
    def base_rate(self, value):
        self.set_param('base_rate', value)

    def to_json(self):
        """
        Returns the opinion as a JSON object.
        """
        return {
            "belief": self.belief,
            "disbelief": self.disbelief,
            "uncertainty": self.uncertainty,
            "base_rate": self.base_rate
        }

    @classmethod
    def from_json(cls, opinion_json):
        """
        Creates a BinomialOpinion object from a JSON object.

        Args:
            opinion_json (dict): A JSON-like dictionary containing keys for 'belief', 'disbelief', 'uncertainty', and 'base_rate'.

        Returns:
            BinomialOpinion: An instance of BinomialOpinion initialized from the provided JSON.

        Raises:
            ValueError: If the input is not a dictionary or is missing any of the required keys.
        """
        # Check that the json object is valid
        if not isinstance(opinion_json, dict):
            raise ValueError("JSON object must be a dictionary.")
        required_keys = ["belief", "disbelief", "uncertainty", "base_rate"]
        if not all(key in opinion_json for key in required_keys):
            raise ValueError("JSON object must contain the keys 'belief', 'disbelief', 'uncertainty', and 'base_rate'.")

        return cls(
            opinion_json["belief"], 
            opinion_json["disbelief"], 
            opinion_json["uncertainty"], 
            opinion_json.get("base_rate", 0.5)  # Assuming default base_rate as 0.5 if not specified
        )

    def probability(self) -> Union[float, int]:
        """
        Calculates the expected probability of the opinion.
        
        Returns:
            float | int: The probability of the binomial opinion, which could be either a float or an int.
        
        Raises:
            ValueError: If the calculated probability is not between 0 and 1.
        """
        # Use Decimal for precise calculation
        probability = self._belief + self._base_rate * self._uncertainty

        # Add error check that the probability is between 0 and 1
        if not Decimal(0) <= probability <= Decimal(1):
            raise ValueError("Probability must be between 0 and 1.")

        # Convert to float before returning
        return float(probability)
    
    @classmethod
    def from_evidence(cls, r, s, base_rate=0.5, W=2):
        """
        Get a binomial opinion based on positive and negative evidence.

        Args:
            r (int): Positive evidence. Must be a positive integer.
            s (int): Negative evidence. Must be a positive integer.
            a (float): Base rate, default is 0.5.
            W (float): Non-informative prior weight, default is 2.
        
        Returns:
            BinomialOpinion: An instance of BinomialOpinion initialized from evidence.

        Raises:
            ValueError: If 'r' or 's' are not positive integers.
        """
        
        # Validate that r and s are positive integers
        if not (isinstance(r, int) and r > 0):
            raise ValueError("Positive evidence 'r' must be a positive integer.")
        if not (isinstance(s, int) and s > 0):
            raise ValueError("Negative evidence 's' must be a positive integer.")
            
        belief = Decimal(r) / (Decimal(r) + Decimal(s) + Decimal(W))
        disbelief = Decimal(s) / (Decimal(r) + Decimal(s) + Decimal(W))
        uncertainty = Decimal(W) / (Decimal(r) + Decimal(s) + Decimal(W))

        # Create a new instance of BinomialOpinion using the calculated values
        return cls(float(belief), float(disbelief), float(uncertainty), base_rate)

    
    def __str__(self):
        """
        Returns a string representation of the binomial opinion.

        Returns:
            str: A string describing the binomial opinion.
        """
        return (f"BinomialOpinion(belief={self.belief:.3f}, disbelief={self.disbelief:.3f}, "
                f"uncertainty={self.uncertainty:.3f}, base_rate={self.base_rate:.3f})")
    
    def __repr__(self):
        return f"BinomialOpinion(belief={float(self.belief)}, disbelief={float(self.disbelief)}, uncertainty={float(self.uncertainty)}, base_rate={float(self.base_rate)})"    

    def cumulative_fusion(self, other: "BinomialOpinion"):
        """
        Performs cumulative fusion with another BinomialOpinion object.
        
        :param other: Another BinomialOpinion object to fuse with
        :return: A new BinomialOpinion object representing the fused opinion

        Assume a long-term opinion about agent X, is calculated based on previous observations within a time window. 
        And newly observed evidences forms a short-term opinion just on that window.
        The updated BinomialOpinion is now over the entire time period vis the cumulative fusion opinion.
        """
        # Eq: 12.14

        # Check for the edge case where both uncertainties are zero, which would cause division by zero
        if self._uncertainty == 0 and other._uncertainty == 0:
            raise ValueError("Cumulative fusion is undefined when both uncertainties are zero.")
            # TODO: Add Eq: 12.15 from book for this case

        # Calculate the fused belief, disbelief, uncertainty, and base rate
        denominator = self._uncertainty + other._uncertainty - (self._uncertainty * other._uncertainty)
        belief = ((self._belief * other._uncertainty) + (other._belief * self._uncertainty)) / denominator
        disbelief = ((self._disbelief * other._uncertainty) + (other._disbelief * self._uncertainty)) / denominator
        uncertainty = (self._uncertainty * other._uncertainty) / denominator


        # Check for the special case where both As are 1
        if self._uncertainty == 1 and other._uncertainty == 1:
            base_rate = (self._base_rate + other._base_rate) / 2
        else:
            base_rate = ((self._base_rate * other._uncertainty) + (other._base_rate * self._uncertainty) - ((self._base_rate + other._base_rate) * self._uncertainty * other._uncertainty)) / \
                        (self._uncertainty + other._uncertainty - (2 * self._uncertainty * other._uncertainty))
        
        return BinomialOpinion(float(belief), float(disbelief), float(uncertainty), float(base_rate))
    

    def trust_discounting(self, other: "BinomialOpinion"):
        """
        Performs trust discounting with another opinion object.

        The discounting operator combines A's trust in B, and B's opinion about X. Then to derive A's opinion about X, the discounting operator is used:
        """

        # Eq: 14.6
        # Calculate the discounted belief, disbelief, and uncertainty using Decimal
        belief = Decimal(self.probability()) * other._belief
        disbelief = Decimal(self.probability()) * other._disbelief
        uncertainty = Decimal(1) - belief - disbelief
        base_rate = other._base_rate

        # Convert the results to float before creating the new BinomialOpinion
        return BinomialOpinion(float(belief), float(disbelief), float(uncertainty), float(base_rate))

    def average_fusion(self, other: "BinomialOpinion"):  
        """
        Performs average fusion with another opinion object.

        Based on two opinions W_A_X (Opinion of A about X) and W_B_X (Opinion of B about X). The average fusion, i.e., the averaged opinion, of these two opinions is calculated as follows:
        """
       
        if self._uncertainty == 0 and other._uncertainty == 0:
            raise ValueError("Cumulative fusion is undefined when both uncertainties are zero.")
            # TODO: Add Eq: 12.19 from book for this case
       
        if self._uncertainty != 0 or other._uncertainty != 0:
            belief = ((self._belief * other._uncertainty) + (other._belief * self._uncertainty)) / (self._uncertainty + other._uncertainty)
            disbelief = ((self._disbelief * other._uncertainty) + (other._disbelief * self._uncertainty)) / (self._uncertainty + other._uncertainty)
            uncertainty = (2 * self._uncertainty * other._uncertainty) / (self._uncertainty + other._uncertainty)
            base_rate = (self._base_rate + other._base_rate) / 2

        return BinomialOpinion(float(belief), float(disbelief), float(uncertainty), float(base_rate))

# TODO: Weighted Belief Fusion (Eq: 12.22)