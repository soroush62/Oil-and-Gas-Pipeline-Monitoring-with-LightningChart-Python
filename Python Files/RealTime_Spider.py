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
# encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
# categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

# # Prepare features and target
# X = np.hstack((data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], categorical_features))
# y = data['All Costs']

# # Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# model.fit(X_train, y_train)

# # Use most common categories in the dataset for future years
# most_common_categories = data[['Pipeline Type', 'Cause Category']].mode().iloc[0].tolist()

# # Create a dashboard with two rows and three columns
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# # First Row: Annual Analysis of Pipeline Incidents and Impact Metrics (2 columns)
# line_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
# line_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")
# x_values = [int(datetime(year, 1, 1).timestamp() * 1000) for year in range(2010, 2028)]
# features = {
#     'Incidents': 'Number of Incidents',
#     'Liquid Recovery': 'Liquid Recovery',
#     'Net Loss': 'Net Loss',
#     'All Costs': 'All Costs (USD)'
# }
# line_chart.get_default_y_axis().dispose()
# legend = line_chart.add_legend()

# # Create series for each metric
# series_dict = {}
# for i, (feature, y_title) in enumerate(features.items()):
#     y_axis = line_chart.add_y_axis(stack_index=i)
#     y_axis.set_title(y_title)
#     y_axis.set_title_rotation(315).set_title_font(size=12)
#     series = line_chart.add_line_series(y_axis=y_axis, data_pattern='ProgressiveX')
#     series.set_name(y_title)
#     legend.add(series)
#     series_dict[feature] = series

# x_axis = line_chart.get_default_x_axis()
# x_axis.set_title('Year')
# x_axis.set_tick_strategy('DateTime', utc=True)

# # Spider Chart (1 column)
# spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
# spider_chart.set_title("Pipeline Incident Impact Metrics")
# spider_chart.set_axis_label_font(weight='bold', size=15)
# spider_chart.set_nib_style(thickness=5, color=lc.Color(0, 0, 0))

# metrics = ['Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']
# for metric in metrics:
#     spider_chart.add_axis(metric)

# # Second Row: Heatmap for Geospatial Analysis (3 columns)
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=3)
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

# # Dictionary to track spider chart series
# spider_series_dict = {}

# # Helper function to normalize values to a range between 0 and 10
# def normalize_value(value, min_val, max_val):
#     return (value - min_val) / (max_val - min_val) * 10

# def update_dashboard():
#     # Determine min and max values for normalization
#     min_incidents = 0
#     max_incidents = 500  # Adjust based on dataset
#     min_liquid_recovery = 0
#     max_liquid_recovery = 100000  # Adjust based on dataset
#     min_net_loss = 0
#     max_net_loss = 100000  # Adjust based on dataset
#     min_all_costs = 0
#     max_all_costs = 1000000000  # Adjust based on dataset

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
#             encoded_features = encoder.transform([most_common_categories] * 10)
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
#                                   encoded_features))
#             all_costs_pred = model.predict(X_future)
            
#             # Calculate synthetic metrics
#             incidents = int(np.random.randint(100, 400))
#             liquid_recovery = float(synthetic_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(synthetic_data['Net Loss (Barrels)'].sum())
#             all_costs = float(all_costs_pred.sum())
#             synthetic_data['All Costs'] = all_costs_pred
#         else:
#             # Use historical data for years up to 2017
#             year_data = data[data['Year'] == year]
#             incidents = int(year_data.shape[0])
#             liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(year_data['Net Loss (Barrels)'].sum())
#             all_costs = float(year_data['All Costs'].sum())
#             synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]
        
#         year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)  # Ensure native int
        
#         # Add data to the line chart with native types
#         series_dict['Incidents'].add([year_timestamp], [incidents])
#         series_dict['Liquid Recovery'].add([year_timestamp], [liquid_recovery])
#         series_dict['Net Loss'].add([year_timestamp], [net_loss])
#         series_dict['All Costs'].add([year_timestamp], [all_costs])

