import folium
import sqlite3



# Initializing a starting point on the map
m = folium.Map(location=[55.8734, -4.2889], zoom_start=15)

# Connecting with database
conn = sqlite3.connect("RIDENOW.db")
print("Database connecting successfully")
c = conn.cursor()

# Select available bikes on the specific location
c.execute("""SELECT * FROM Parking_lot""")
parking_data_list = c.fetchall()

print(parking_data_list)
print(parking_data_list[3])

for parking_data in parking_data_list:
    location_str = parking_data[3]
    location_tuple = tuple(map(float, location_str[1:-1].split(', ')))
    folium.Marker(
        location = location_tuple,
        popup=("{}, Bike available: {}".format(parking_data[1],parking_data[2])),
        # tooltip=(""),
        icon=folium.Icon(color='red', prefix='fa', icon='paw')
    ).add_to(m)

m.save("Map_for_2BIKE.html")

