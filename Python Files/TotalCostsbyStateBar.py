import pandas as pd
import lightningchart as lc

# Load your license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load your dataset
file_path = 'Dataset/database.csv'  # Update this with the actual file path to your dataset
data = pd.read_csv(file_path)

# Group by 'Accident State' and sum the 'All Costs' for each state
state_costs = data.groupby('Accident State')['All Costs'].sum().sort_values(ascending=False)

# Prepare data for the bar chart
chart_data = [{'category': state, 'value': int(cost)} for state, cost in zip(state_costs.index, state_costs.values)]

# Create the bar chart
chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.White,
    title='Total Costs by State'
)

# Set sorting to 'disabled' to retain the order by cost
chart.set_sorting('descending')

# Rotate labels for better readability and set data
chart.set_label_rotation(90)
chart.set_data(chart_data)

# Open the chart
chart.open()
