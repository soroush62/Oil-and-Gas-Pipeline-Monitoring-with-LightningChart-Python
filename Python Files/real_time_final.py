# import pandas as pd
# import numpy as np
# import lightningchart as lc
# import random
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
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

# # Calculate min and max values for each metric
# historical_min = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].min()
# historical_max = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].max()
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

# # Initialize scaler for global scaling based on historical data
# scaler = MinMaxScaler(feature_range=(0, 10))
# historical_values = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].values
# scaler.fit(historical_values)

# # Create a dashboard with two rows and three columns
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# # First Row: Annual Analysis of Pipeline Incidents and Impact Metrics
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

# # First Row: Spider Chart for Each Year
# spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
# spider_chart.set_title('Yearly Impact Metrics')
# spider_chart.add_axis("Unintentional Release (Barrels)")
# spider_chart.add_axis("Liquid Recovery (Barrels)")
# spider_chart.add_axis("Net Loss (Barrels)")
# spider_chart.add_axis("Predicted All Costs")
# spider_chart.set_axis_label_font(weight='bold', size=10)

# # Variable to track the last added series
# last_spider_series = None

# # Second Row: Heatmap for Geospatial Analysis
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=3)
# heatmap = heatmap_chart.add_heatmap_grid_series(rows=100, columns=100)
# heatmap.set_palette_colors(
#     steps=[
#         {'value': 0, 'color': lc.Color(0, 0, 255)},  
#         {'value': 50000, 'color': lc.Color(0, 255, 0)}, 
#         {'value': 500000, 'color': lc.Color(255, 255, 0)}, 
#         {'value': 1000000, 'color': lc.Color(255, 178, 102)},  
#         {'value': 5000000, 'color': lc.Color(204, 102, 0)}, 
#         {'value': 10000000, 'color': lc.Color(255, 102, 102)}, 
#         {'value': 25000000, 'color': lc.Color(255, 0, 0)},
#         {'value': 25000000, 'color': lc.Color(51, 0, 51)}
#     ],
#     look_up_property='value'
# )


# heatmap_chart.get_default_x_axis().set_title('Longitude')
# heatmap_chart.get_default_y_axis().set_title('Latitude')

# def update_dashboard():
#     global last_spider_series
#     for year in range(2010, 2028):
#         print(f"Updating year: {year}")
#         if year > 2017:
#             # Generate synthetic data within historical range for future years
#             synthetic_data = pd.DataFrame({
#                 'Unintentional Release (Barrels)': np.random.uniform(historical_min['Unintentional Release (Barrels)'], 
#                                                                     historical_max['Unintentional Release (Barrels)'], 50),
#                 'Liquid Recovery (Barrels)': np.random.uniform(historical_min['Liquid Recovery (Barrels)'], 
#                                                               historical_max['Liquid Recovery (Barrels)'], 50),
#                 'Net Loss (Barrels)': np.random.uniform(historical_min['Net Loss (Barrels)'], 
#                                                         historical_max['Net Loss (Barrels)'], 50),
#                 'Accident Longitude': np.random.uniform(-100, -80, 50),
#                 'Accident Latitude': np.random.uniform(25, 50, 50)
#             })
#             encoded_features = encoder.transform([most_common_categories] * 50)
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
#                                   encoded_features))
#             all_costs_pred = model.predict(X_future)
            
#             # Introduce variability by adding a small random noise to each prediction
#             noise = np.random.normal(0, 0.05 * all_costs_pred.mean(), all_costs_pred.shape)
#             all_costs_pred += noise
            
#             # Debug: Print all costs with noise applied
#             print(f"Predicted All Costs (with noise) for year {year}: {all_costs_pred}")

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
        
#         # Normalize values to ensure all metrics are on a similar scale based on historical range
#         values = np.array([[incidents, liquid_recovery, net_loss, all_costs]])
#         scaled_values = scaler.transform(values).flatten()

#         # Update line chart
#         year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)
#         series_dict['Incidents'].add([year_timestamp], [incidents])
#         series_dict['Liquid Recovery'].add([year_timestamp], [liquid_recovery])
#         series_dict['Net Loss'].add([year_timestamp], [net_loss])
#         series_dict['All Costs'].add([year_timestamp], [all_costs])

