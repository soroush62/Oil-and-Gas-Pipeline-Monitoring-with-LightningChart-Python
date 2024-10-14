import pandas as pd
import numpy as np
import lightningchart as lc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor


lc.set_license(open('../license-key').read())

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
data['Year'] = data['Accident Date/Time'].dt.year
data = data[data['Year'] <= 2017]

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

imputer = SimpleImputer(strategy='mean')
numerical_features = ['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)',
                      'Property Damage Costs', 'Lost Commodity Costs', 'Public/Private Property Damage Costs',
                      'Emergency Response Costs', 'Environmental Remediation Costs', 'Other Costs']

data[numerical_features] = imputer.fit_transform(data[numerical_features])

X = np.hstack((data[numerical_features], categorical_features))
y = data['All Costs']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Linear Regression': LinearRegression(),
    'Gradient Boosting': GradientBoostingRegressor(random_state=42),
    'Support Vector Regressor': SVR(),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'K-Neighbors Regressor': KNeighborsRegressor(n_neighbors=5)
}

model_performance = {
    'Model': [],
    'MAE': [],
    'MSE': [],
    'R2': []
}

for model_name, model in models.items():
    print(f"Training {model_name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    model_performance['Model'].append(model_name)
    model_performance['MAE'].append(mae)
    model_performance['MSE'].append(mse)
    model_performance['R2'].append(r2)

performance_df = pd.DataFrame(model_performance)
print(performance_df)


dashboard = lc.Dashboard(theme=lc.Themes.Light, rows=1, columns=3)

mae_chart = dashboard.ChartXY(row_index=0, column_index=0)
mae_chart.set_title("Model Comparison - MAE")
mae_chart.add_x_axis().set_title("Model")
mae_chart.add_y_axis().set_title("MAE")
legend=mae_chart.add_legend()

for index, row in performance_df.iterrows():
    series = mae_chart.add_point_series().add([index], [row['MAE']])
    series.set_name(row['Model'])
    legend.add(data=series)

mse_chart = dashboard.ChartXY(row_index=0, column_index=1)
mse_chart.set_title("Model Comparison - MSE")
mse_chart.add_x_axis().set_title("Model")
mse_chart.add_y_axis().set_title("MSE")
legend=mse_chart.add_legend()

for index, row in performance_df.iterrows():
    series = mse_chart.add_point_series().add([index], [row['MSE']])
    series.set_name(row['Model'])
    legend.add(data=series)

r2_chart = dashboard.ChartXY(row_index=0, column_index=2)
r2_chart.set_title("Model Comparison - R2 Score")
r2_chart.add_x_axis().set_title("Model")
r2_chart.add_y_axis().set_title("R2 Score")
legend=r2_chart.add_legend()

for index, row in performance_df.iterrows():
    series = r2_chart.add_point_series().add([index], [row['R2']])
    series.set_name(row['Model'])
    legend.add(data=series)

dashboard.open()
