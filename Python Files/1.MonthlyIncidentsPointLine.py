import pandas as pd
import lightningchart as lc

lc.set_license(open('../license-key').read())

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


