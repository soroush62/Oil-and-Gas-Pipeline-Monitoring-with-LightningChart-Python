import pandas as pd
import lightningchart as lc
from datetime import datetime

lc.set_license('my-license-key')

file_path = 'Dataset/database.csv' 
data = pd.read_csv(file_path)

data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])

data['year_month'] = data['Accident Date/Time'].dt.to_period('M')
monthly_recovery = data.groupby('year_month')['Liquid Recovery (Barrels)'].sum().reset_index()

monthly_recovery['timestamp'] = [int(datetime(year.year, year.month, 1).timestamp()) * 1000 for year in monthly_recovery['year_month']]

x_values = monthly_recovery['timestamp'].tolist()
y_values_recovery = monthly_recovery['Liquid Recovery (Barrels)'].tolist()

monthly_incidents = data.groupby('year_month').size().reset_index(name='incident_count')
y_values_incidents = monthly_incidents['incident_count'].tolist()

chart = lc.ChartXY(theme=lc.Themes.Dark, title="Incidents Over Time vs Liquid Recovery")
x_axis = chart.get_default_x_axis()
x_axis.set_title("Incident Date").set_tick_strategy('DateTime', utc=True)
y_axis_left = chart.get_default_y_axis()
y_axis_left.set_title("Number of Incidents")

y_axis_right = chart.add_y_axis(opposite=True)
y_axis_right.set_title("Liquid Recovery (Barrels)")

incident_series = chart.add_line_series()
incident_series.set_name("Incident Frequency")
incident_series.add(x_values, y_values_incidents)

recovery_series = chart.add_area_series(y_axis=y_axis_right)
recovery_series.set_name("Liquid Recovery (Barrels)")
recovery_series.add(x_values, y_values_recovery)

recovery_series.set_fill_color(lc.Color(0, 128, 255, 128))  
recovery_series.set_line_color(lc.Color(0, 128, 255, 128)) 
incident_series.set_line_color(lc.Color(255, 255, 0)) 

legend = chart.add_legend()
legend.add(incident_series)
legend.add(recovery_series)
legend.set_margin(70)

chart.open()
