# import lightningchart as lc
# import pandas as pd
# import numpy as np

# lc.set_license(open('../license-key').read())

# data = pd.read_csv('Dataset/database.csv')
# data = pd.DataFrame(data)
# # print(data)

# accident = data['Accident Year'].unique()
# # print(accident)



# # let's count the number of accidents in each year
# accidents_in_each_year = data['Accident Year'].value_counts().tolist()


# chart=lc.ChartXY(theme=lc.Themes.Dark, title="Accidents in each year")
# series = chart.add_point_line_series()
# series.add(accident, accidents_in_each_year)
# x_axis=chart.get_default_x_axis().set_tick_strategy('Numeric')
# chart.open()



import pandas as pd
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

import pandas as pd
import lightningchart as lc

# Load the dataset
file_path = 'Dataset/database.csv'  # Update this with your actual file path
data = pd.read_csv(file_path)

# Convert the "Accident Date/Time" column to datetime format
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'], format='%m/%d/%Y %H:%M')

# Extract month and year for grouping
data['year_month'] = data['Accident Date/Time'].dt.to_period('M')

# Count the number of incidents per month
monthly_incidents = data.groupby('year_month').size().reset_index(name='incident_count')

# Convert Period to timestamp in milliseconds (beginning of the month)
monthly_incidents['timestamp'] = monthly_incidents['year_month'].dt.start_time.astype('int64') // 10**6  # Convert to Unix timestamp in milliseconds

# Prepare x and y values for plotting
x_values = monthly_incidents['timestamp'].tolist()  # Unix timestamps in milliseconds
y_values = monthly_incidents['incident_count'].values.tolist()  # Incident counts

# Fix: Set time_origin using the actual minimum timestamp value, and divide by 1000 for seconds (not nanoseconds)
min_timestamp = min(x_values) // 1000

# Create a chart
chart = lc.ChartXY(theme=lc.Themes.Dark, title='Monthly Incidents of Oil Pipeline Leaks and Spills')

# Configure the x-axis to use DateTime and set the time origin to milliseconds (time_origin is in seconds)
x_axis = chart.get_default_x_axis()
x_axis.set_title('Month').set_tick_strategy('DateTime', time_origin=min_timestamp)

# Configure the y-axis for incident count
chart.get_default_y_axis().set_title('Number of Incidents')

# Create a line series for the incidents
point_line_series = chart.add_point_line_series(data_pattern='ProgressiveX')
point_line_series.set_point_size(8).set_point_shape('Triangle').set_point_color(lc.Color('orange'))

# Add data to the series
point_line_series.add(x_values, y_values)

# Open the chart
chart.open()
