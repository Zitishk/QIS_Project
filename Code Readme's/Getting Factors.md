This notebook prepares data for the analysis. It focuses on pre-processing firm-level financial data, merging it with market-level data, and addressing missing values.

**Data Sources:**
The analysis utilizes two primary data sources:
1. **Firm-Level Characteristics:** A comprehensive dataset containing various financial characteristics of firms are taken from Andrew Chen's files.
2. **Returns Data:** A dataset containing historical stock returns, market capitalization, and other relevant information is prepared by the previous code from WRDS.

**Data Cleaning and Preprocessing:**
The notebook performs the following steps:
1. **Data Extraction:** It extracts the zipped firm-level data file and converts it to a Polars DataFrame for efficient data manipulation. The code specifies a set of relevant columns to keep, based on a pre-defined list made on the basis of theoretical understanding.
2. **Handling Missing Data:** The script examines the extent of missing values in each selected column. Some variables can be dropped, based on a domain expert's analysis and the severity of the missing data. The script includes important commentary on why specific decisions were made regarding imputation and/or removal.
3. **Data Merging:** The preprocessed firm characteristics are joined with the market data using a common identifier (firm ID and date).

### Output: 
The preprocessed data (both the raw factors and the merged dataset) are saved to new Parquet files for future analysis.

Next Step - [[Data Preprocessing]]
Optional Step - [[Missing Data Visualization]]