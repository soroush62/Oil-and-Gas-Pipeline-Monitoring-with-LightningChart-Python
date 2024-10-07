import pandas as pd
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

file_path = 'Dataset/database.csv'  
data = pd.read_csv(file_path)

cause_counts = data['Cause Subcategory'].value_counts()

chart_data = [{'category': cause, 'value': int(count)} for cause, count in zip(cause_counts.index, cause_counts.values)]

chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.White,
    title='Cause Subcategory Counts'
)

chart.set_sorting('disabled')

chart.set_label_rotation(90)
chart.set_data(chart_data)

# Open the chart
chart.open()