#         # Remove last spider series if it exists
#         if last_spider_series:
#             last_spider_series.dispose()

#         # Add a new series to the spider chart for the current year
#         last_spider_series = spider_chart.add_series()
#         last_spider_series.add_points([
#             {'axis': "Unintentional Release (Barrels)", 'value': scaled_values[0]},
#             {'axis': "Liquid Recovery (Barrels)", 'value': scaled_values[1]},
#                         {'axis': "Net Loss (Barrels)", 'value': scaled_values[2]},
#             {'axis': "Predicted All Costs", 'value': scaled_values[3]}
#         ])

#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], 
#             synthetic_data['Accident Latitude'], 
#             bins=[100, 100], 
#             weights=synthetic_data['All Costs']
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
#         heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')
        
#         # Simulate real-time data update delay
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
# from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
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

# # Calculate min and max values for each metric
# historical_min = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].min()
# historical_max = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].max()

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

# # Initialize scaler for global scaling based on historical data
# scaler = MinMaxScaler(feature_range=(0, 10))
# historical_values = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].values
# scaler.fit(historical_values)

# # Create a dashboard with two rows and three columns
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# # First Row: Real-Time Stacked Area Chart
# stacked_area_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
# stacked_area_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics (Stacked Area)")
# x_axis = stacked_area_chart.get_default_x_axis()
# x_axis.set_title('Year')
# x_axis.set_tick_strategy('DateTime', utc=True)

# # Define colors for each layer and create series for the stacked area chart
# colors = [lc.Color("#FFCC00"), lc.Color("#FF6600"), lc.Color("#FF3300"), lc.Color("#CC0000")]
# metrics = ['Incidents', 'Liquid Recovery', 'Net Loss', 'All Costs']
# series_dict = {}

# for i, metric in enumerate(metrics):
#     series = stacked_area_chart.add_area_series(data_pattern='ProgressiveX')
#     series.set_name(metric).set_fill_color(color=colors[i])
#     series_dict[metric] = series

# # First Row: Spider Chart for Each Year
# spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
# spider_chart.set_title('Yearly Impact Metrics')
# spider_chart.add_axis("Unintentional Release (Barrels)")
# spider_chart.add_axis("Liquid Recovery (Barrels)")
# spider_chart.add_axis("Net Loss (Barrels)")
# spider_chart.add_axis("Predicted All Costs")
# spider_chart.set_axis_label_font(weight='bold', size=10)

# # Variable to track the last added series
# last_spider_series = None

# # Second Row: Heatmap for Geospatial Analysis
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=3)
# heatmap = heatmap_chart.add_heatmap_grid_series(rows=100, columns=100)
# heatmap.set_palette_colors(
#     steps=[
#         {'value': 0, 'color': lc.Color(0, 0, 255)},  
#         {'value': 50000, 'color': lc.Color(0, 255, 0)}, 
#         {'value': 500000, 'color': lc.Color(255, 255, 0)}, 
#         {'value': 1000000, 'color': lc.Color(255, 178, 102)},  
#         {'value': 5000000, 'color': lc.Color(204, 102, 0)}, 
#         {'value': 10000000, 'color': lc.Color(255, 102, 102)}, 
#         {'value': 25000000, 'color': lc.Color(255, 0, 0)},
#         {'value': 25000000, 'color': lc.Color(51, 0, 51)}
#     ],
#     look_up_property='value'
# )
# heatmap_chart.get_default_x_axis().set_title('Longitude')
# heatmap_chart.get_default_y_axis().set_title('Latitude')

# # Update function for the dashboard
# def update_dashboard():
#     global last_spider_series
#     for year in range(2010, 2028):
#         print(f"Updating year: {year}")
#         if year > 2017:
#             # Generate synthetic data within historical range for future years
#             synthetic_data = pd.DataFrame({
#                 'Unintentional Release (Barrels)': np.random.uniform(historical_min['Unintentional Release (Barrels)'], 
#                                                                     historical_max['Unintentional Release (Barrels)'], 50),
#                 'Liquid Recovery (Barrels)': np.random.uniform(historical_min['Liquid Recovery (Barrels)'], 
#                                                               historical_max['Liquid Recovery (Barrels)'], 50),
#                 'Net Loss (Barrels)': np.random.uniform(historical_min['Net Loss (Barrels)'], 
#                                                         historical_max['Net Loss (Barrels)'], 50),
#                 'Accident Longitude': np.random.uniform(-100, -80, 50),
#                 'Accident Latitude': np.random.uniform(25, 50, 50)
#             })
#             encoded_features = encoder.transform([most_common_categories] * 50)
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
        
