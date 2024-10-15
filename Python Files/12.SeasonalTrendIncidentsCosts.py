import pandas as pd
import numpy as np
import lightningchart as lc

lc.set_license(open('../license-key').read())

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])
data['Year'] = data['Accident Date/Time'].dt.year
data['Month'] = data['Accident Date/Time'].dt.month

monthly_data = data.groupby(['Year', 'Month']).agg({
    'All Costs': 'sum', 
}).reset_index()

monthly_data['Log Normalized Costs'] = np.log1p(monthly_data['All Costs'])
monthly_data['Log Normalized Costs'] = (monthly_data['Log Normalized Costs'] - monthly_data['Log Normalized Costs'].min()) / \
                                       (monthly_data['Log Normalized Costs'].max() - monthly_data['Log Normalized Costs'].min())

log_normalized_stats = monthly_data.groupby('Month')['Log Normalized Costs'].describe(
    percentiles=[0.25, 0.5, 0.75]
).rename(columns={
    '25%': 'Lower Quartile', 
    '50%': 'Median', 
    '75%': 'Upper Quartile', 
    'min': 'Lower Extreme', 
    'max': 'Upper Extreme'
})

box_data = []
for month in range(1, 13):
    box_data.append({
        'start': month - 0.4,  
        'end': month + 0.4,
        'median': log_normalized_stats.loc[month, 'Median'],
        'lowerQuartile': log_normalized_stats.loc[month, 'Lower Quartile'],
        'upperQuartile': log_normalized_stats.loc[month, 'Upper Quartile'],
        'lowerExtreme': log_normalized_stats.loc[month, 'Lower Extreme'],
        'upperExtreme': log_normalized_stats.loc[month, 'Upper Extreme'],
    })

monthly_avg_log_normalized = monthly_data.groupby('Month')['Log Normalized Costs'].mean()

chart = lc.ChartXY(
    theme=lc.Themes.Light,
    title="Seasonal Trend Analysis of Log-Normalized Incident Costs"
)

box_series = chart.add_box_series()
box_series.set_name("Monthly Log-Normalized Cost Distribution")
box_series.add_multiple(box_data)

line_series = chart.add_point_line_series()
line_series.set_name("Average Log-Normalized Monthly Cost Trend")
line_series.set_line_color(lc.Color(255, 0, 0))  

x_values = np.arange(1, 13) 
y_values = monthly_avg_log_normalized.values
line_series.add(x=x_values.tolist(), y=y_values.tolist())

x_axis = chart.get_default_x_axis()
x_axis.set_title("Month")
x_axis.set_interval(0.5, 12.5)

x_axis.set_tick_strategy('Empty')
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for i, month_name in enumerate(month_labels, start=1):
    custom_tick = x_axis.add_custom_tick()
    custom_tick.set_value(i)
    custom_tick.set_text(month_name)

y_axis = chart.get_default_y_axis()
y_axis.set_title("Log-Normalized Cost (0 to 1)")

legend = chart.add_legend()
legend.add(box_series).add(line_series)

chart.open()
