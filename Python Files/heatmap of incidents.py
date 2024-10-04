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

# Load the license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
data = pd.read_csv('Dataset/database.csv')

# Extract necessary data: latitude and longitude of incidents
latitude = data['Accident Latitude'].dropna()
longitude = data['Accident Longitude'].dropna()

# Create a 2D histogram for density over the latitude and longitude
# Use bins that match the desired resolution of the heatmap
bins = [100, 100]  # You can adjust the number of bins for different resolution

incident_density, lon_edges, lat_edges = np.histogram2d(longitude, latitude, bins=bins)

# Calculate the center points of the bins for plotting
lon_centers = (lon_edges[:-1] + lon_edges[1:]) / 2
lat_centers = (lat_edges[:-1] + lat_edges[1:]) / 2
grid_lon, grid_lat = np.meshgrid(lon_centers, lat_centers)

# Replace any NaN values in incident_density with zero
incident_density = np.nan_to_num(incident_density)

# Create the heatmap chart
chart = lc.ChartXY(
    title='Geospatial Analysis of Oil Pipeline Spills and Leaks',
    theme=lc.Themes.Dark
)

# Add the heatmap to the chart
heatmap = chart.add_heatmap_grid_series(
    rows=incident_density.shape[0],
    columns=incident_density.shape[1]
)

# Define the region for the heatmap based on the longitude and latitude bin edges
heatmap.set_start(x=lon_edges.min(), y=lat_edges.min())
heatmap.set_end(x=lon_edges.max(), y=lat_edges.max())
heatmap.set_step(x=(lon_edges.max() - lon_edges.min()) / incident_density.shape[1],
                 y=(lat_edges.max() - lat_edges.min()) / incident_density.shape[0])

# Set the density values directly to the heatmap
heatmap.invalidate_intensity_values(incident_density.tolist())
# heatmap.hide_wireframe()

# Set the X and Y axes labels
chart.get_default_x_axis().set_title('Longitude')
chart.get_default_y_axis().set_title('Latitude')

# Define a custom color palette for the heatmap
custom_palette = [
    {"value": np.min(incident_density), "color": lc.Color(204, 229, 255)},
    {"value": np.percentile(incident_density, 99), "color": lc.Color(0, 0, 255)},   
    {"value": np.percentile(incident_density, 99.25), "color": lc.Color(0, 255, 255)},
    {"value": np.percentile(incident_density, 99.5), "color": lc.Color(0, 255, 0)}, 
    {"value": np.percentile(incident_density, 99.75), "color": lc.Color(255, 255, 204)},
    {"value": np.max(incident_density), "color": lc.Color(255, 0, 0)}    
]
# print(np.max(incident_density))
# print(np.percentile(incident_density, 99.5))
# Apply the custom palette to the heatmap
heatmap.set_palette_colors(
    steps=custom_palette,
    look_up_property='value',
    interpolate=True
)

# Add a legend for the heatmap
chart.add_legend(data=heatmap, title="Incident Density")

# Open the chart
chart.open()
