import lightningchart as lc
import pandas as pd
from datetime import datetime

# Load your license
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)

# Convert "Accident Date/Time" to datetime and extract year
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
data['Year'] = data['Accident Date/Time'].dt.year

# Aggregate data by year
aggregated_data = data.groupby('Year').agg({
    'Accident Year': 'count',  # Number of incidents
    'Liquid Recovery (Barrels)': 'sum',
    'Net Loss (Barrels)': 'sum',
    'All Costs': 'sum'
}).reset_index()
aggregated_data.columns = ['Year', 'Incidents', 'Liquid Recovery', 'Net Loss', 'All Costs']

# Prepare X-axis values (convert years to datetime format in milliseconds)
x_values = [int(datetime(year, 1, 1).timestamp() * 1000) for year in aggregated_data['Year']]

# Create a ChartXY
chart = lc.ChartXY(
    theme=lc.Themes.Black,
    title='Annual Analysis of Pipeline Incidents and Impact Metrics'
)

# Remove default Y-axis
chart.get_default_y_axis().dispose()

# Add Legend
legend = chart.add_legend()

# Define features and Y-axes
features = {
    'Incidents': 'Number of Incidents',
    'Liquid Recovery': 'Liquid Recovery (Barrels)',
    'Net Loss': 'Net Loss (Barrels)',
    'All Costs': 'All Costs (USD)'
}

# Add each feature to the chart with its own Y-axis
for i, (feature, y_title) in enumerate(features.items()):
    y_axis = chart.add_y_axis(stack_index=i)
    y_axis.set_title(y_title)
    
    # Plot each feature with corresponding data
    y_values = aggregated_data[feature].tolist()
    series = chart.add_line_series(y_axis=y_axis, data_pattern='ProgressiveX')
    series.add(x_values, y_values)
    series.set_name(y_title)
    legend.add(series)

# Set X-axis
x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)

# Open the chart
chart.open()
