import pandas as pd
import lightningchart as lc
from datetime import datetime

# Load your LightningChart license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/database.csv'  # Update this with your actual file path
data = pd.read_csv(file_path)

# Convert the "Accident Date/Time" column to datetime format
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'], format='%m/%d/%Y %H:%M')

# Extract year from the Accident Date/Time for grouping
data['year'] = data['Accident Date/Time'].dt.year

# Group the data by year and sum up Net Loss (Barrels) and Total Costs (USD)
annual_data = data.groupby('year').agg({
    'Net Loss (Barrels)': 'sum',
    'All Costs': 'sum'  # Replace 'All Costs' with the actual column name for total costs
}).reset_index()
print(annual_data)
# Create a LightningChart XY chart with two Y axes
chart = lc.ChartXY(theme=lc.Themes.Dark, title="Annual Net Loss (Barrels) vs Total Costs (USD)")

# Y-axis 1 (Left) for Net Loss (Barrels)
y_axis_loss = chart.get_default_y_axis()
y_axis_loss.set_title("Net Loss (Barrels)")

# Y-axis 2 (Right) for Total Costs (USD)
y_axis_costs = chart.add_y_axis(opposite=True)
y_axis_costs.set_title("Total Costs (USD)")

# Create an area series for Net Loss (Barrels)
series_loss = chart.add_area_series()
series_loss.set_name('Net Loss (Barrels)')
series_loss.set_fill_color(lc.Color(255, 102, 102))  # Light green
series_loss.set_line_color(lc.Color(255, 102, 102))  # Light green line

# Create a line series for Total Costs (USD)
series_costs = chart.add_point_line_series(y_axis=y_axis_costs)
series_costs.set_name('Total Costs (USD)')
series_costs.set_point_shape('triangle').set_point_size(6).set_line_thickness(2).set_line_color(lc.Color(255, 255, 0))  # Yellow

# Prepare the X and Y data for both series
x_values = [int(datetime(year, 1, 1).timestamp()) * 1000 for year in annual_data['year']]
y_values_loss = annual_data['Net Loss (Barrels)'].tolist()
y_values_costs = annual_data['All Costs'].tolist()  # Replace 'All Costs' with the correct column name

# Add data to the series
series_loss.add(x=x_values, y=y_values_loss)
series_costs.add(x=x_values, y=y_values_costs)

# Configure the X-axis as a datetime axis
x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)

# Add a constant line at 0 to the Net Loss axis
y_axis_loss.add_constant_line().set_value(0).set_stroke(2, lc.Color(255, 0, 0))  # Red constant line at 0

# Add a legend to the chart
legend = chart.add_legend()
legend.set_margin(70)
legend.add(series_loss)
legend.add(series_costs)
legend.set_margin(120)

# Open the chart
chart.open()

