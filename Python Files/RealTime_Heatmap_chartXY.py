# import pandas as pd
# import numpy as np
# import lightningchart as lc
# import random
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder
# import time
# from datetime import datetime

# # Load license key
# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load and preprocess the dataset
# file_path = 'Dataset/database.csv'
# data = pd.read_csv(file_path)
# data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
# data['Year'] = data['Accident Date/Time'].dt.year
# data = data[data['Year'] <= 2017]

# # Encode categorical variables
# encoder = OneHotEncoder(sparse=False)
# categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

# # Prepare features and target
# X = np.hstack((data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], categorical_features))
# y = data['All Costs']

# # Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# model.fit(X_train, y_train)

# # Create a dashboard with two rows
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=1)

# # First Row: Annual Analysis Line Chart
# line_chart = dashboard.ChartXY(row_index=0, column_index=0)
# line_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")
# incident_series = line_chart.add_line_series()
# line_chart.get_default_x_axis().set_tick_strategy('DateTime')

# # Second Row: Heatmap for Geospatial Analysis
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0)
# heatmap_chart.set_title("Geospatial Analysis of All Costs Over Time")
# heatmap = heatmap_chart.add_heatmap_grid_series(rows=100, columns=100)
# heatmap.set_palette_colors(
#     steps=[
#         {'value': 0, 'color': lc.Color(0, 0, 255)},  # Blue
#         {'value': 50000, 'color': lc.Color(0, 255, 0)},  # Green
#         {'value': 100000, 'color': lc.Color(255, 255, 0)},  # Yellow
#         {'value': 500000, 'color': lc.Color(255, 0, 0)}  # Red
#     ],
#     look_up_property='value'
# )
# heatmap_chart.get_default_x_axis().set_title('Longitude')
# heatmap_chart.get_default_y_axis().set_title('Latitude')

# # Simulate dynamic updates for each year from 2010 to 2027
# # Simulate dynamic updates for each year from 2010 to 2027
# def update_dashboard():
#     for year in range(2010, 2028):
#         print(f"Updating year: {year}")
#         if year > 2017:
#             # Generate synthetic data for future years
#             synthetic_data = pd.DataFrame({
#                 'Unintentional Release (Barrels)': np.random.rand(10) * 50,
#                 'Liquid Recovery (Barrels)': np.random.rand(10) * 50,
#                 'Net Loss (Barrels)': np.random.rand(10) * 50,
#                 'Accident Longitude': np.random.uniform(-100, -80, 10),
#                 'Accident Latitude': np.random.uniform(25, 50, 10)
#             })
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
#                                  encoder.transform([['ONSHORE', 'INCORRECT OPERATION']] * 10)))
#             all_costs_pred = model.predict(X_future)
#         else:
#             # Use historical data with corrected column names
#             year_data = data[data['Year'] == year]
#             all_costs_pred = year_data['All Costs']
#             synthetic_data = year_data[['Accident Longitude', 'Accident Latitude']]

#         # Update the line chart for incidents and impact metrics
#         incident_series.add([int(time.mktime(datetime(year, 1, 1).timetuple()) * 1000)], [np.mean(all_costs_pred)])

#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], synthetic_data['Accident Latitude'], bins=[100, 100], weights=all_costs_pred
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
        
#         time.sleep(2)  # Pause to simulate real-time data update


# dashboard.open(live=True)
# update_dashboard()







# import pandas as pd
# import numpy as np
# import lightningchart as lc
# import random
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder
# import time
# from datetime import datetime

# # Load license key
# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# # Load and preprocess the dataset
# file_path = 'Dataset/database.csv'
# data = pd.read_csv(file_path)
# data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
# data['Year'] = data['Accident Date/Time'].dt.year
# data = data[data['Year'] <= 2017]

# # Encode categorical variables
# encoder = OneHotEncoder(sparse=False)
# categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

# # Prepare features and target
# X = np.hstack((data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], categorical_features))
# y = data['All Costs']

# # Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# model.fit(X_train, y_train)

# # Create a dashboard with two rows
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=1)

# # First Row: Annual Analysis of Pipeline Incidents and Impact Metrics
# line_chart = dashboard.ChartXY(row_index=0, column_index=0)
# line_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")

