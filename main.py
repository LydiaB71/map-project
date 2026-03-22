import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import os

def run_robust_batch_map(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    df = pd.read_csv(filename)
    geolocator = Nominatim(user_agent="mapping_nexus_v2")
    m = folium.Map(location=[29.4122, -95.2441], zoom_start=10)
    
    points = []
    failed_rows = [] # This list will hold our "bad" data

    print(f"Processing {len(df)} locations...")

    for index, row in df.iterrows():
        address = row.get('Address')
        name = row.get('Name', f"Location {index}")
        
        # Data Cleaning: Skip empty rows entirely
        if pd.isna(address) or str(address).strip() == "":
            row['Failure_Reason'] = "Empty Address"
            failed_rows.append(row)
            continue

        try:
            location = geolocator.geocode(address)
            if location:
                coords = [location.latitude, location.longitude]
                points.append(coords)
                folium.Marker(coords, popup=name).add_to(m)
                print(f"✔ Mapped: {name}")
            else:
                print(f"✘ Not Found: {address}")
                row['Failure_Reason'] = "Geocoder could not find address"
                failed_rows.append(row)
            
            time.sleep(1)

        except GeocoderTimedOut:
            row['Failure_Reason'] = "Connection Timeout"
            failed_rows.append(row)
            print(f"⚠ Timeout: {address}")

    # Save the successful map
    if points:
        m.fit_bounds(points)
        m.save("cleaned_batch_map.html")
        print("\nMap saved as 'cleaned_batch_map.html'")

    # --- THE DATA CLEANING OUTPUT ---
    if failed_rows:
        failed_df = pd.DataFrame(failed_rows)
        failed_df.to_csv("failed_addresses.csv", index=False)
        print(f"Finished! {len(failed_rows)} rows failed. See 'failed_addresses.csv' for details.")
    else:
        print("Success! 100% of addresses were mapped.")

run_robust_batch_map("locations.csv")













