#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], synthetic_data['Accident Latitude'], bins=[100, 100], weights=synthetic_data['All Costs']
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
#         heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')

#         # Normalize the values before updating the spider chart
#         normalized_incidents = normalize_value(incidents, min_incidents, max_incidents)
#         normalized_liquid_recovery = normalize_value(liquid_recovery, min_liquid_recovery, max_liquid_recovery)
#         normalized_net_loss = normalize_value(net_loss, min_net_loss, max_net_loss)
#         normalized_all_costs = normalize_value(all_costs, min_all_costs, max_all_costs)

#                 # Update the spider chart dynamically
#         if year not in spider_series_dict:
#             spider_series = spider_chart.add_series()
#             spider_series.set_name(f"Year {year}")
#             spider_series_dict[year] = spider_series

#         # Log normalized values to ensure they are being calculated correctly
#         print(f"Normalized Incidents: {normalized_incidents}, Normalized Liquid Recovery: {normalized_liquid_recovery}, "
#               f"Normalized Net Loss: {normalized_net_loss}, Normalized All Costs: {normalized_all_costs}")

#         # Update the spider chart for the current year with normalized values
#         spider_series_dict[year].add_points([
#             {'axis': 'Incidents', 'value': normalized_incidents},
#             {'axis': 'Average Liquid Recovery', 'value': normalized_liquid_recovery},
#             {'axis': 'Average Net Loss', 'value': normalized_net_loss},
#             {'axis': 'All Costs', 'value': normalized_all_costs}
#         ])

#         time.sleep(5)  # Simulate real-time data update delay

# # Open the dashboard and start updating
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
# encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
# categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

# # Prepare features and target
# X = np.hstack((data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], categorical_features))
# y = data['All Costs']

# # Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# model.fit(X_train, y_train)

# # Use most common categories in the dataset for future years
# most_common_categories = data[['Pipeline Type', 'Cause Category']].mode().iloc[0].tolist()

# # Create a dashboard with two rows and three columns
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# # First Row: Annual Analysis of Pipeline Incidents and Impact Metrics (2 columns)
# line_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
# line_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")
# x_values = [int(datetime(year, 1, 1).timestamp() * 1000) for year in range(2010, 2028)]
# features = {
#     'Incidents': 'Number of Incidents',
#     'Liquid Recovery': 'Liquid Recovery',
#     'Net Loss': 'Net Loss',
#     'All Costs': 'All Costs (USD)'
# }
# line_chart.get_default_y_axis().dispose()
# legend = line_chart.add_legend()

# # Create series for each metric
# series_dict = {}
# for i, (feature, y_title) in enumerate(features.items()):
#     y_axis = line_chart.add_y_axis(stack_index=i)
#     y_axis.set_title(y_title)
#     y_axis.set_title_rotation(315).set_title_font(size=12)
#     series = line_chart.add_line_series(y_axis=y_axis, data_pattern='ProgressiveX')
#     series.set_name(y_title)
#     legend.add(series)
#     series_dict[feature] = series

# x_axis = line_chart.get_default_x_axis()
# x_axis.set_title('Year')
# x_axis.set_tick_strategy('DateTime', utc=True)

# # Spider Chart (1 column)
# spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
# spider_chart.set_title("Pipeline Incident Impact Metrics")
# spider_chart.set_axis_label_font(weight='bold', size=15)
# spider_chart.set_nib_style(thickness=5, color=lc.Color(0, 0, 0))

# metrics = ['Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']
# for metric in metrics:
#     spider_chart.add_axis(metric)

# # Create a spider series to update (we'll reuse this instead of creating new ones each time)
# spider_series = spider_chart.add_series()

# # Second Row: Heatmap for Geospatial Analysis (3 columns)
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=3)
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

