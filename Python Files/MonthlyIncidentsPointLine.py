# import lightningchart as lc
# import pandas as pd
# import numpy as np
# from datetime import datetime

# lc.set_license(open('../license-key').read())

# data = pd.read_csv('Dataset/database.csv')
# data = pd.DataFrame(data)

# data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
# accident_date_year = data['Accident Date/Time'].dt.year
# accident_date_year_month = data['Accident Date/Time'].dt.to_period('M')
# accident_date_month = data['Accident Date/Time'].dt.month

# print(data['Accident Date/Time'])
# print(f' Accident Date/Time in year: {accident_date_year}')
# print(f' Accident Date/Time in year_month: {accident_date_year_month}')
# print(f' Accident Date/Time in month: {accident_date_month}')


# # let's count the number of accidents in each year
# accidents_in_each_year = data['Accident Year'].value_counts().sort_index()
# accident_date_year_ms = [int(datetime(year, 1, 1).timestamp()) * 1000 for year in accidents_in_each_year.index]
# print(f'Accidents in each year in milliseconds: {accident_date_year_ms}')

# chart=lc.ChartXY(theme=lc.Themes.Dark, title="Accidents in each year")
# series = chart.add_point_line_series()
# series.add(accident_date_year_ms, accidents_in_each_year.tolist())
# x_axis=chart.get_default_x_axis().set_tick_strategy('DateTime', utc=True)
# chart.open()



import pandas as pd
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

import pandas as pd
import lightningchart as lc

file_path = 'Dataset/database.csv'  
data = pd.read_csv(file_path)

data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])

data['year_month'] = data['Accident Date/Time'].dt.to_period('M')

monthly_incidents = data.groupby('year_month').size().reset_index(name='incident_count')

monthly_incidents['timestamp'] = monthly_incidents['year_month'].dt.start_time.astype('int64') // 10**6 

x_values = monthly_incidents['timestamp'].tolist() 
y_values = monthly_incidents['incident_count'].values.tolist()  

min_timestamp = min(x_values) // 1000

chart = lc.ChartXY(theme=lc.Themes.Dark, title='Monthly Incidents of Oil Pipeline Leaks and Spills')

x_axis = chart.get_default_x_axis()
x_axis.set_title('Month').set_tick_strategy('DateTime', time_origin=min_timestamp)

chart.get_default_y_axis().set_title('Number of Incidents')

point_line_series = chart.add_point_line_series(data_pattern='ProgressiveX')
point_line_series.set_point_size(8).set_point_shape('Triangle').set_point_color(lc.Color('orange'))

point_line_series.add(x_values, y_values)

chart.open()


