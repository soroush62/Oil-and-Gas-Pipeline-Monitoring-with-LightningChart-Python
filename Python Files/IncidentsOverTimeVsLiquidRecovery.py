import pandas as pd
import lightningchart as lc
from datetime import datetime

# Load your LightningChart license key
lc.set_license(open('../license-key').read())

# Load the dataset
file_path = 'Dataset/database.csv'  # Update with your actual file path
data = pd.read_csv(file_path)

# Convert 'Accident Date/Time' to datetime format
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])

# Group by month/year and sum or average 'Liquid Recovery (Barrels)'
data['year_month'] = data['Accident Date/Time'].dt.to_period('M')
monthly_recovery = data.groupby('year_month')['Liquid Recovery (Barrels)'].sum().reset_index()

# Convert 'year_month' to timestamps (in milliseconds)
monthly_recovery['timestamp'] = [int(datetime(year.year, year.month, 1).timestamp()) * 1000 for year in monthly_recovery['year_month']]

# Extract x and y values for plotting
x_values = monthly_recovery['timestamp'].tolist()
y_values_recovery = monthly_recovery['Liquid Recovery (Barrels)'].tolist()

# Prepare Y-axis for Date representation (left Y-axis)
monthly_incidents = data.groupby('year_month').size().reset_index(name='incident_count')
y_values_incidents = monthly_incidents['incident_count'].tolist()

# Initialize the chart
chart = lc.ChartXY(theme=lc.Themes.Dark, title="Incidents Over Time vs Liquid Recovery")
x_axis = chart.get_default_x_axis()
x_axis.set_title("Incident Date").set_tick_strategy('DateTime', utc=True)
y_axis_left = chart.get_default_y_axis()
y_axis_left.set_title("Number of Incidents")

# Add a secondary Y-axis for 'Liquid Recovery (Barrels)'
y_axis_right = chart.add_y_axis(opposite=True)
y_axis_right.set_title("Liquid Recovery (Barrels)")

# Add Line series for incidents over time on the primary Y-axis
incident_series = chart.add_line_series()
incident_series.set_name("Incident Frequency")
incident_series.add(x_values, y_values_incidents)

# Add Area series for 'Liquid Recovery (Barrels)' on the secondary Y-axis
recovery_series = chart.add_area_series(y_axis=y_axis_right)
recovery_series.set_name("Liquid Recovery (Barrels)")
recovery_series.add(x_values, y_values_recovery)

# Customize the appearance
recovery_series.set_fill_color(lc.Color(0, 128, 255, 128))  # Semi-transparent blue
recovery_series.set_line_color(lc.Color(0, 128, 255, 128))  # Semi-transparent blue line
incident_series.set_line_color(lc.Color(255, 255, 0))  # Yellow line for contrast

# Add a legend
legend = chart.add_legend()
legend.add(incident_series)
legend.add(recovery_series)

# Open the chart
chart.open()