# # Helper function to normalize values to a range between 0 and 10
# def normalize_value(value, min_val, max_val):
#     return (value - min_val) / (max_val - min_val) * 10

# def update_dashboard():
#     # Determine min and max values for normalization
#     min_incidents = 0
#     max_incidents = 500  # Adjust based on dataset
#     min_liquid_recovery = 0
#     max_liquid_recovery = 100000  # Adjust based on dataset
#     min_net_loss = 0
#     max_net_loss = 100000  # Adjust based on dataset
#     min_all_costs = 0
#     max_all_costs = 1000000000  # Adjust based on dataset

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
#             encoded_features = encoder.transform([most_common_categories] * 10)
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
#                                   encoded_features))
#             all_costs_pred = model.predict(X_future)
            
#             # Calculate synthetic metrics
#             incidents = int(np.random.randint(100, 400))
#             liquid_recovery = float(synthetic_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(synthetic_data['Net Loss (Barrels)'].sum())
#             all_costs = float(all_costs_pred.sum())
#             synthetic_data['All Costs'] = all_costs_pred
#         else:
#             # Use historical data for years up to 2017
#             year_data = data[data['Year'] == year]
#             incidents = int(year_data.shape[0])
#             liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(year_data['Net Loss (Barrels)'].sum())
#             all_costs = float(year_data['All Costs'].sum())
#             synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]
        
#         year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)  # Ensure native int
        
#         # Add data to the line chart with native types
#         series_dict['Incidents'].add([year_timestamp], [incidents])
#         series_dict['Liquid Recovery'].add([year_timestamp], [liquid_recovery])
#         series_dict['Net Loss'].add([year_timestamp], [net_loss])
#         series_dict['All Costs'].add([year_timestamp], [all_costs])

#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], synthetic_data['Accident Latitude'], bins=[100, 100], weights=synthetic_data['All Costs']
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
#         heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')

#         # Normalize the values before updating the spider chart
#         normalized_incidents = normalize_value(incidents, min_incidents, max_incidents)
#         normalized_liquid_recovery = normalize_value(liquid_recovery, min_liquid_recovery, max_liquid_recovery)
#         normalized_net_loss = normalize_value(net_loss, min_net_loss, max_net_loss)
#         normalized_all_costs = normalize_value(all_costs, min_all_costs, max_all_costs)

#         # Log normalized values to ensure they are being calculated correctly
#         print(f"Normalized Incidents: {normalized_incidents}, Normalized Liquid Recovery: {normalized_liquid_recovery}, "
#               f"Normalized Net Loss: {normalized_net_loss}, Normalized All Costs: {normalized_all_costs}")

#                 # Overwrite points in the spider series for the current year
#         spider_series.add_points([
#             {'axis': 'Incidents', 'value': normalized_incidents},
#             {'axis': 'Average Liquid Recovery', 'value': normalized_liquid_recovery},
#             {'axis': 'Average Net Loss', 'value': normalized_net_loss},
#             {'axis': 'All Costs', 'value': normalized_all_costs}
#         ])

#         # Pause for real-time simulation
#         time.sleep(5)

# # Open the dashboard and start updating
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
# encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
# categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

# # Prepare features and target
# X = np.hstack((data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], categorical_features))
# y = data['All Costs']

# # Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# model.fit(X_train, y_train)

# # Use most common categories in the dataset for future years
# most_common_categories = data[['Pipeline Type', 'Cause Category']].mode().iloc[0].tolist()

# # Create a dashboard with two rows and three columns
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# # First Row: Annual Analysis of Pipeline Incidents and Impact Metrics (2 columns)
# line_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
# line_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")
# x_values = [int(datetime(year, 1, 1).timestamp() * 1000) for year in range(2010, 2028)]
# features = {
#     'Incidents': 'Number of Incidents',
#     'Liquid Recovery': 'Liquid Recovery',
#     'Net Loss': 'Net Loss',
#     'All Costs': 'All Costs (USD)'
# }
# line_chart.get_default_y_axis().dispose()
# legend = line_chart.add_legend()

