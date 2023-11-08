from tkinter import *
import tkintermapview           # https://github.com/TomSchimansky/TkinterMapView
from ManipulateDatabase import OperatorDatabase
import sqlite3


root = Tk()
root.title("map")
root.geometry("900x700")

l_map = LabelFrame(root)
l_map.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(l_map, width=800, height=600, corner_radius=0)
map_widget.set_position(55.87180409870281, -4.288428799073684)
map_widget.set_zoom(15)
map_widget.grid()


conn = sqlite3.connect('RIDENOW.db')
print("Database connecting successfully")
c = conn.cursor()
c.execute("""
    SELECT address FROM Parking_lot
    """)
address = c.fetchall()
print(address)

c.execute("""
    SELECT name FROM Parking_lot
    """)
parking_lot_name = c.fetchall()
print(parking_lot_name)
names = [item[0] for item in parking_lot_name]
# Loop through each tuple and extract the values
latitude = []
longitude = []
for item in address:
    # Extract the string from the tuple
    coord_string = item[0]

    # Remove the brackets and split the string into latitude and longitude
    coord_string = coord_string.strip('[]')
    lat, long = map(float, coord_string.split(', '))
    latitude.append(lat)
    longitude.append(long)
    # set a position marker
    for x, y, z in zip(latitude, longitude, names):
        markers = map_widget.set_marker(x, y, text="{}".format(z))

root.mainloop()



