This notebook analyzes multiple parquet files located in a Google Drive directory to identify highly correlated and multicollinear variables within each dataset. 
### Data Loading and Preprocessing
The notebook begins by mounting Google Drive and specifying the directory containing the parquet files. It then reads each file into a Pandas DataFrame and stores them in a dictionary, where the keys are filenames and the values are the corresponding DataFrames.
### Identifying Highly Correlated Variables
A function `find_highly_correlated_variables` is defined to identify highly correlated variables within a given DataFrame using the following steps:
1. Calculates the correlation matrix for specified variables.
2. Replaces the diagonal elements of the correlation matrix with zeros.
3. Identifies variables with a correlation coefficient exceeding a defined threshold (default 0.5).
4. Visualizes the correlation matrix for the highly correlated variables using a heatmap.
This function is applied to each dataset, and the results are stored.
### Variance Inflation Factor (VIF) Analysis
A function `VIF_check` is defined to calculate the Variance Inflation Factor (VIF) for each variable in a DataFrame. The VIF measures the severity of multicollinearity in ordinary least squares regression. A VIF exceeding 5 or 10 is typically considered an indication of multicollinearity.
This function is applied to each dataset.
### Output
This notebook eliminates the highly correlated variables and then saves the data in Final folder.

Next Step would be *drumroll* ...... [[Regression Experiments]]
Or [[Vanilla Regression]] if you already have model specifications in mind.
Alternatively we could have tried Factor reduction techniques like [[Factor Reduction]]