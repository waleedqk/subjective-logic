# __main__.py

import sys
from .binomial_opinion import BinomialOpinion

def main():
    if len(sys.argv) != 5:
        print("Usage: python -m subjective_logic <belief> <disbelief> <uncertainty> <base_rate>")
        sys.exit(1)

    belief = float(sys.argv[1])
    disbelief = float(sys.argv[2])
    uncertainty = float(sys.argv[3])
    base_rate = float(sys.argv[4])

    opinion = BinomialOpinion(belief, disbelief, uncertainty, base_rate)
    print(f"Created Binomial Opinion: {opinion}")

if __name__ == "__main__":
    main()