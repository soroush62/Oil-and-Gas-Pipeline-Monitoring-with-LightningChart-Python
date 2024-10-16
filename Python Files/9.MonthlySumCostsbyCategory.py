import pandas as pd
import lightningchart as lc
from datetime import datetime, timedelta

lc.set_license('my-license-key')

file_path = 'Dataset/database.csv' 
data = pd.read_csv(file_path)

data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'], format='%m/%d/%Y %H:%M')
data['relative_month'] = ((data['Accident Date/Time'].dt.year - 2010) * 12 + 
                           data['Accident Date/Time'].dt.month - 1)

monthly_costs = data.groupby(['relative_month']).agg({
    'Emergency Response Costs': 'sum',
    'Environmental Remediation Costs': 'sum',
    'Property Damage Costs': 'sum',
    'Lost Commodity Costs': 'sum',
    'Public/Private Property Damage Costs': 'sum',
    'All Costs': 'sum'
}).reset_index()

start_date = datetime(2010, 1, 1)
monthly_costs['timestamp'] = [(start_date + timedelta(days=month * 30)).timestamp() * 1000 for month in monthly_costs['relative_month']]

chart = lc.ChartXY(
    theme=lc.Themes.White,
    title="Monthly Sum Costs by Category"
)

categories = [
    ('Emergency Response Costs', 'yellow', 'Emergency'),
    ('Environmental Remediation Costs', 'green', 'Environment'),
    ('Property Damage Costs', 'blue', 'Property'),
    ('Lost Commodity Costs', 'red', 'Commodity'),
    ('Public/Private Property Damage Costs', 'cyan', 'Public/Private Prop.'),
    ('All Costs', 'black', 'All')
]
legend=chart.add_legend()
for category, color, label in categories:
    series = chart.add_line_series(data_pattern='ProgressiveX')
    series.set_name(label)
    series.set_line_thickness(2)
    series.add(monthly_costs['timestamp'].tolist(), monthly_costs[category].tolist())
    legend.add(series)
    
# Customize axes
x_axis = chart.get_default_x_axis()
x_axis.set_title('Month (DateTime)')
x_axis.set_tick_strategy('DateTime')

y_axis = chart.get_default_y_axis()
y_axis.set_title('Sum Cost ($Millions)')

annotations = [
    (datetime(2010, 7, 1).timestamp() * 1000, 840, 'Enbridge Energy\nMarshall, MI'),
    (datetime(2011, 5, 1).timestamp() * 1000, 135, 'ExxonMobil\nLaurel, MT'),
    (datetime(2012, 9, 1).timestamp() * 1000, 91, 'Mobil\nMayflower, AR'),
    (datetime(2014, 5, 1).timestamp() * 1000, 143, 'Plains Pipeline Co\nGoleta, CA'),
    (datetime(2016, 1, 1).timestamp() * 1000, 66, 'Colonial Pipeline\nHelena, AL')
]



chart.open()
