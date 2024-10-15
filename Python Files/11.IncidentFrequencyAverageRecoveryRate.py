import pandas as pd
import numpy as np
import lightningchart as lc
from datetime import datetime

lc.set_license('my-license-key')

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
data['Year'] = data['Accident Date/Time'].dt.year

data['Severity Level'] = pd.cut(
    data['Unintentional Release (Barrels)'],
    bins=[0, 50, 200, np.inf],
    labels=['Minor', 'Moderate', 'Severe']
)

incident_counts = data.groupby('Year').size()
avg_recovery_rate = data.groupby('Year')['Liquid Recovery (Barrels)'].mean()
severity_counts = data.groupby(['Year', 'Severity Level']).size().unstack(fill_value=0)

timestamps = [int(datetime(year, 1, 1).timestamp() * 1000) for year in incident_counts.index]

severity_proportions = severity_counts.div(severity_counts.sum(axis=1), axis=0)

chart = lc.ChartXY(
    theme=lc.Themes.Dark, 
    title="Incident Frequency and Average Recovery Rate Over Time"
)

incident_series = chart.add_point_line_series()
incident_series.set_name("Incident Frequency")
incident_series.set_line_color(lc.Color('yellow'))  # yellow color
incident_series.set_point_shape('Triangle').set_point_size(8)
incident_series.add(x=timestamps, y=incident_counts.values.tolist())

y_axis_left = chart.get_default_y_axis()
y_axis_left.set_title("Incident Frequency")

y_axis_right_1 = chart.add_y_axis(opposite=True)
y_axis_right_1.set_title("Average Recovery Rate (Barrels)")
recovery_series = chart.add_point_line_series(y_axis=y_axis_right_1)
recovery_series.set_name("Average Recovery Rate")
recovery_series.set_line_color(lc.Color(0, 255, 0))  # Green color
recovery_series.set_point_shape('Circle').set_point_size(8)
recovery_series.add(x=timestamps, y=avg_recovery_rate.values.tolist())

y_axis_right_2 = chart.add_y_axis(opposite=True)
y_axis_right_2.set_title("Proportion of Incidents by Severity")

severity_colors = {
    'Minor': lc.Color(135, 206, 235, 128),      # Light blue
    'Moderate': lc.Color(255, 160, 122, 128),   # Light salmon
    'Severe': lc.Color(144, 238, 144, 128)      # Light green
}
legend = chart.add_legend()
for severity_level in severity_proportions.columns:
    area_series = chart.add_area_series(y_axis=y_axis_right_2)
    area_series.set_name(severity_level)
    area_series.set_fill_color(severity_colors[severity_level])
    area_series.add(x=timestamps, y=severity_proportions[severity_level].values.tolist())
    legend.add(area_series)

x_axis = chart.get_default_x_axis()
x_axis.set_title("Year")
x_axis.set_tick_strategy("DateTime")


legend.add(incident_series).add(recovery_series)
legend.set_margin(140)
chart.open()
