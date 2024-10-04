import pandas as pd
import lightningchart as lc

# Load your license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load your dataset
file_path = 'Dataset/database.csv'  # Update this with the actual file path to your dataset
data = pd.read_csv(file_path)

# Count occurrences of each unique value in the "Cause Subcategory" column
cause_counts = data['Cause Subcategory'].value_counts()

# Convert counts to regular Python int to ensure compatibility
chart_data = [{'category': cause, 'value': int(count)} for cause, count in zip(cause_counts.index, cause_counts.values)]

# Create the bar chart
chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.White,
    title='Cause Subcategory Counts'
)

# Set sorting to 'disabled' to retain the original order
chart.set_sorting('disabled')

# Increase label rotation and adjust padding
chart.set_label_rotation(90)
chart.set_data(chart_data)

# Open the chart
chart.open()
