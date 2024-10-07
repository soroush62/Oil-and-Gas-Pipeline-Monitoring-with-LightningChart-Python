import pandas as pd
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/database.csv' 
data = pd.read_csv(file_path)

state_costs = data.groupby('Accident State')['All Costs'].sum().sort_values(ascending=False)

chart_data = [{'category': state, 'value': int(cost)} for state, cost in zip(state_costs.index, state_costs.values)]

chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.White,
    title='Total Costs by State'
)

chart.set_sorting('descending')

chart.set_label_rotation(90)
chart.set_data(chart_data)
chart.set_value_label_font_size(10)

chart.open()
