import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# 1) Load Data
iowa_file_path = '../input/train.csv'
home_data = pd.read_csv(iowa_file_path)
y = home_data.SalePrice

# 2) Create X (Features) - Modify to alter model performance
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']

# Select columns corresponding to features, and preview the data
X = home_data[features]
X.head()

# 3) Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# 4) Define a random forest model
rf_model = RandomForestRegressor(random_state=1)

# 5) Fit
rf_model.fit(train_X, train_y)

# 6) Predict
rf_val_predictions = rf_model.predict(val_X)

# 7) Evaluate
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))