# # Create series for each metric
# series_dict = {}
# for i, (feature, y_title) in enumerate(features.items()):
#     y_axis = line_chart.add_y_axis(stack_index=i)
#     y_axis.set_title(y_title)
#     y_axis.set_title_rotation(315).set_title_font(size=12)
#     series = line_chart.add_line_series(y_axis=y_axis, data_pattern='ProgressiveX')
#     series.set_name(y_title)
#     legend.add(series)
#     series_dict[feature] = series

# x_axis = line_chart.get_default_x_axis()
# x_axis.set_title('Year')
# x_axis.set_tick_strategy('DateTime', utc=True)

# # Spider Chart (1 column)
# spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
# spider_chart.set_title("Pipeline Incident Impact Metrics")
# spider_chart.set_axis_label_font(weight='bold', size=15)
# spider_chart.set_nib_style(thickness=5, color=lc.Color(0, 0, 0))

# metrics = ['Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']
# for metric in metrics:
#     spider_chart.add_axis(metric)

# # Create a spider series to update (we'll reuse this instead of creating new ones each time)
# spider_series = spider_chart.add_series()

# # Second Row: Heatmap for Geospatial Analysis (3 columns)
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=3)
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

# # Helper function to normalize values to a range between 0 and 10
# def normalize_value(value, min_val, max_val):
#     return (value - min_val) / (max_val - min_val) * 10

# def update_dashboard():
#     # Determine min and max values for normalization
#     min_incidents = 0
#     max_incidents = 500  # Adjust based on dataset
#     min_liquid_recovery = 0
#     max_liquid_recovery = 100000  # Adjust based on dataset
#     min_net_loss = 0
#     max_net_loss = 100000  # Adjust based on dataset
#     min_all_costs = 0
#     max_all_costs = 1000000000  # Adjust based on dataset

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
#             encoded_features = encoder.transform([most_common_categories] * 10)
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
#                                   encoded_features))
#             all_costs_pred = model.predict(X_future)
            
#             # Calculate synthetic metrics
#             incidents = int(np.random.randint(100, 400))
#             liquid_recovery = float(synthetic_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(synthetic_data['Net Loss (Barrels)'].sum())
#             all_costs = float(all_costs_pred.sum())
#             synthetic_data['All Costs'] = all_costs_pred
#         else:
#             # Use historical data for years up to 2017
#             year_data = data[data['Year'] == year]
#             incidents = int(year_data.shape[0])
#             liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(year_data['Net Loss (Barrels)'].sum())
#             all_costs = float(year_data['All Costs'].sum())
#             synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]
        
#         year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)  # Ensure native int
        
#         # Add data to the line chart with native types
#         series_dict['Incidents'].add([year_timestamp], [incidents])
#         series_dict['Liquid Recovery'].add([year_timestamp], [liquid_recovery])
#         series_dict['Net Loss'].add([year_timestamp], [net_loss])
#         series_dict['All Costs'].add([year_timestamp], [all_costs])

#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], synthetic_data['Accident Latitude'], bins=[100, 100], weights=synthetic_data['All Costs']
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
#         heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')

#         # Normalize the values before updating the spider chart
#         normalized_incidents = normalize_value(incidents, min_incidents, max_incidents)
#         normalized_liquid_recovery = normalize_value(liquid_recovery, min_liquid_recovery, max_liquid_recovery)
#         normalized_net_loss = normalize_value(net_loss, min_net_loss, max_net_loss)
#         normalized_all_costs = normalize_value(all_costs, min_all_costs, max_all_costs)

#         # Log normalized values to ensure they are being calculated correctly
#         print(f"Normalized Incidents: {normalized_incidents}, Normalized Liquid Recovery: {normalized_liquid_recovery}, "
#               f"Normalized Net Loss: {normalized_net_loss}, Normalized All Costs: {normalized_all_costs}")

