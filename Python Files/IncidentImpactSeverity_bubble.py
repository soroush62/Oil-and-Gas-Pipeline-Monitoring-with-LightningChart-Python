import lightningchart as lc
import pandas as pd
import numpy as np
from datetime import datetime

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data['Accident Date/Time']).dt.to_period('M').dt.to_timestamp()  # Convert date to start of each month
monthly_data = data.groupby('Date').agg({
    'All Costs': 'sum',
    'Net Loss (Barrels)': 'sum',
}).reset_index()

monthly_data['ColorValue'] = np.log1p(monthly_data['All Costs']) / np.log1p(monthly_data['All Costs']).max()  
monthly_data['BubbleSize'] = (monthly_data['Net Loss (Barrels)'] / monthly_data['Net Loss (Barrels)'].max()) * 100  
print(monthly_data['BubbleSize'])

chart = lc.ChartXY(
    theme=lc.Themes.White,
    title='Monthly Incident Impact and Severity'
)

series = chart.add_point_series(
    sizes=True,
    rotations=True,
    lookup_values=True,
)
x_values = monthly_data['Date'].apply(lambda x: int(x.timestamp() * 1000)).tolist()  
y_values = monthly_data['Net Loss (Barrels)'].tolist()
sizes = monthly_data['BubbleSize'].tolist()
lookup_values = monthly_data['ColorValue'].tolist()

series.append_samples(
    x_values=x_values,
    y_values=y_values,
    sizes=sizes,
    lookup_values=lookup_values
)

series.set_individual_point_color_enabled(enabled=True)
series.set_palette_colors(
    steps=[
        {'value': 0.0, 'color': lc.Color(0, 0, 128, 128)},     
        {'value': 0.25, 'color': lc.Color(0, 128, 255, 128)},   
        {'value': 0.5, 'color': lc.Color(0, 255, 0, 128)},    
        {'value': 0.7, 'color': lc.Color(255, 255, 0, 128)},   
        {'value': 0.75, 'color': lc.Color(255, 165, 0, 128)},  
        {'value': 0.8, 'color': lc.Color(255, 0, 0, 128)},   
    ],
    look_up_property='value',
    percentage_values=True
)

x_axis = chart.get_default_x_axis()
x_axis.set_tick_strategy('DateTime', utc=True)  
x_axis.set_title('Date (Monthly)')

y_axis = chart.get_default_y_axis().set_title('Net Loss (Barrels)')

legend=chart.add_legend()
legend.add(series).set_title('Total Costs')

chart.open()
