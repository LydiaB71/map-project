import time

import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def create_map_with_pins(addresses):
    #Initialize the Geocoder (using OpenStreetMap/Nominatim)
    geolocator = Nominatim(user_agent="my_map_app")
    
    points = []

    # Starting location (Let's start centered on Houston/Alvin area)
    m = folium.Map(location=[29.7604, -95.3698], zoom_start=10)

    for addr in addresses:
        try:
            #Convert address to coordinates
            location = geolocator.geocode(addr)
            
            if location:
                print(f"Adding pin for: {addr}")
                #Add a marker to the map
                coords = [location.latitude, location.longitude]
                points.append(coords)
                folium.Marker(
                    coords, 
                    popup=addr, 
                    tooltip="Click for info",
                    icon=folium.Icon(color='blue', icon='info-sign') # Added a little style
                ).add_to(m)
            else:
                print(f"Could not find address: {addr}")
                
            #Respect Nominatim's Terms of Service (1 request per second)
            time.sleep(1)

        except GeocoderTimedOut:
            print(f"Error: Geocode timed out for {addr}")

    # Auto-fit the map to show all pins
    if points:
        m.fit_bounds(points)
    else:
        # Fallback to Houston if no pins were found
        m.location = [29.7604, -95.3698]




    #Save the map as an HTML file
    m.save("my_map.html")
    print("\nSuccess! Open 'my_map.html' in your browser to see your pins.")

# Example usage:
user_addresses = [
    "Alvin, TX",
    "Space Center Houston",
    "University of Houston-Clear Lake",
    "Cypress, California"
]

create_map_with_pins(user_addresses)