# # Prepare X-axis values (convert years to datetime format in milliseconds)
# x_values = [int(datetime(year, 1, 1).timestamp() * 1000) for year in data['Year'].unique()]
# features = {
#     'Incidents': 'Number of Incidents',
#     'Liquid Recovery': 'Liquid Recovery',
#     'Net Loss': 'Net Loss',
#     'All Costs': 'All Costs (USD)'
# }
# # Remove default Y-axis
# line_chart.get_default_y_axis().dispose()

# # Add Legend
# legend = line_chart.add_legend()

# # Aggregate data by year
# aggregated_data = data.groupby('Year').agg({
#     'Accident Year': 'count',  # Number of incidents
#     'Liquid Recovery (Barrels)': 'sum',
#     'Net Loss (Barrels)': 'sum',
#     'All Costs': 'sum'
# }).reset_index()


# # Update column names if necessary
# aggregated_data.columns = ['Year', 'Incidents', 'Liquid Recovery', 'Net Loss', 'All Costs']

# # Verify that the expected column names are correctly set
# print("Updated Columns in aggregated_data:", aggregated_data.columns)


# # Create a dictionary to store the series references for easy access during updates
# series_dict = {}

# # Add each feature to the chart with its own Y-axis and store the series in the dictionary
# for i, (feature, y_title) in enumerate(features.items()):
#     y_axis = line_chart.add_y_axis(stack_index=i)
#     y_axis.set_title(y_title)
    
#     # Extract corresponding y_values using the updated feature names
#     y_values = aggregated_data[feature].tolist()
#     series = line_chart.add_line_series(y_axis=y_axis, data_pattern='ProgressiveX')
#     series.add(x_values, y_values)
#     series.set_name(y_title)
#     legend.add(series)
    
#     # Store the series reference in the dictionary
#     series_dict[feature] = series

# # Set X-axis
# x_axis = line_chart.get_default_x_axis()
# x_axis.set_title('Year')
# x_axis.set_tick_strategy('DateTime', utc=True)

# # Second Row: Heatmap for Geospatial Analysis
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0)
# # heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year')
# heatmap = heatmap_chart.add_heatmap_grid_series(rows=100, columns=100)
# heatmap.set_palette_colors(
#     steps=[
#         {'value': 0, 'color': lc.Color(0, 0, 255)},  # Blue
#         {'value': 50000, 'color': lc.Color(0, 255, 0)},  # Green
#         {'value': 100000, 'color': lc.Color(255, 255, 0)},  # Yellow
#         {'value': 500000, 'color': lc.Color(255, 0, 0)}  # Red
#     ],
#     look_up_property='value'
# )
# heatmap_chart.get_default_x_axis().set_title('Longitude')
# heatmap_chart.get_default_y_axis().set_title('Latitude')

# def update_dashboard():
#     for year in range(2010, 2028):
#         print(f"Updating year: {year}")
#         if year > 2017:
#             # Generate synthetic data for future years
#             synthetic_data = pd.DataFrame({
#                 'Unintentional Release (Barrels)': np.random.rand(10) * 50,
#                 'Liquid Recovery (Barrels)': np.random.rand(10) * 50,
#                 'Net Loss (Barrels)': np.random.rand(10) * 50,
#                 'Accident Longitude': np.random.uniform(-100, -80, 10),
#                 'Accident Latitude': np.random.uniform(25, 50, 10)
#             })
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
#                                   encoder.transform([['ONSHORE', 'INCORRECT OPERATION']] * 10)))
#             all_costs_pred = model.predict(X_future)
#             heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')
#         else:
#             # Use historical data with corrected column names
#             year_data = data[data['Year'] == year]
#             all_costs_pred = year_data['All Costs']
#             synthetic_data = year_data[['Accident Longitude', 'Accident Latitude']]
#             heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')

#         # Update each series in the line chart for the current year
#         year_timestamp = int(time.mktime(datetime(year, 1, 1).timetuple()) * 1000)
#         for feature in features.keys():
#             feature_values = aggregated_data[aggregated_data['Year'] == year][feature].values
#             if len(feature_values) > 0:  # Check if feature values exist for the year
#                 series_dict[feature].add([year_timestamp], feature_values)
        
#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], synthetic_data['Accident Latitude'], bins=[100, 100], weights=all_costs_pred
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
        
#         time.sleep(2)  # Pause to simulate real-time data update

# # Open the dashboard and start updating
# dashboard.open(live=True)
# update_dashboard()






import pandas as pd
import numpy as np
import lightningchart as lc
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import time
from datetime import datetime

