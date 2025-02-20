This notebook cleans and pre-processes financial data. It performs several key operations:
### Data Loading and Preparation
1. Reads financial data from a Parquet file `factors.parquet`.
2. Removes rows with missing values in the 'ret' column.
3. **Industry Classification:** Classifies companies into industries based on their SIC codes using data from an Excel file `SIC_49_Industry.xlsx`.
### Feature Engineering
4. **Prospect Theory Factor:** Calculates the prospect theory factor (TK) using a custom `ProspectTheory` class.
5. **Market Age Factor:** Calculates the market age of each company (in years).
### Data Cleaning and Preprocessing
6. **Outlier Handling:** Outliers are first capped at the 0.5% and 99.5% quantiles, based on the industry. Then outliers based on standard deviations are removed.
7. **Financial Sector Removal:** Removes data for companies in the financials sectors (industries 48 and 50)
8. **Z-Score Normalization:** Standardizes relevant features by calculating z-scores within each year and industry, creating new columns. (Normalize based on insample data)
### Data Imputation

9. **Missing Value Handling:** Creates three versions of the dataset, each handling missing values differently:
	- `industry_mean.parquet`: Imputes missing values with the mean for each year and industry.
	- `industry_mean_mask.parquet`: Imputes missing values with the mean for each year and industry for a subset of columns with a specified missing value threshold.
	- `industry_median.parquet`: Imputes missing values with the median for each year and industry.
	- `dropped.parquet`: Drops rows that contain missing values after masking columns with high missing value counts.
10. **Saves Datasets:** Saves all processed datasets to Parquet files in the `imputed` subdirectory on Google Drive.
### Setup Instructions
- **Custom Code:** The script uses a custom class `ProspectTheory`, which needs to be in the specified code directory path.
- **Excel File:** Requires the `SIC_49_Industry.xlsx` file to classify industries.

If there are other factors which needs to be added, use [[Additional Factor]]
We can also try imputing data using Random Forrest [[ML Imputation]]
Optional next step would be to Explore our factors [[Deep Factor Exploration]]
Then we will move on to factor selection [[Factor Selection]]
Optionally we can also do PCA/other techniques based [[Factor Reduction]]