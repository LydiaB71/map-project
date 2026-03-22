import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import os

def run_batch_map(filename):
    #Load the Data
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    df = pd.read_csv(filename)
    
    #Setup Geocoder and Map
    # Use a unique user_agent to follow Nominatim's rules
    geolocator = Nominatim(user_agent="lydia_map_project_v1")
    
    # Initial map centered generally near your area
    m = folium.Map(location=[29.4122, -95.2441], zoom_start=10)
    points = []

    print(f"Processing {len(df)} locations...")

    #Loop through the CSV rows
    for index, row in df.iterrows():
        address = row.get('Address')
        name = row.get('Name', f"Location {index}") # Fallback if Name column is missing
        
        if pd.isna(address):
            continue

        try:
            location = geolocator.geocode(address)
            if location:
                coords = [location.latitude, location.longitude]
                points.append(coords)
                
                # Add the pin
                folium.Marker(
                    coords, 
                    popup=f"<b>{name}</b><br>{address}", 
                    tooltip=name
                ).add_to(m)
                
                print(f"Mapped: {name}")
            else:
                print(f"Skipped (Not Found): {address}")
            
            # Respect the 1-second rule for free geocoding
            time.sleep(1)

        except GeocoderTimedOut:
            print(f"Timeout error for: {address}. Skipping...")

    #Finalize and Save
    if points:
        m.fit_bounds(points) # Zoom to show all pins
        m.save("final_batch_map.html")
        print("\nSuccess! Open 'final_batch_map.html' to see your results.")
    else:
        print("No locations were successfully geocoded.")

# --- RUN IT ---
# Replace "locations.csv" with your actual filename
run_batch_map("locations.csv")




























































# import time
# import os
# import pandas as pd
# import folium
# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut

# def create_map_with_pins(addresses):
#     #Initialize the Geocoder (using OpenStreetMap/Nominatim)
#     geolocator = Nominatim(user_agent="my_map_app")
    
#     points = []

#     # Starting location (Let's start centered on Houston/Alvin area)
#     m = folium.Map(location=[29.7604, -95.3698], zoom_start=10)

#     for addr in addresses:
#         try:
#             #Convert address to coordinates
#             location = geolocator.geocode(addr)
            
#             if location:
#                 print(f"Adding pin for: {addr}")
#                 #Add a marker to the map
#                 coords = [location.latitude, location.longitude]
#                 points.append(coords)
#                 folium.Marker(
#                     coords, 
#                     popup=addr, 
#                     tooltip="Click for info",
#                     icon=folium.Icon(color='blue', icon='info-sign') # Added a little style
#                 ).add_to(m)
#             else:
#                 print(f"Could not find address: {addr}")
                
#             #Respect Nominatim's Terms of Service (1 request per second)
#             time.sleep(1)

#         except GeocoderTimedOut:
#             print(f"Error: Geocode timed out for {addr}")

#     # Auto-fit the map to show all pins
#     if points:
#         m.fit_bounds(points)
#     else:
#         # Fallback to Houston if no pins were found
#         m.location = [29.7604, -95.3698]




#     #Save the map as an HTML file
#     m.save("my_map.html")
#     print("\nSuccess! Open 'my_map.html' in your browser to see your pins.")

# # Example usage:
# user_addresses = [
#     "Alvin, TX",
#     "Space Center Houston",
#     "University of Houston-Clear Lake",
#     "Cypress, California"
# ]

# create_map_with_pins(user_addresses)