#         # Normalize values to ensure all metrics are on a similar scale based on historical range
#         values = np.array([[incidents, liquid_recovery, net_loss, all_costs]])
#         scaled_values = scaler.transform(values).flatten()
        
#         # Update stacked area chart with cumulative values
#         year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)
#         series_dict['Incidents'].add([year_timestamp], [scaled_values[0]])
#         series_dict['Liquid Recovery'].add([year_timestamp], [scaled_values[1]])
#         series_dict['Net Loss'].add([year_timestamp], [scaled_values[2]])
#         series_dict['All Costs'].add([year_timestamp], [scaled_values[3]])

#         # Remove last spider series if it exists
#         if last_spider_series:
#             last_spider_series.dispose()

#         # Add a new series to the spider chart for the current year
#         last_spider_series = spider_chart.add_series()
#         last_spider_series.add_points([
#             {'axis': "Unintentional Release (Barrels)", 'value': scaled_values[0]},
#             {'axis': "Liquid Recovery (Barrels)", 'value': scaled_values[1]},
#             {'axis': "Net Loss (Barrels)", 'value': scaled_values[2]},
#             {'axis': "Predicted All Costs", 'value': scaled_values[3]}
#         ])

#                 # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], 
#             synthetic_data['Accident Latitude'], 
#             bins=[100, 100], 
#             weights=synthetic_data['All Costs']
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
#         heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')
        
#         # Simulate real-time data update delay
#         time.sleep(5)

# # Open the dashboard and start updating
# dashboard.open(live=True)
# update_dashboard()










# import pandas as pd
# import numpy as np
# import lightningchart as lc
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
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

# # Calculate min and max values for each metric
# historical_min = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].min()
# historical_max = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].max()

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

# # Initialize scaler for global scaling based on historical data
# scaler = MinMaxScaler(feature_range=(0, 10))
# historical_values = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].values
# scaler.fit(historical_values)

# # Create a dashboard with two rows and three columns
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

# # First Row: Real-Time Stacked Area Chart
# stacked_area_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
# stacked_area_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics (Stacked Area)")
# x_axis = stacked_area_chart.get_default_x_axis()
# x_axis.set_title('Year')
# x_axis.set_tick_strategy('DateTime', utc=True)
# legend=stacked_area_chart.add_legend()

# # Define colors for each layer and create series for the stacked area chart
# colors = [lc.Color(255, 204, 0), lc.Color(255, 102, 0), lc.Color(255, 51, 0), lc.Color(204, 0, 0)]
# metrics = ['Incidents', 'Liquid Recovery', 'Net Loss', 'All Costs']
# series_dict = {}

# for i, metric in enumerate(metrics):
#     series = stacked_area_chart.add_area_series(data_pattern='ProgressiveX')
#     series.set_name(metric).set_fill_color(color=colors[i])
#     legend.add(series)
#     series_dict[metric] = series
    

# # First Row: Gauge Charts for Recovery Rate and Cost-to-Incident Ratio
# recovery_gauge = dashboard.GaugeChart(row_index=1, column_index=2)
# recovery_gauge.set_title('Recovery Rate (%)')
# recovery_gauge.set_angle_interval(start=225, end=-45)
# recovery_gauge.set_interval(start=0, end=100)
# recovery_gauge.set_value_label_font(35, weight='bold')
# recovery_gauge.set_unit_label('%')
# recovery_gauge.set_value_indicators([
#     {'start': 0, 'end': 30, 'color': lc.Color(255, 0, 0)},      # Red
#     {'start': 30, 'end': 70, 'color': lc.Color(255, 255, 0)},   # Yellow
#     {'start': 70, 'end': 100, 'color': lc.Color(0, 255, 0)}     # Green
# ])
# recovery_gauge.set_bar_thickness(30)
# recovery_gauge.set_value_indicator_thickness(8)

