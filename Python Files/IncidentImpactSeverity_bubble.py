import lightningchart as lc
import pandas as pd
import numpy as np
from datetime import datetime

# Load the license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load your dataset
file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)

# Preprocess data - aggregate by month instead of year
data['Date'] = pd.to_datetime(data['Accident Date/Time']).dt.to_period('M').dt.to_timestamp()  # Convert date to start of each month
monthly_data = data.groupby('Date').agg({
    'All Costs': 'sum',
    'Net Loss (Barrels)': 'sum',
}).reset_index()

# Normalizing columns for visualization
monthly_data['ColorValue'] = np.log1p(monthly_data['All Costs']) / np.log1p(monthly_data['All Costs']).max()  # Log normalization for 'All Costs'
monthly_data['BubbleSize'] = (monthly_data['Net Loss (Barrels)'] / monthly_data['Net Loss (Barrels)'].max()) * 100  # Normalize size for bubbles
print(monthly_data['BubbleSize'])
# Create the chart
chart = lc.ChartXY(
    theme=lc.Themes.White,
    title='Monthly Incident Impact and Severity'
)

# Adding Point Series for bubble chart
series = chart.add_point_series(
    sizes=True,
    rotations=True,
    lookup_values=True,
)
print(np.array(range(10,50)))
# Set up values based on your dataset
x_values = monthly_data['Date'].apply(lambda x: int(x.timestamp() * 1000)).tolist()  # X-axis as monthly date in milliseconds
y_values = monthly_data['Net Loss (Barrels)'].tolist()  # Y-axis as Net Loss or other metric
sizes = monthly_data['BubbleSize'].tolist()  # Bubble sizes based on Net Loss
lookup_values = monthly_data['ColorValue'].tolist()  # Color gradient based on normalized 'All Costs'

# Append data samples
series.append_samples(
    x_values=x_values,
    y_values=y_values,
    sizes=sizes,
    lookup_values=lookup_values
)

# Configure color gradient with intermediary colors for the bubble color based on 'All Costs'
series.set_individual_point_color_enabled(enabled=True)
series.set_palette_colors(
    steps=[
        {'value': 0.0, 'color': lc.Color(0, 0, 128, 128)},       # Dark blue for very low costs
        {'value': 0.25, 'color': lc.Color(0, 128, 255, 128)},    # Light blue
        {'value': 0.5, 'color': lc.Color(0, 255, 0, 128)},       # Green for mid-low costs
        {'value': 0.7, 'color': lc.Color(255, 255, 0, 128)},    # Yellow for mid-high costs
        {'value': 0.75, 'color': lc.Color(255, 165, 0, 128)},     # Orange
        {'value': 0.8, 'color': lc.Color(255, 0, 0, 128)},       # Red for very high costs
    ],
    look_up_property='value',
    percentage_values=True
)

# Set x-axis to DateTime mode for months
x_axis = chart.get_default_x_axis()
x_axis.set_tick_strategy('DateTime', utc=True)  # Show month-year format
x_axis.set_title('Date (Monthly)')

y_axis = chart.get_default_y_axis().set_title('Net Loss (Barrels)')

legend=chart.add_legend()
legend.add(series).set_title('Total Costs')
# Open chart
chart.open()