#         # Overwrite points in the spider series for the current year
#         spider_series.add_points([
#             {'axis': 'Incidents', 'value': normalized_incidents},
#             {'axis': 'Average Liquid Recovery', 'value': normalized_liquid_recovery},
#             {'axis': 'Average Net Loss', 'value': normalized_net_loss},
#             {'axis': 'All Costs', 'value': normalized_all_costs}
#         ])

#         # Pause for real-time simulation
#         time.sleep(5)

# # Open the dashboard and start updating
# dashboard.open(live=True)
# update_dashboard()










# import pandas as pd
# import numpy as np
# import lightningchart as lc
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder
# import time
# from datetime import datetime
# from sklearn.impute import SimpleImputer
# from random import random

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
# encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
# categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

# imputer = SimpleImputer(strategy='mean')
# numerical_features = ['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)',
#                       'Property Damage Costs', 'Lost Commodity Costs', 'Public/Private Property Damage Costs',
#                       'Emergency Response Costs', 'Environmental Remediation Costs', 'Other Costs']

# # Apply imputer to numerical columns in the dataset
# data[numerical_features] = imputer.fit_transform(data[numerical_features])

# # Now prepare features and target for the RandomForest model
# X = np.hstack((data[numerical_features], categorical_features))
# y = data['All Costs']

# # Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the model
# model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# model.fit(X_train, y_train)

# # Use most common categories in the dataset for future years
# most_common_categories = data[['Pipeline Type', 'Cause Category']].mode().iloc[0].tolist()

# # Create a dashboard with two rows and three columns
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# # First Row: Annual Analysis of Pipeline Incidents and Impact Metrics (2 columns)
# line_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
# line_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")
# x_values = [int(datetime(year, 1, 1).timestamp() * 1000) for year in range(2010, 2028)]
# features = {
#     'Incidents': 'Number of Incidents',
#     'Liquid Recovery': 'Liquid Recovery',
#     'Net Loss': 'Net Loss',
#     'All Costs': 'All Costs (USD)'
# }
# line_chart.get_default_y_axis().dispose()
# legend = line_chart.add_legend()

# # Create series for each metric
# series_dict = {}
# for i, (feature, y_title) in enumerate(features.items()):
#     y_axis = line_chart.add_y_axis(stack_index=i)
#     y_axis.set_title(y_title)
#     y_axis.set_title_rotation(315).set_title_font(size=12)
#     series = line_chart.add_line_series(y_axis=y_axis, data_pattern='ProgressiveX')
#     series.set_name(y_title)
#     legend.add(series)
#     series_dict[feature] = series

# x_axis = line_chart.get_default_x_axis()
# x_axis.set_title('Year')
# x_axis.set_tick_strategy('DateTime', utc=True)

# # Spider Chart (1 column)
# spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
# spider_chart.set_title("Pipeline Incident Impact Metrics")
# spider_chart.set_axis_label_font(weight='bold', size=15)
# spider_chart.set_nib_style(thickness=5, color=lc.Color(0, 0, 0))

# metrics = ['Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']
# for metric in metrics:
#     spider_chart.add_axis(metric)

# # Create a spider series to update (we'll reuse this instead of creating new ones each time)
# spider_series = spider_chart.add_series()

# # Second Row: Heatmap for Geospatial Analysis (3 columns)
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=3)
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

