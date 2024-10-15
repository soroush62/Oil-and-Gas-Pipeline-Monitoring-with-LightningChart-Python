import pandas as pd
import lightningchart as lc
from datetime import datetime

lc.set_license('my-license-key')

file_path = 'Dataset/database.csv' 
data = pd.read_csv(file_path)

data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'], format='%m/%d/%Y %H:%M')

data['year'] = data['Accident Date/Time'].dt.year

annual_data = data.groupby('year').agg({
    'Net Loss (Barrels)': 'sum',
    'All Costs': 'sum' 
}).reset_index()
print(annual_data)
chart = lc.ChartXY(theme=lc.Themes.Dark, title="Annual Net Loss (Barrels) vs Total Costs (USD)")

y_axis_loss = chart.get_default_y_axis()
y_axis_loss.set_title("Net Loss (Barrels)")

y_axis_costs = chart.add_y_axis(opposite=True)
y_axis_costs.set_title("Total Costs (USD)")

series_loss = chart.add_area_series()
series_loss.set_name('Net Loss (Barrels)')
series_loss.set_fill_color(lc.Color(255, 102, 102))
series_loss.set_line_color(lc.Color(255, 102, 102))  

series_costs = chart.add_point_line_series(y_axis=y_axis_costs)
series_costs.set_name('Total Costs (USD)')
series_costs.set_point_shape('triangle').set_point_size(6).set_line_thickness(2).set_line_color(lc.Color(255, 255, 0))  # Yellow

x_values = [int(datetime(year, 1, 1).timestamp()) * 1000 for year in annual_data['year']]
y_values_loss = annual_data['Net Loss (Barrels)'].tolist()
y_values_costs = annual_data['All Costs'].tolist() 

series_loss.add(x=x_values, y=y_values_loss)
series_costs.add(x=x_values, y=y_values_costs)

x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)

y_axis_loss.add_constant_line().set_value(0).set_stroke(2, lc.Color(255, 0, 0)) 

legend = chart.add_legend()
legend.set_margin(70)
legend.add(series_loss)
legend.add(series_costs)
legend.set_margin(120)

chart.open()

