**Summary of The Project**

## Introduction
This project aims to preprocess and analyze financial data to extract meaningful investment factors, handle missing data, and conduct regression-based portfolio analysis. The methodology integrates theoretical finance concepts with quantitative techniques to ensure robust and interpretable results.

## Data Preprocessing and Feature Engineering
### Data Collection
- The dataset comprises financial factors extracted from multiple sources, including CRSP and WRDS, covering stock returns and firm characteristics from **1990 to 2023**.
- **Training Periods:** 1993-2013 and 2013-2023.
- **Testing Periods:** 1990-1992 and 2013-2023.
- Industry classification is performed using SIC codes to ensure sector-specific analysis.

### Data Cleaning
- **Outlier Handling:** Extreme values are managed by capping at industry-based quantiles and standard deviation-based trimming.
- **Missing Data Imputation:** Various strategies, including industry mean, median imputation, and MICEForest, are tested for optimal factor preservation.
- **Normalization:** Z-score normalization is applied within each year and industry to ensure comparability.
- **Financial Sector Exclusion:** Companies in financial industries are excluded due to their distinct capital structures.

## Exploratory Data Analysis (EDA)
### Factor Distributions and Correlations
- Histograms and hexbin plots reveal skewness in key factors such as realized volatility, max return, and idiosyncratic volatility.
- Correlation matrices highlight relationships between factors and stock returns, aiding in factor selection.

### Temporal Dynamics and Market Events
- Significant market events (e.g., 2000, 2008, and 2020) correspond with high return volatility and abnormal factor behavior.
- The impact of firm age and structural breaks on return predictability is explored.

## Factor Selection and Reduction
- **Multicollinearity Detection:** Highly correlated variables are identified using correlation matrices and Variance Inflation Factor (VIF) analysis.
- **Dimensionality Reduction:** Factor reduction techniques such as PCA are considered to enhance model interpretability.
- **Selection Criteria:** The initial dataset contained **50 variables**, of which **20 were found to be significant** based on theoretical justification and statistical significance in predicting returns.

## Regression-Based Portfolio Analysis
### Methodology
- **Fama-MacBeth Regression:** Used to assess factor significance in predicting stock returns across time.
- **Cross-Sectional Regressions:** Identify relevant factors through coefficient analysis and statistical validation.
- **Portfolio Construction:** Decile-based ranking is employed to create long-short portfolios based on significant factors.
- **Future Returns Constructed:** 1-month, 6-month, and 12-month future returns.

### Portfolio Turnover and Training Frequency
- **Portfolio Turnover:** Chosen as **yearly**, but an option exists for **monthly** turnover.
- **Training Frequency:** Can be done on **annual or monthly** basis.

### Performance Evaluation
- **Metrics Used:** Mean returns, Sharpe ratios, alpha calculations, and cross-validation techniques ensure robust factor performance assessment.
- **Model Comparison:** Various imputation strategies are compared, with industry mean and MICEForest emerging as top performers in terms of Sharpe ratios and alpha stability.
- **Time Horizon Considerations:** Shorter-term models exhibit better performance, but overfitting risks are analyzed through validation comparisons.

## Future Research Directions
- Investigating the impact of longer return horizons on factor predictability.
- Exploring alternative machine learning imputation techniques for improved data handling.
- Enhancing portfolio optimization strategies through dynamic weighting schemes.
- Addressing survivorship bias by incorporating data on delisted firms.

## Conclusion
This work provides a comprehensive framework for financial data preprocessing, factor selection, and regression-based portfolio construction. The insights gained contribute to developing robust quantitative investment strategies while ensuring statistical rigor and economic interpretability.

