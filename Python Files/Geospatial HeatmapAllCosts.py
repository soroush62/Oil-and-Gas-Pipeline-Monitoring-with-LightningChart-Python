import pandas as pd
import numpy as np
import lightningchart as lc

# Load the license key
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
data = pd.read_csv('Dataset/database.csv')

# Extract latitude, longitude, and cost data, dropping any rows with NaN values in these columns
filtered_data = data[['Accident Latitude', 'Accident Longitude', 'All Costs']].dropna()

latitude = filtered_data['Accident Latitude']
longitude = filtered_data['Accident Longitude']
costs = filtered_data['All Costs']

# Create a 2D grid for the heatmap based on the costs associated with each location
bins = [100, 100]  # Adjust as needed for resolution

# Use a 2D histogram weighted by costs to aggregate costs within each bin
cost_density, lon_edges, lat_edges = np.histogram2d(
    longitude, latitude, bins=bins, weights=costs
)

# Calculate the center points of the bins for plotting
lon_centers = (lon_edges[:-1] + lon_edges[1:]) / 2
lat_centers = (lat_edges[:-1] + lat_edges[1:]) / 2
grid_lon, grid_lat = np.meshgrid(lon_centers, lat_centers)

# Replace any NaN values in cost_density with zero
cost_density = np.nan_to_num(cost_density)

# Create the heatmap chart
chart = lc.ChartXY(
    title='Geospatial Analysis of All Costs by Location',
    theme=lc.Themes.Dark
)

# Add the heatmap to the chart
heatmap = chart.add_heatmap_grid_series(
    rows=cost_density.shape[0],
    columns=cost_density.shape[1]
)

# Define the region for the heatmap based on the longitude and latitude bin edges
heatmap.set_start(x=lon_edges.min(), y=lat_edges.min())
heatmap.set_end(x=lon_edges.max(), y=lat_edges.max())
heatmap.set_step(x=(lon_edges.max() - lon_edges.min()) / cost_density.shape[1],
                 y=(lat_edges.max() - lat_edges.min()) / cost_density.shape[0])

# Set the cost values directly to the heatmap
heatmap.invalidate_intensity_values(cost_density.tolist())
# heatmap.hide_wireframe()

# Set the X and Y axes labels
chart.get_default_x_axis().set_title('Longitude')
chart.get_default_y_axis().set_title('Latitude')
print(np.max(cost_density))
print(np.min(cost_density))
print(np.percentile(cost_density, 97))
# Define a custom color palette for the heatmap
custom_palette = [
    {"value": np.min(cost_density), "color": lc.Color(204, 229, 255)},
    {"value": np.percentile(cost_density, 97), "color": lc.Color(0, 0, 255)},   
    {"value": np.percentile(cost_density, 97.9), "color": lc.Color(0, 255, 255)},
    {"value": np.percentile(cost_density, 98.5), "color": lc.Color(0, 255, 0)}, 
    {"value": np.percentile(cost_density, 99), "color": lc.Color(255, 255, 204)},
    {"value": np.max(cost_density), "color": lc.Color(255, 0, 0)}    
]

# Apply the custom palette to the heatmap
heatmap.set_palette_colors(
    steps=custom_palette,
    look_up_property='value',
    interpolate=True
)

# Add a legend for the heatmap
chart.add_legend(data=heatmap, title="All Costs (USD)")

# Open the chart
chart.open()