# Load license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load and preprocess the dataset
file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
data['Year'] = data['Accident Date/Time'].dt.year
data = data[data['Year'] <= 2017]

# Encode categorical variables
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

# Prepare features and target
X = np.hstack((data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], categorical_features))
y = data['All Costs']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Use most common categories in the dataset for future years
most_common_categories = data[['Pipeline Type', 'Cause Category']].mode().iloc[0].tolist()

# Create a dashboard with two rows
dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=1)

# First Row: Annual Analysis of Pipeline Incidents and Impact Metrics
line_chart = dashboard.ChartXY(row_index=0, column_index=0)
line_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")
x_values = [int(datetime(year, 1, 1).timestamp() * 1000) for year in range(2010, 2028)]
features = {
    'Incidents': 'Number of Incidents',
    'Liquid Recovery': 'Liquid Recovery',
    'Net Loss': 'Net Loss',
    'All Costs': 'All Costs (USD)'
}
line_chart.get_default_y_axis().dispose()
legend = line_chart.add_legend()

# Create series for each metric
series_dict = {}
for i, (feature, y_title) in enumerate(features.items()):
    y_axis = line_chart.add_y_axis(stack_index=i)
    y_axis.set_title(y_title)
    y_axis.set_title_rotation(315).set_title_font(size=12)
    series = line_chart.add_line_series(y_axis=y_axis, data_pattern='ProgressiveX')
    series.set_name(y_title)
    legend.add(series)
    series_dict[feature] = series

x_axis = line_chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)

# Second Row: Heatmap for Geospatial Analysis
heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0)
heatmap = heatmap_chart.add_heatmap_grid_series(rows=100, columns=100)
heatmap.set_palette_colors(
    steps=[
        {'value': 0, 'color': lc.Color(0, 0, 255)},  # Blue
        {'value': 50000, 'color': lc.Color(0, 255, 0)},  # Green
        {'value': 100000, 'color': lc.Color(255, 255, 0)},  # Yellow
        {'value': 500000, 'color': lc.Color(255, 0, 0)}  # Red
    ],
    look_up_property='value'
)
heatmap_chart.get_default_x_axis().set_title('Longitude')
heatmap_chart.get_default_y_axis().set_title('Latitude')

def update_dashboard():
    for year in range(2010, 2028):
        print(f"Updating year: {year}")
        if year > 2017:
            # Generate synthetic data for future years
            synthetic_data = pd.DataFrame({
                'Unintentional Release (Barrels)': np.random.rand(10) * 50,
                'Liquid Recovery (Barrels)': np.random.rand(10) * 50,
                'Net Loss (Barrels)': np.random.rand(10) * 50,
                'Accident Longitude': np.random.uniform(-100, -80, 10),
                'Accident Latitude': np.random.uniform(25, 50, 10)
            })
            encoded_features = encoder.transform([most_common_categories] * 10)
            X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
                                  encoded_features))
            all_costs_pred = model.predict(X_future)
            
            # Calculate synthetic metrics
            incidents = int(np.random.randint(100, 400))
            liquid_recovery = float(synthetic_data['Liquid Recovery (Barrels)'].sum())
            net_loss = float(synthetic_data['Net Loss (Barrels)'].sum())
            all_costs = float(all_costs_pred.sum())
            synthetic_data['All Costs'] = all_costs_pred
        else:
            # Use historical data for years up to 2017
            year_data = data[data['Year'] == year]
            incidents = int(year_data.shape[0])
            liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
            net_loss = float(year_data['Net Loss (Barrels)'].sum())
            all_costs = float(year_data['All Costs'].sum())
            synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]
        
        year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)  # Ensure native int
        
        # Add data to the line chart with native types
        series_dict['Incidents'].add([year_timestamp], [incidents])
        series_dict['Liquid Recovery'].add([year_timestamp], [liquid_recovery])
        series_dict['Net Loss'].add([year_timestamp], [net_loss])
        series_dict['All Costs'].add([year_timestamp], [all_costs])

        # Update heatmap for All Costs by Longitude and Latitude
        incident_density, lon_edges, lat_edges = np.histogram2d(
            synthetic_data['Accident Longitude'], synthetic_data['Accident Latitude'], bins=[100, 100], weights=synthetic_data['All Costs']
        )
        heatmap.invalidate_intensity_values(incident_density.tolist())
        heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')
        
        time.sleep(4)  # Simulate real-time data update delay

# Open the dashboard and start updating
dashboard.open(live=True)
update_dashboard()
