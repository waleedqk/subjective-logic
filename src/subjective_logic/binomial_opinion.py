import math
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
        self.set_param('belief', belief)
        self.set_param('disbelief', disbelief)
        self.set_param('uncertainty', uncertainty)
        self.set_param('base_rate', base_rate)
        self.validate_opinion()

    def set_param(self, attribute, value):
        """
        Set the value of a parameter of the opinion object.
        """
        setattr(self, attribute, self._validate_value(self._set_to_zero_if_close(value)))

    def _set_to_zero_if_close(self, value, n_decimal_places = 6):
        # Threshold for closeness to zero
        threshold = 10 ** (-n_decimal_places)  

        if abs(value) < threshold:
            return 0
        else:
            return value

    def _validate_value(self, value):

        # Validate that the input is a float between 0 and 1
        if not isinstance(value, (float, int)):
            raise ValueError("Value must be a float or an integer.")
        if not 0 <= value <= 1:
            raise ValueError("Value must be between 0 and 1.")
        return float(value)        

    def validate_opinion(self):
        """
        Validates the opinion to ensure the sum of belief, disbelief, and uncertainty equals 1.
        Raises an exception if the validation fails.
        """
        total = self.belief + self.disbelief + self.uncertainty
        if not (0.999 <= total <= 1.001):  # Allows a small margin for floating-point errors
            raise ValueError("The sum of belief, disbelief, and uncertainty must equal 1.")

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
        probability =  self.belief + self.base_rate * self.uncertainty

        ## add error check that the probability is between 0 and 1
        if not 0 <= probability <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        
        return probability
    
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
            
        belief = r / (r + s + W)
        disbelief = s / (r + s + W)
        uncertainty = W / (r + s + W)

        # Create a new instance of BinomialOpinion using the calculated values
        return cls(belief, disbelief, uncertainty, base_rate)

    
    def __str__(self):
        """
        Returns a string representation of the binomial opinion.

        Returns:
            str: A string describing the binomial opinion.
        """
        return (f"BinomialOpinion(belief={self.belief:.3f}, disbelief={self.disbelief:.3f}, "
                f"uncertainty={self.uncertainty:.3f}, base_rate={self.base_rate:.3f})")
