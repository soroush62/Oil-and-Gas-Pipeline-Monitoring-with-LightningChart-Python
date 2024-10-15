import pandas as pd
import lightningchart as lc

lc.set_license('my-license-key')

file_path = 'Dataset/database.csv'
data = pd.read_csv(file_path)

data['Accident Date/Time'] = pd.to_datetime(data['Accident Date/Time'])

data['Year'] = data['Accident Date/Time'].dt.year.astype(str)

categories = ['Pipeline Type', 'Liquid Type']

chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.Light,
    title='Incident Frequency by Category Over the Years (Stacked Bar Chart)'
)
chart.set_sorting('alphabetical') 

for category in categories:
    filtered_data = data.dropna(subset=[category])
    category_year_data = filtered_data.groupby(['Year', category]).size().unstack(fill_value=0)

    x_values = category_year_data.index.tolist()
    stacked_data = []
    for subCategory in category_year_data.columns:
        sub_category_values = category_year_data[subCategory].values.tolist()
        stacked_data.append({
            'subCategory': subCategory,
            'values': sub_category_values,
        })

    chart.set_data_stacked(x_values, stacked_data)
    
    chart.set_title(f'Incident Frequency by {category} Over the Years')
    chart.set_value_label_display_mode('hidden')
    chart.set_label_rotation(45)
    chart.add_legend().add(chart)
    chart.open()
