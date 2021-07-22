import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# 1) Load Data
X_full = pd.read_csv('../input/train.csv', index_col='Id')
y = X_full.SalePrice

# 2) Create X (Features) - Modify to alter model performance
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']

# Select columns corresponding to features, and preview the data
X = X_full[features]
X.head()

# 3) Split into validation and training data
X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state=1, train_size=0.8, test_size=0.2)

# 4) EDA
print(X_train.shape)
missing_val_count_by_column = (X_train.isnull().sum())
print(missing_val_count_by_column[missing_val_count_by_column > 0])

s = (X_train.dtypes == 'object')
object_cols = list(s[s].index)

print("Categorical variables:")
print(object_cols)

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)

print("MAE from Approach 3 (One-Hot Encoding):")
print(score_dataset(OH_X_train, OH_X_valid, y_train, y_valid))


# ) Define a random forest model
rf_model = RandomForestRegressor(random_state=1)

# ) Fit
rf_model.fit(X_train, y_train)

# ) Predict
rf_val_predictions = rf_model.predict(X_valid)

# ) Evaluate
rf_val_mae = mean_absolute_error(rf_val_predictions, y_valid)

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))

# ) Fit to test data & submit (Kaggle Competition)
rf_model.fit(X, y)
predictions = rf_model.predict(X)

output = pd.DataFrame({'Id': X.index, 'SalePrice': predictions})
output.to_csv('submission.csv', index=False)
