# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the dataset
# data = pd.read_csv('Dataset/database.csv')

# # Extract latitude and longitude columns
# latitude = data['Accident Latitude']
# longitude = data['Accident Longitude']

# # Create a figure for the heatmap
# plt.figure(figsize=(10, 8))

# # Plot a heatmap using seaborn's kdeplot for latitude and longitude
# sns.kdeplot(
#     x=longitude,
#     y=latitude,
#     cmap="YlOrRd",
#     shade=True,
#     shade_lowest=False,
#     alpha=0.7,
#     cbar=True
# )

# # Set plot title and labels
# plt.title('Geospatial Heatmap of Oil Spills and Leaks')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')

# # Display the plot
# plt.show()



import pandas as pd
import numpy as np
import lightningchart as lc

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

data = pd.read_csv('Dataset/database.csv')

latitude = data['Accident Latitude'].dropna()
longitude = data['Accident Longitude'].dropna()

bins = [100, 100]  

incident_density, lon_edges, lat_edges = np.histogram2d(longitude, latitude, bins=bins)

lon_centers = (lon_edges[:-1] + lon_edges[1:]) / 2
lat_centers = (lat_edges[:-1] + lat_edges[1:]) / 2
grid_lon, grid_lat = np.meshgrid(lon_centers, lat_centers)

incident_density = np.nan_to_num(incident_density)

chart = lc.ChartXY(
    title='Geospatial Analysis of Oil Pipeline Spills and Leaks',
    theme=lc.Themes.Dark
)

heatmap = chart.add_heatmap_grid_series(
    rows=incident_density.shape[0],
    columns=incident_density.shape[1]
)

heatmap.set_start(x=lon_edges.min(), y=lat_edges.min())
heatmap.set_end(x=lon_edges.max(), y=lat_edges.max())
heatmap.set_step(x=(lon_edges.max() - lon_edges.min()) / incident_density.shape[1],
                 y=(lat_edges.max() - lat_edges.min()) / incident_density.shape[0])

heatmap.invalidate_intensity_values(incident_density.tolist())
# heatmap.hide_wireframe()

chart.get_default_x_axis().set_title('Longitude')
chart.get_default_y_axis().set_title('Latitude')

custom_palette = [
    {"value": np.min(incident_density), "color": lc.Color(204, 229, 255)},
    {"value": np.percentile(incident_density, 99), "color": lc.Color(0, 0, 255)},   
    {"value": np.percentile(incident_density, 99.25), "color": lc.Color(0, 255, 255)},
    {"value": np.percentile(incident_density, 99.5), "color": lc.Color(0, 255, 0)}, 
    {"value": np.percentile(incident_density, 99.75), "color": lc.Color(255, 255, 204)},
    {"value": np.max(incident_density), "color": lc.Color(255, 0, 0)}    
]
heatmap.set_palette_colors(
    steps=custom_palette,
    look_up_property='value',
    interpolate=True
)

chart.add_legend(data=heatmap, title="Incident Density")

chart.open()
