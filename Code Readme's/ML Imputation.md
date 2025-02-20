### Data Imputation using MICEForest
This notebook demonstrates data imputation using the MICEForest algorithm. It addresses missing values in a financial dataset.

#### Data Preparation
The code converts the 'permno' and 'ind' columns to categorical data types. A subset of the data (`D`) is sampled for computational efficiency. Key columns ('date', 'hsiccd', 's') are removed.
### MICEForest Imputation

1. **Initialization:** An imputation kernel is created using `miceforest.ImputationKernel`.
3. **Hyperparameter Tuning:** `tune_parameters()` optimizes hyperparameters of the underlying imputation models. The optimized parameters are then manually adjusted to prevent issues with large datasets (specifically, capping `num_iterations`, `num_leaves` and `max_depth`).
4. **Final Imputation:** The `mice()` function is run again with the tuned parameters to get the final imputed dataset.
5. **Imputing New Data:** The trained kernel is applied to the full dataset to create a complete dataset with imputed values.
### Output
The final imputed dataset, `D3`, is saved to `data_dir + 'imputed/mice.parquet'`.

Optional next step would be to Explore our factors [[Deep Factor Exploration]]
Then we will move on to factor selection [[Factor Selection]]
Optionally we can also do PCA/other techniques based [[Factor Reduction]]