import pandas as pd
import numpy as np
import lightningchart as lc
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import time
from datetime import datetime

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
data['Year'] = data['Accident Date/Time'].dt.year
data = data[data['Year'] <= 2017]

historical_min = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].min()
historical_max = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].max()

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
categorical_features = encoder.fit_transform(data[['Pipeline Type', 'Cause Category']])

X = np.hstack((data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)']], categorical_features))
y = data['All Costs']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

most_common_categories = data[['Pipeline Type', 'Cause Category']].mode().iloc[0].tolist()

scaler = MinMaxScaler(feature_range=(0, 10))
historical_values = data[['Unintentional Release (Barrels)', 'Liquid Recovery (Barrels)', 'Net Loss (Barrels)', 'All Costs']].values
scaler.fit(historical_values)

dashboard = lc.Dashboard(theme=lc.Themes.TurquoiseHexagon, rows=2, columns=3)

stacked_area_chart = dashboard.ChartXY(row_index=0, column_index=0, column_span=2)
stacked_area_chart.set_title("Annual Analysis of Pipeline Incidents and Impact Metrics")
x_axis = stacked_area_chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)
legend = stacked_area_chart.add_legend()

colors = [lc.Color(255, 204, 0), lc.Color(255, 102, 0), lc.Color(255, 51, 0), lc.Color(204, 0, 0)]
metrics = ['Incidents', 'Liquid Recovery', 'Net Loss', 'All Costs']
series_dict = {}

for i, metric in enumerate(metrics):
    series = stacked_area_chart.add_area_series(data_pattern='ProgressiveX')
    series.set_name(metric).set_fill_color(color=colors[i])
    legend.add(series)
    series_dict[metric] = series

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

spider_chart = dashboard.SpiderChart(row_index=0, column_index=2)
spider_chart.set_title('Incident Metrics')
spider_chart.add_axis("Number of Incidents")
spider_chart.add_axis("Liquid Recovery (Barrels)")
spider_chart.add_axis("Net Loss (Barrels)")
spider_chart.add_axis("Predicted All Costs")
spider_chart.set_axis_label_font(weight='bold', size=10)

last_spider_series = None

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
        
        year_timestamp = int(datetime(year, 1, 1).timestamp() * 1000)
        series_dict['Incidents'].add([year_timestamp], [scaled_values[0]])
        series_dict['Liquid Recovery'].add([year_timestamp], [scaled_values[1]])
        series_dict['Net Loss'].add([year_timestamp], [scaled_values[2]])
        series_dict['All Costs'].add([year_timestamp], [scaled_values[3]])

        if incidents > 0:
            recovery_rate = (liquid_recovery / (liquid_recovery + net_loss)) * 100
        else:
            recovery_rate = 0

        recovery_gauge.set_value(recovery_rate)

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

        incident_density, lon_edges, lat_edges = np.histogram2d(
            synthetic_data['Accident Longitude'], 
            synthetic_data['Accident Latitude'], 
            bins=[100, 100], 
            weights=synthetic_data['All Costs']
        )
        heatmap.invalidate_intensity_values(incident_density.tolist())
        heatmap_chart.set_title(f'Geospatial Analysis of All Costs Over Time in year {year}')
        
        time.sleep(3)

dashboard.open(live=True)
update_dashboard()