# # Predefined values for Liquid Recovery, Net Loss, and Incidents between 2017-2027
# predefined_data = {
#     2018: {'Liquid Recovery': 32000, 'Net Loss': 72000, 'Incidents': 200},
#     2019: {'Liquid Recovery': 81000, 'Net Loss': 43000, 'Incidents': 230},
#     2020: {'Liquid Recovery': 24000, 'Net Loss': 61000, 'Incidents': 250},
#     2021: {'Liquid Recovery': 35000, 'Net Loss': 42000, 'Incidents': 150},
#     2022: {'Liquid Recovery': 46000, 'Net Loss': 84000, 'Incidents': 400},
#     2023: {'Liquid Recovery': 67000, 'Net Loss': 45000, 'Incidents': 300},
#     2024: {'Liquid Recovery': 38000, 'Net Loss': 46000, 'Incidents': 220},
#     2025: {'Liquid Recovery': 39000, 'Net Loss': 77000, 'Incidents': 350},
#     2026: {'Liquid Recovery': 40000, 'Net Loss': 98000, 'Incidents': 400},
#     2027: {'Liquid Recovery': 41000, 'Net Loss': 49000, 'Incidents': 150}
# }

# # Helper function to normalize values to a range between 0 and 100
# def normalize_value(value, min_val, max_val):
#     return (value - min_val) / (max_val - min_val) * 100

# def update_dashboard():
#     # Determine min and max values for normalization
#     min_incidents = 0
#     max_incidents = 500  # Adjust based on dataset
#     min_liquid_recovery = 0
#     max_liquid_recovery = 100000  # Adjust based on dataset
#     min_net_loss = 0
#     max_net_loss = 100000  # Adjust based on dataset
#     min_all_costs = 0
#     max_all_costs = 1000000000  # Adjust based on dataset

#     for year in range(2010, 2028):
#         print(f"Updating year: {year}")
#         if year > 2017:
#             # Use predefined values for incidents, liquid recovery, net loss
#             incidents = predefined_data[year]['Incidents']
#             liquid_recovery = predefined_data[year]['Liquid Recovery']
#             net_loss = predefined_data[year]['Net Loss']
            
#             # Generate synthetic data for future years using np.random.uniform
#             synthetic_data = pd.DataFrame({
#                 'Unintentional Release (Barrels)': np.random.uniform(10, 50, size=50),
#                 'Liquid Recovery (Barrels)': [liquid_recovery] * 50,
#                 'Net Loss (Barrels)': [net_loss] * 50,
#                 'Property Damage Costs': np.random.rand(50) * 10000,
#                 'Lost Commodity Costs': np.random.rand(50) * 5000,
#                 'Public/Private Property Damage Costs': np.random.rand(50) * 3000,
#                 'Emergency Response Costs': np.random.rand(50) * 2000,
#                 'Environmental Remediation Costs': np.random.rand(50) * 10000,
#                 'Other Costs': np.random.rand(50) * 1000,
#                 'Accident Longitude': np.random.uniform(-100, -80, 50),
#                 'Accident Latitude': np.random.uniform(25, 50, 50)
#             })

#             # Add missing categorical features for future years (use most common values)
#             encoded_features = encoder.transform([most_common_categories] * 50)

#             # Concatenate numerical features and encoded categorical features to ensure 21 features
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 
#                                                   'Net Loss (Barrels)', 'Property Damage Costs', 'Lost Commodity Costs', 
#                                                   'Public/Private Property Damage Costs', 'Emergency Response Costs', 
#                                                   'Environmental Remediation Costs', 'Other Costs']],
#                                   encoded_features))
            
#             # Ensure that the number of features matches the model's expectation
#             all_costs_pred = model.predict(X_future)

#             # Calculate synthetic metrics
#             all_costs = float(all_costs_pred.sum())
#             synthetic_data['All Costs'] = all_costs_pred
#         else:
#             # Use historical data for years up to 2017
#             year_data = data[data['Year'] == year]
#             incidents = int(year_data.shape[0])
#             liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(year_data['Net Loss (Barrels)'].sum())
#             all_costs = float(year_data['All Costs'].sum())
#             synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]

#         year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)  # Ensure native int
        
