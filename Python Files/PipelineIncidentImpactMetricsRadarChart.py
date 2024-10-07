import numpy as np
import pandas as pd
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)
data['Year'] = pd.to_datetime(data['Accident Date/Time']).dt.year

aggregated_data = data.groupby('Year').agg({
    'Accident Year': 'count',
    'Liquid Recovery (Barrels)': 'mean',
    'Net Loss (Barrels)': 'mean',
    'All Costs': 'mean'
}).reset_index()
aggregated_data.columns = ['Year', 'Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']

scaled_data = aggregated_data.copy()
for column in ['Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']:
    min_val = scaled_data[column].min()
    max_val = scaled_data[column].max()
    scaled_data[column] = (scaled_data[column] - min_val) / (max_val - min_val) * 10 

chart = lc.SpiderChart(
    theme=lc.Themes.White,
    title='Pipeline Incident Impact Metrics Over Time'
)
chart.set_axis_label_font(weight='bold', size=15)
chart.set_nib_style(thickness=5, color=lc.Color(0, 0, 0))

metrics = ['Incidents', 'Average Liquid Recovery', 'Average Net Loss', 'All Costs']
for metric in metrics:
    chart.add_axis(metric)

series_list = []
for _, row in scaled_data.iterrows():
    series = chart.add_series()
    series.set_name(f"Year {int(row['Year'])}")
    series.add_points([
        {'axis': metric, 'value': row[metric]} for metric in metrics
    ])
    series_list.append(series)

legend = chart.add_legend()
for series in series_list:
    legend.add(data=series)

chart.open()
