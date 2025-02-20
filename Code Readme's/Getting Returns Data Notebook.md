This notebook downloads and processes monthly CRSP data from WRDS using SQL as `returns.parquet`. It connects to WRDS, retrieves stock return data, handles delisting events, and prepares the data for further analysis.
Runtime: 6 mins
### Steps

1. **WRDS Connection:** Connects to the WRDS database using user-provided credentials. Ensure you have a valid WRDS account.

2. **CRSP Data Query:** Retrieves monthly stock data from the CRSP database using a SQL query. The query includes information such as `permno`, `date`, `ret`, `shrout`, `prc`, `hsiccd`, `exchcd`, and delisting information (`dlstcd`, `dlret`). The query is focused on data from 1989-2024.

3. **Delisting Return Handling:** Addresses potential issues with delisting returns (`dlret`):
	* Missing `dlret` values are imputed based on delisting codes (`dlstcd`) and exchange codes (`exchcd`).
	* Default delisting returns are applied for specific delisting scenarios (-0.35 for NYSE/AMEX, -0.55 for NASDAQ).
	* Delisting returns are capped at -1.
	* Missing `dlret` after adjustments is filled with 0.

4. **Return Adjustments:** Adjusts returns using the delisting return, ensuring that returns are never less than -100%.

5. **Missing Data Handling:** Rows with missing returns (`ret` = -66, -77, -88, -99) are removed.

6. **Data Cleaning and Transformation:**
	* Absolute values of prices (`prc`) are used (negative prices indicate averages of bid and ask).
	* Market capitalization (`me`) is calculated.
	* Year-month (`yyyymm`) is created from the date column.
	* Log of Mcap (`lnsize`) and price (`lnP`) are computed.

7. **Data Filtering:**
	* Filters out data before 1990.
	* Applies a minimum price threshold based on inflation adjustment.
	* Includes companies with a market cap greater than $100M.

8. **Data Storage:**
	* Saves the final, filtered data to a Parquet file named `returns.parquet` within the specified data directory.
### Setup Instructions

1. **Mount Google Drive**
2. **WRDS Credentials:** Enter your username and password when prompted.
3. **Directory Configuration:** Update the `folder` and `data_dir` variables.

### Output
  
The processed data is stored in a Parquet file named `returns.parquet` located in the specified data directory.

Next step - [[Processing Returns]] 