# cost_incident_ratio_gauge = dashboard.GaugeChart(row_index=0, column_index=2)
# cost_incident_ratio_gauge.set_title('Cost-to-Incident Ratio')
# cost_incident_ratio_gauge.set_angle_interval(start=225, end=-45)
# cost_incident_ratio_gauge.set_interval(start=0, end=1000000)
# cost_incident_ratio_gauge.set_unit_label('USD/Incident').set_value_label_font(25)
# cost_incident_ratio_gauge.set_tick_font(10)
# cost_incident_ratio_gauge.set_value_indicators([
#     {'start': 0, 'end': 200000, 'color': lc.Color(0, 255, 0)},  # Green
#     {'start': 200000, 'end': 500000, 'color': lc.Color(255, 255, 0)},  # Yellow
#     {'start': 500000, 'end': 1000000, 'color': lc.Color(255, 0, 0)}  # Red
# ])
# cost_incident_ratio_gauge.set_bar_thickness(30)
# cost_incident_ratio_gauge.set_value_indicator_thickness(8)

# # Second Row: Heatmap for Geospatial Analysis
# heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=2)
# heatmap = heatmap_chart.add_heatmap_grid_series(rows=100, columns=100)
# heatmap.set_palette_colors(
#     steps=[
#         {'value': 0, 'color': lc.Color(0, 0, 255)},  
#         {'value': 50000, 'color': lc.Color(0, 255, 0)}, 
#         {'value': 500000, 'color': lc.Color(255, 255, 0)}, 
#         {'value': 1000000, 'color': lc.Color(255, 178, 102)},  
#         {'value': 5000000, 'color': lc.Color(204, 102, 0)}, 
#         {'value': 10000000, 'color': lc.Color(255, 102, 102)}, 
#         {'value': 25000000, 'color': lc.Color(255, 0, 0)},
#         {'value': 25000000, 'color': lc.Color(51, 0, 51)}
#     ],
#     look_up_property='value'
# )
# heatmap_chart.get_default_x_axis().set_title('Longitude')
# heatmap_chart.get_default_y_axis().set_title('Latitude')

# # Update function for the dashboard
# def update_dashboard():
#     for year in range(2010, 2028):
#         print(f"Updating year: {year}")
#         if year > 2017:
#             synthetic_data = pd.DataFrame({
#                 'Unintentional Release (Barrels)': np.random.uniform(historical_min['Unintentional Release (Barrels)'], 
#                                                                     historical_max['Unintentional Release (Barrels)'], 50),
#                 'Liquid Recovery (Barrels)': np.random.uniform(historical_min['Liquid Recovery (Barrels)'], 
#                                                               historical_max['Liquid Recovery (Barrels)'], 50),
#                 'Net Loss (Barrels)': np.random.uniform(historical_min['Net Loss (Barrels)'], 
#                                                         historical_max['Net Loss (Barrels)'], 50),
#                 'Accident Longitude': np.random.uniform(-100, -80, 50),
#                 'Accident Latitude': np.random.uniform(25, 50, 50)
#             })
#             encoded_features = encoder.transform([most_common_categories] * 50)
#             X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
#                                   encoded_features))
#             all_costs_pred = model.predict(X_future)

#             incidents = int(np.random.randint(100, 400))
#             liquid_recovery = float(synthetic_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(synthetic_data['Net Loss (Barrels)'].sum())
#             all_costs = float(all_costs_pred.sum())
#             synthetic_data['All Costs'] = all_costs_pred
#         else:
#             year_data = data[data['Year'] == year]
#             incidents = int(year_data.shape[0])
#             liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
#             net_loss = float(year_data['Net Loss (Barrels)'].sum())
#             all_costs = float(year_data['All Costs'].sum())
#             synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]
        
#         values = np.array([[incidents, liquid_recovery, net_loss, all_costs]])
#         scaled_values = scaler.transform(values).flatten()
        
#         # Update stacked area chart with cumulative values
#         year_timestamp = int(datetime(year, 1, 1).timestamp() *         1000)
#         series_dict['Incidents'].add([year_timestamp], [scaled_values[0]])
#         series_dict['Liquid Recovery'].add([year_timestamp], [scaled_values[1]])
#         series_dict['Net Loss'].add([year_timestamp], [scaled_values[2]])
#         series_dict['All Costs'].add([year_timestamp], [scaled_values[3]])

