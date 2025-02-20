import pandas as pd
import numpy as np

class ProspectTheory:
    def __init__(self, alp=0.88, lam=2.25, gam=0.61, thet=0.69, window=36,value_column='V'):
        """
        Initialize Prospect Theory parameters

        :param alp: Utility function curvature for gains/losses
        :param lam: Loss aversion parameter
        :param gam: Probability weighting for gains
        :param thet: Probability weighting for losses
        :param window: Rolling window size for calculation
        """
        self.alp = alp
        self.lam = lam
        self.gam = gam
        self.thet = thet
        self.window = window
        self.valuecol = value_column
        self.weights_dict = {}

        print(f"Initialized ProspectTheory with:")
        print(f"α (alpha): {self.alp}")
        print(f"λ (lambda): {self.lam}")
        print(f"γ (gamma): {self.gam}")
        print(f"θ (theta): {self.thet}")
        print(f"Window: {self.window} months")

    def value(self, data):
        """
        Apply prospect theory value function

        :param data: Array of returns
        :return: Transformed values according to prospect theory
        """
        # Handle NaNs
        data = np.nan_to_num(data, nan=0.0)

        # Create a sign factor based on the original sign
        factor = np.where(data < 0, -self.lam, 1)

        # Take absolute value and raise to alpha power
        abs_data = np.abs(data) ** self.alp

        # Multiply by the sign factor
        return abs_data * factor

    def prob_w(self, P, f):
        """
        Probability weighting function

        :param P: Probability
        :param f: Weighting parameter
        :return: Transformed probability
        """
        return (P**f) / ((P**f + (1 - P)**f)**(1 / f))

    def weights(self, mm, nn):
        """
        Compute probability weights for a distribution

        :param mm: Number of negative returns
        :param nn: Number of positive returns
        :return: Probability weights
        """
        # Check if weights are already computed
        if (mm, nn) in self.weights_dict:
            return self.weights_dict[(mm, nn)]

        # Total number of observations
        l = nn + mm

        # Negative weights (losses)
        neg_indices = np.arange(1, mm + 1)
        neg_weights = (self.prob_w(neg_indices / l, self.thet) -
                       self.prob_w((neg_indices - 1) / l, self.thet))

        # Positive weights (gains)
        pos_indices = np.arange(1, nn + 1)
        pos_weights = (self.prob_w((nn - pos_indices + 1) / l, self.gam) -
                       self.prob_w((nn - pos_indices) / l, self.gam))

        # Combine weights
        weights = np.concatenate([neg_weights, pos_weights])

        # Cache and return
        self.weights_dict[(mm, nn)] = weights
        return weights

    def compute_TK(self, returns):
        """
        Compute Tversky-Kahneman (TK) prospect theory value

        :param returns: Array of modified returns
        :return: Prospect theory value
        """
        # Ensure returns are numeric and handle NaNs
        returns = np.nan_to_num(returns, nan=0.0)

        # Sort returns - ***** COULD BE REMOVED AS ALREADY Sorted
        # sorted_returns = np.sort(returns)

        # Count negative and positive returns
        mm = np.sum(returns < 0)
        nn = len(returns) - mm

        # Compute value function for returns - SHOULD ON THE WHOLE RETURNS
        #values = self.value(returns)

        # Compute probability weights
        weights = self.weights(mm, nn)

        # Compute TK value
        tk_value = np.dot(weights, returns)

        return tk_value

    def process_group(self, group):
        """
        Process a group of returns to compute rolling TK value

        :param group: DataFrame group for a specific stock
        :return: DataFrame with TK values
        """

        # Ensure enough data points
        if len(group) < self.window:
            group['TK'] = 0
            return group

        # Compute rolling TK values
        group['TK'] = group[self.valuecol].rolling(
            window=self.window,
            min_periods=self.window
        ).apply(lambda x: self.compute_TK(x))
        return group

    def prospect(self, data):
        """
        Main method to compute prospect theory factor

        :param data: Input DataFrame
        :return: DataFrame with TK values
        """
        print("\n--- Prospect Theory Factor Computation ---")

        # Ensure required columns
        required_cols = ['permno', 'yyyymm','ret']
        data = data.loc[:, required_cols]

        # Sort by PERMNO and date
        data = data.sort_values(['permno', 'yyyymm'])

        data[self.valuecol] = self.value(data['ret'].values)
        # Compute TK values for each stock
        processed = data.groupby('permno', group_keys=False).apply(self.process_group)
        processed['TK'] = processed.TK.fillna(0)

        print("\n--- Prospect Theory Computation Complete ---")

        return processed