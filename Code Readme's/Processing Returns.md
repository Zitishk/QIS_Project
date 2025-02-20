  This notebook processes market returns data for a quantitative investment portfolio. It focuses on cleaning, transforming, and preparing the data for subsequent analysis and modeling.
Runtime: 15 mins
### Data Processing Steps

1. **Data Loading:** Loads both the Fama-French data and stock returns into pandas DataFrames.
2. **Data Cleaning:**
	- Identifies missing dates in the stock return data, reporting the percentage of missing dates.
	- Clips extreme return outliers to improve data stability.
	- Addresses missing returns due to delisting by setting returns to 0 for stocks with a missing last return.
3. **Feature Engineering:**
	- Calculates excess returns by subtracting the risk-free rate (from Fama-French) from the stock returns.
	- Computes log returns from excess returns.
	- Creates lagged returns (`1m.lret`), representing the return shifted one month into the future.
	- Generates rolling sums of future returns over 6 and 12-month windows to capture long term returns.
4. **Data Handling:**
	- Uses `pd.DateOffset` to correctly align the shifted returns with the current month's data as there are missing dates
	- Makes sure when correct dates are chosen in the 6 and 12 months window. Missing dates are treated as 0 return.
5. **Data Export:** Saves the processed data to a new parquet file
###### Key Highlight
Specific care is taken to correctly align lagged returns to their corresponding current month, correctly handling issues arising from non-consecutive dates.
### Output

The processed data, stored in `processed_returns.parquet`, is ready for use in subsequent model building, backtesting, or further analysis.

Next we explore the return characteristics [[Return Exploration]]
Alternatively Skip to [[Getting Factors]]