#         # Add data to the line chart with native types
#         series_dict['Incidents'].add([year_timestamp], [incidents])
#         series_dict['Liquid Recovery'].add([year_timestamp], [liquid_recovery])
#         series_dict['Net Loss'].add([year_timestamp], [net_loss])
#         series_dict['All Costs'].add([year_timestamp], [all_costs])

#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], synthetic_data['Accident Latitude'], bins=[100, 100], weights=synthetic_data['All Costs']
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
#         heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')

#         # Normalize the values before updating the spider chart
#         normalized_incidents = normalize_value(incidents, min_incidents, max_incidents)
#         normalized_liquid_recovery = normalize_value(liquid_recovery, min_liquid_recovery, max_liquid_recovery)
#         normalized_net_loss = normalize_value(net_loss, min_net_loss, max_net_loss)
#         normalized_all_costs = normalize_value(all_costs, min_all_costs, max_all_costs)

#         print(f"min_incidents: {min_incidents}, max_incidents: {max_incidents}, normalized_incidents: {normalized_incidents}, "
#         f"min_liquid_recovery: {min_liquid_recovery}, max_liquid_recovery: {max_liquid_recovery}, normalized_liquid_recovery: {normalized_liquid_recovery}, "
#         f"min_net_loss: {min_net_loss}, max_net_loss: {max_net_loss}, normalized_net_loss: {normalized_net_loss}, "
#         f"min_all_costs: {min_all_costs}, max_all_costs: {max_all_costs}, normalized_all_costs: {normalized_all_costs}")

#         # Overwrite points in the spider series for the current year
#         spider_series.add_points([
#             {'axis': 'Incidents', 'value': normalized_incidents},
#             {'axis': 'Average Liquid Recovery', 'value': normalized_liquid_recovery},
#             {'axis': 'Average Net Loss', 'value': normalized_net_loss},
#             {'axis': 'All Costs', 'value': normalized_all_costs}
#         ])

#         # Pause for real-time simulation
#         time.sleep(5)

# # Open the dashboard and start updating
# dashboard.open(live=True)
# update_dashboard()













import pandas as pd
import numpy as np
import lightningchart as lc
from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import time
from datetime import datetime
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
data['Year'] = data['Accident Date/Time'].dt.year
data = data[data['Year'] <= 2017]

# Encode categorical variables
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

imputer = SimpleImputer(strategy='mean')
numerical_features = ['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)',
                      'Property Damage Costs', 'Lost Commodity Costs', 'Public/Private Property Damage Costs',
                      'Emergency Response Costs', 'Environmental Remediation Costs', 'Other Costs']

# Apply imputer to numerical columns in the dataset
data[numerical_features] = imputer.fit_transform(data[numerical_features])

# Prepare features and target
X = np.hstack((data[numerical_features], categorical_features))
y = data['All Costs']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
# model = LinearRegression()
model = Pipeline([
    ('scaler', StandardScaler()),
    ('gb_regressor', GradientBoostingRegressor(n_estimators=200, random_state=42))
])
model.fit(X_train, y_train)

# Use most common categories in the dataset for future years
most_common_categories = data[['Pipeline Type', 'Cause Category']].mode().iloc[0].tolist()

# Create a dashboard with two rows and three columns
dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# First Row: Annual Analysis of Pipeline Incidents and Impact Metrics (2 columns)
line_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
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

# Spider Chart (1 column)
spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
spider_chart.set_title("Pipeline Incident Impact Metrics")
spider_chart.set_axis_label_font(weight='bold', size=15)
spider_chart.set_nib_style(thickness=5, color=lc.Color(0, 0, 0))

metrics = ['Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']
for metric in metrics:
    spider_chart.add_axis(metric)

# Create a spider series to update (we'll reuse this instead of creating new ones each time)
spider_series = spider_chart.add_series()

# Second Row: Heatmap for Geospatial Analysis (3 columns)
heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=3)
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

