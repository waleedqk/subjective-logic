import math
from typing import Annotated

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


    def __str__(self):
        """
        Returns a string representation of the binomial opinion.

        Returns:
            str: A string describing the binomial opinion.
        """
        return (f"BinomialOpinion(belief={self.belief:.3f}, disbelief={self.disbelief:.3f}, "
                f"uncertainty={self.uncertainty:.3f}, base_rate={self.base_rate:.3f})")
