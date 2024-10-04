import pandas as pd
import lightningchart as lc

# Set your license key here
lc.set_license(open('../license-key').read())

# Load the dataset
file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)

# Convert the 'Accident Date/Time' column to datetime
data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])

# Extract year from 'Accident Date/Time'
data['Year'] = data['Accident Date/Time'].dt.year.astype(str)

# Define the categories for analysis
categories = ['Pipeline Type', 'Liquid Type']

# Initialize the chart
chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.Light,
    title='Incident Frequency by Category Over the Years (Stacked Bar Chart)'
)
chart.set_sorting('alphabetical') 

# Loop over each category to create a stacked bar chart
for category in categories:
    # Filter and prepare data
    filtered_data = data.dropna(subset=[category])
    category_year_data = filtered_data.groupby(['Year', category]).size().unstack(fill_value=0)

    # Prepare data for the stacked bar chart
    x_values = category_year_data.index.tolist()
    stacked_data = []
    for subCategory in category_year_data.columns:
        sub_category_values = category_year_data[subCategory].values.tolist()
        stacked_data.append({
            'subCategory': subCategory,
            'values': sub_category_values,
        })

    # Set data for the chart
    chart.set_data_stacked(x_values, stacked_data)
    
    # Customize chart settings
    chart.set_title(f'Incident Frequency by {category} Over the Years')
    chart.set_value_label_display_mode('hidden')
    chart.set_label_rotation(45)
    chart.add_legend().add(chart)
    chart.open()