#         # Calculate KPI metrics for gauges
#         if incidents > 0:
#             recovery_rate = (liquid_recovery / (liquid_recovery + net_loss)) * 100  # Recovery as a percentage
#             cost_to_incident_ratio = all_costs / incidents  # Average cost per incident
#         else:
#             recovery_rate = 0
#             cost_to_incident_ratio = 0

#         # Update gauge charts with current KPI metrics
#         recovery_gauge.set_value(recovery_rate)
#         cost_incident_ratio_gauge.set_value(cost_to_incident_ratio)

#         # Update heatmap for All Costs by Longitude and Latitude
#         incident_density, lon_edges, lat_edges = np.histogram2d(
#             synthetic_data['Accident Longitude'], 
#             synthetic_data['Accident Latitude'], 
#             bins=[100, 100], 
#             weights=synthetic_data['All Costs']
#         )
#         heatmap.invalidate_intensity_values(incident_density.tolist())
#         heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')
        
#         # Simulate real-time data update delay
#         time.sleep(5)

# # Open the dashboard and start updating
# dashboard.open(live=True)
# update_dashboard()



import pandas as pd
import numpy as np
import lightningchart as lc
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
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

# Calculate min and max values for each metric
historical_min = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].min()
historical_max = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].max()

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

# Initialize scaler for global scaling based on historical data
scaler = MinMaxScaler(feature_range=(0, 10))
historical_values = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].values
scaler.fit(historical_values)

# Create a dashboard with two rows and three columns
dashboard = lc.Dashboard(theme=lc.Themes.TurquoiseHexagon, rows=2, columns=3)

# First Row: Real-Time Stacked Area Chart
stacked_area_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
stacked_area_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics (Stacked Area)")
x_axis = stacked_area_chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)
legend = stacked_area_chart.add_legend()

# Define colors for each layer and create series for the stacked area chart
colors = [lc.Color(255, 204, 0), lc.Color(255, 102, 0), lc.Color(255, 51, 0), lc.Color(204, 0, 0)]
metrics = ['Incidents', 'Liquid Recovery', 'Net Loss', 'All Costs']
series_dict = {}

for i, metric in enumerate(metrics):
    series = stacked_area_chart.add_area_series(data_pattern='ProgressiveX')
    series.set_name(metric).set_fill_color(color=colors[i])
    legend.add(series)
    series_dict[metric] = series

# First Row: Gauge Chart for Recovery Rate
recovery_gauge = dashboard.GaugeChart(row_index=1, column_index=2)
recovery_gauge.set_title('Recovery Rate (%)')
recovery_gauge.set_angle_interval(start=225, end=-45)
recovery_gauge.set_interval(start=0, end=100)
recovery_gauge.set_value_label_font(35, weight='bold')
recovery_gauge.set_unit_label('%')
recovery_gauge.set_value_indicators([
    {'start': 0, 'end': 30, 'color': lc.Color(255, 0, 0)},      # Red
    {'start': 30, 'end': 70, 'color': lc.Color(255, 255, 0)},   # Yellow
    {'start': 70, 'end': 100, 'color': lc.Color(0, 255, 0)}     # Green
])
recovery_gauge.set_bar_thickness(30)
recovery_gauge.set_value_indicator_thickness(8)

# First Row: Spider Chart for Incident Metrics
spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
spider_chart.set_title('Incident Metrics')
spider_chart.add_axis("Number of Incidents")
spider_chart.add_axis("Liquid Recovery (Barrels)")
spider_chart.add_axis("Net Loss (Barrels)")
spider_chart.add_axis("Predicted All Costs")
spider_chart.set_axis_label_font(weight='bold', size=10)

# Variable to track the last added series to the Spider Chart
last_spider_series = None

# Second Row: Heatmap for Geospatial Analysis
heatmap_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=2)
heatmap = heatmap_chart.add_heatmap_grid_series(rows=100, columns=100)
heatmap.set_palette_colors(
    steps=[
        {'value': 0, 'color': lc.Color(0, 0, 255)},  
        {'value': 50000, 'color': lc.Color(0, 255, 0)}, 
        {'value': 500000, 'color': lc.Color(255, 255, 0)}, 
        {'value': 1000000, 'color': lc.Color(255, 178, 102)},  
        {'value': 5000000, 'color': lc.Color(204, 102, 0)}, 
        {'value': 10000000, 'color': lc.Color(255, 102, 102)}, 
        {'value': 25000000, 'color': lc.Color(255, 0, 0)},
        {'value': 25000000, 'color': lc.Color(51, 0, 51)}
    ],
    look_up_property='value'
)
heatmap_chart.get_default_x_axis().set_title('Longitude')
heatmap_chart.get_default_y_axis().set_title('Latitude')

