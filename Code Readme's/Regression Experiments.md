
This notebook performs a quantitative investment analysis using regression techniques. It aims to identify significant factors influencing stock returns and construct portfolios based on those factors and compare the results for different datasets.
### Data Sources

* **Fama-French Data:** Loaded from 'Fama_french.csv'. Contains market risk premium, size, value, and momentum factors.
* **Processed Stock Returns:** Loaded from 'processed_returns.parquet'. Contains monthly stock returns.
* **Imputed Data:** A set of parquet files (specified by the 'imputed' directory). These files likely contain other relevant financial metrics, preprocessed and imputed.
### Methodology
1. **Data Loading and Preprocessing:**
It performs data cleaning and preprocessing such as converting data types, handling missing values, and more importantly Splits the training data into training and validation data. We do not touch the testing data in this notebook
2. **Regression Analysis:**
* A custom regression class `regression` is defined.
* `crossreg`: Executes cross-sectional regressions.
* `coefsm`: Analyzes coefficient statistics.
* `scor_rank`: Calculates scores and ranks based on regression results.
* `portfolio`: Forms long-short portfolios based on the ranks.
* `performance_metrics`: Computes performance statistics (mean returns and Sharpe ratio)
* `carhart_metrics`: Fits the Carhart four-factor model and evaluates alpha.
* `run`: Orchestrates the entire regression pipeline.
3. **Experiment Orchestration:**
* A custom class `experimentor` manages the regression experiments.
* `run_combinations`: Runs regressions on multiple combinations of data.
* `printres`: Presents results in tabular format.  
### Customization
* You can adjust the input data files.
* Change the `rets`, variables used in regressions, and data resampling parameters.
* Modify the portfolio construction logic in the `portfolio` method. Currently the portfolio is turnover is monthly. Currently only the monthly and yearly method is supported. For Yearly Portfolio is constructed in Jan and kept as same for the rest of year. Theoretically Making the portfolio in Jan should not affect performance.
* Adjust the performance metrics and evaluation criteria.
### Output

The final output is a table summarizing the performance of different portfolio combinations across training and validation sets. The table includes metrics like mean returns, Sharpe ratios, R-squared, alpha, and p-value of alpha.

### Interpretation
![[Screenshot 2025-02-04 at 2.41.09 PM.png]]

###### Top 3 performers -
1. Valid Alpha
	1. Industry Mean 12 months: 1.22% pm
	2. Industry Mean 6 months: 1.07% pm
	3. Mice 1 month: 1.03% pm
2. Valid Sharpe
	1. Dropped 6 months: 0.62
	2. Industry Median 12 months: 0.595
	3. Industry Mean 12 months: 0.5812
3. Valid LS Returns
	1. Mice 1 month: 1.14% pm
	2. Industry Mean 12 months: 1.13% pm
	3. Industry Mean 6 months: 1.08% pm
Arguably Sharpe is the most important metric, however taking Alpha into consideration - I am inclined to Make the Industry mean my champion and contrast it with mice 1 month.

4. Training Alpha
	1. Industry Median 12 months: 1.24% pm
	2. Industry Median 6 months: 1.21% pm
5. Training Sharpe
	1. Industry Mean 12 months: 0.41
	2. Industry Median 12 months: 0.40
6. Training LS Returns
	1. Industry Median 12 months: 1.37%
	2. Industry Median 6 months: 1.35%
Interesting to see that training sharpe isn't even close to validation sharpe. I wonder why that is.
Looking at Alpha and LS Returns, it's quite possible that Industry median is leading to overfitting.

When the Data is turned-over monthly detailed analysis is needed but overall the performance is better (as expected) and the 1m models perform better than the 12m models, again expected. Except Industry_median_12! which is also a overall winner model here. Very interesting. Dropped 6m remains top contender for sharpe so maybe some overfitting is still going on here. Could be worth exploring Lasso/Ridge. Industry Mean also has strong performance.
###### Other Factors
1. Time Horizon Impact:
	- Longer time horizons (6m and 12m) generally show better long-short (LS) performance in validation sets
	- The 12-month models consistently show stronger validation performance across different imputation methods
2. Missing Data Handling Methods:
	- Industry mean imputation performs slightly better than MICE (Multiple Imputation by Chained Equations) in most cases
	- The masked approach (industry_mean_mask) shows more stability between training and validation performance, suggesting less overfitting
3. Portfolio Performance:
	- Long portfolios consistently outperform short portfolios across all strategies
	- The best validation performance comes from:
	    - Long portfolio: industry_mean_12 (1.3209)
	    - Long-Short portfolio: industry_mean_12 (1.1338)
	    - Highest Sharpe ratio: industry_mean_12 (valid_s_LS = 0.5812)

Next Steps would be Run the best model in the [[Vanilla Regression]]