# Helper function to normalize values to a range between 0 and 100
def normalize_value(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 100

def update_dashboard():
    min_incidents = 0
    max_incidents = 500  # Adjust based on dataset
    min_liquid_recovery = 0
    max_liquid_recovery = 100000  # Adjust based on dataset
    min_net_loss = 0
    max_net_loss = 100000  # Adjust based on dataset
    min_all_costs = 0
    max_all_costs = 1000000000  # Adjust based on dataset

    for year in range(2010, 2028):
        print(f"Updating year: {year}")
        if year > 2017:
            synthetic_data = pd.DataFrame({
            'Unintentional Release (Barrels)': np.random.uniform(0, 500, size=50),
            'Liquid Recovery (Barrels)': np.random.uniform(0, 8000, size=50),
            'Net Loss (Barrels)': np.random.uniform(0, 5000, size=50),
            'Property Damage Costs': np.random.uniform(0, 1000000, size=50),
            'Lost Commodity Costs': np.random.uniform(0, 50000, size=50),
            'Public/Private Property Damage Costs': np.random.uniform(0, 30000, size=50),
            'Emergency Response Costs': np.random.uniform(0, 1000000, size=50),
            'Environmental Remediation Costs': np.random.uniform(0, 2000000, size=50),
            'Other Costs': np.random.uniform(0, 100000, size=50),
            'Accident Longitude': np.random.uniform(-100, -80, size=50),
            'Accident Latitude': np.random.uniform(25, 50, size=50)
})


            encoded_features = encoder.transform([most_common_categories] * 50)

            # Concatenate numerical features and encoded categorical features to ensure 21 features
            X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 
                                                  'Net Loss (Barrels)', 'Property Damage Costs', 'Lost Commodity Costs', 
                                                  'Public/Private Property Damage Costs', 'Emergency Response Costs', 
                                                  'Environmental Remediation Costs', 'Other Costs']],
                                  encoded_features))
            
            # Predict `All Costs` for each individual point in X_future
            all_costs_pred = model.predict(X_future)
            synthetic_data['All Costs'] = all_costs_pred
            print(f"Predictions for year {year}: {all_costs_pred[:5]}...")  # Display first few predictions for verification

            incidents = int(np.random.uniform(100, 400))
            liquid_recovery = float(synthetic_data['Liquid Recovery (Barrels)'].sum())
            net_loss = float(synthetic_data['Net Loss (Barrels)'].sum())
            all_costs = float(all_costs_pred.sum())
        else:
            # Use historical data for years up to 2017
            year_data = data[data['Year'] == year]
            incidents = int(year_data.shape[0])
            liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
            net_loss = float(year_data['Net Loss (Barrels)'].sum())
            all_costs = float(year_data['All Costs'].sum())
            synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]

        year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)  # Ensure native int
        
        # Add data to the line chart
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

        # Normalize values for the spider chart
        normalized_incidents = normalize_value(incidents, min_incidents, max_incidents)
        normalized_liquid_recovery = normalize_value(liquid_recovery, min_liquid_recovery, max_liquid_recovery)
        normalized_net_loss = normalize_value(net_loss, min_net_loss, max_net_loss)
        normalized_all_costs = normalize_value(all_costs, min_all_costs, max_all_costs)

        print(f"Normalized Incidents: {normalized_incidents}, Normalized Liquid Recovery: {normalized_liquid_recovery}, "
              f"Normalized Net Loss: {normalized_net_loss}, Normalized All Costs: {normalized_all_costs}")

        # Update spider chart with normalized values
        spider_series.add_points([
            {'axis': 'Incidents', 'value': normalized_incidents},
            {'axis': 'Average Liquid Recovery', 'value': normalized_liquid_recovery},
            {'axis': 'Average Net Loss', 'value': normalized_net_loss},
            {'axis': 'All Costs', 'value': normalized_all_costs}
        ])
        spider_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')

        # Pause for real-time simulation
        time.sleep(5)

# Open the dashboard and start updating
dashboard.open(live=True)
update_dashboard()