# Update function for the dashboard
def update_dashboard():
    global last_spider_series
    for year in range(2010, 2028):
        print(f"Updating year: {year}")
        if year > 2017:
            synthetic_data = pd.DataFrame({
                'Unintentional Release (Barrels)': np.random.uniform(historical_min['Unintentional Release (Barrels)'], 
                                                                    historical_max['Unintentional Release (Barrels)'], 50),
                'Liquid Recovery (Barrels)': np.random.uniform(historical_min['Liquid Recovery (Barrels)'], 
                                                              historical_max['Liquid Recovery (Barrels)'], 50),
                'Net Loss (Barrels)': np.random.uniform(historical_min['Net Loss (Barrels)'], 
                                                        historical_max['Net Loss (Barrels)'], 50),
                'Accident Longitude': np.random.uniform(-100, -80, 50),
                'Accident Latitude': np.random.uniform(25, 50, 50)
            })
            encoded_features = encoder.transform([most_common_categories] * 50)
            X_future = np.hstack((synthetic_data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], 
                                  encoded_features))
            all_costs_pred = model.predict(X_future)

            incidents = int(np.random.randint(100, 400))
            liquid_recovery = float(synthetic_data['Liquid Recovery (Barrels)'].sum())
            net_loss = float(synthetic_data['Net Loss (Barrels)'].sum())
            all_costs = float(all_costs_pred.sum())
            synthetic_data['All Costs'] = all_costs_pred
        else:
            year_data = data[data['Year'] == year]
            incidents = int(year_data.shape[0])
            liquid_recovery = float(year_data['Liquid Recovery (Barrels)'].sum())
            net_loss = float(year_data['Net Loss (Barrels)'].sum())
            all_costs = float(year_data['All Costs'].sum())
            synthetic_data = year_data[['Accident Longitude', 'Accident Latitude', 'All Costs']]
        
        values = np.array([[incidents, liquid_recovery, net_loss, all_costs]])
        scaled_values = scaler.transform(values).flatten()
        
        # Update stacked area chart with cumulative values
        year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)
        series_dict['Incidents'].add([year_timestamp], [scaled_values[0]])
        series_dict['Liquid Recovery'].add([year_timestamp], [scaled_values[1]])
        series_dict['Net Loss'].add([year_timestamp], [scaled_values[2]])
        series_dict['All Costs'].add([year_timestamp], [scaled_values[3]])

                # Update Recovery Rate Gauge
        if incidents > 0:
            recovery_rate = (liquid_recovery / (liquid_recovery + net_loss)) * 100  # Recovery as a percentage
        else:
            recovery_rate = 0

        # Update gauge with the current recovery rate
        recovery_gauge.set_value(recovery_rate)

        # Update the Spider Chart with incident metrics
        if last_spider_series:
            last_spider_series.dispose()

        last_spider_series = spider_chart.add_series()
        last_spider_series.add_points([
            {'axis': "Number of Incidents", 'value': scaled_values[0]},
            {'axis': "Liquid Recovery (Barrels)", 'value': scaled_values[1]},
            {'axis': "Net Loss (Barrels)", 'value': scaled_values[2]},
            {'axis': "Predicted All Costs", 'value': scaled_values[3]}
        ])
        spider_chart.set_title(f'Incident Metrics Over Time in year {year}')

        # Update heatmap for All Costs by Longitude and Latitude
        incident_density, lon_edges, lat_edges = np.histogram2d(
            synthetic_data['Accident Longitude'], 
            synthetic_data['Accident Latitude'], 
            bins=[100, 100], 
            weights=synthetic_data['All Costs']
        )
        heatmap.invalidate_intensity_values(incident_density.tolist())
        heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')
        
        # Simulate real-time data update delay
        time.sleep(3)

# Open the dashboard and start updating
dashboard.open(live=True)
update_dashboard()

