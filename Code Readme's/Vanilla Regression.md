This notebook implements a quantitative investment strategy based on Fama-MacBeth regressions and portfolio optimization. It uses a dataset of financial data to identify significant factors predicting stock returns, constructs portfolios based on these factors, and then evaluates the performance of these portfolios against a market benchmark.

### Methodology
1. **Data Preparation:** The notebook begins by loading and preparing the necessary data, merging different datasets and performing necessary data cleaning.
2. **Fama-MacBeth Regression:** A Fama-MacBeth cross-sectional regression is performed to identify factors significantly related to stock returns. The regressions are run on a rolling basis. Key statistics including t-statistics are calculated and reported. Significant factors are selected based on their t-statistic.
3. **Portfolio Formation:** Portfolios are formed based on decile rankings derived from composite scores. The composite score is created by summing the product of each stock's factor value and its corresponding t-statistic from the Fama-MacBeth regression. A long-short portfolio strategy is employed using the top and bottom deciles.
4. **Performance Evaluation:** Portfolio performance is assessed using various metrics:
	* Mean returns
	* Standard deviation
	* Sharpe ratio
	* Cumulative returns
5. **Factor Model Analysis:** The portfolio returns are regressed on the Fama-French factors to evaluate alphas and determine the performance of the strategy compared to known market factors.
6. **Portfolio Optimization:** The notebook demonstrates optimization of a long-short portfolio with a market factor using weights derived from a minimization of the negative Sharpe ratio. The results are compared to a market-only strategy with a risk-free asset as a reference.

### Significant Variables Found

zlnP is quite significant and negative which means lower priced stocks perform better. Reasonable
zlnsize is a litle significant showing positive effect, implying bigger firms perform better.
zAbnormal Accurals imply ?
zAssetGrowwth is positive, firms which are actively expanding provide better results.
zCPVolSpread shows that when there is more uncertainity about stock there is a +ve effect on returns.
zEarningsStreak is not entirely significant but it has a +ve sign
zFEPS is quite significant and positive emplying forecasted EPS being high has a +ve effect on returns
zfgr5yrLag is pretty interesting as it is negative - A probable reason is that high 5yr growth imply higher forward beta.
zGP is positive and significant
### Usage

The notebook can be run as is in Google Colab. Ensure that the necessary libraries and data files are correctly configured. The data directory (`data_dir`) should be modified to reflect the actual location of the data files in your Google Drive.

### Conclusion
