import sqlite3
from time import strftime
from datetime import datetime



conn = sqlite3.connect('RIDENOW.db')
c = conn.cursor()
print("Database connecting successfully")


# Inserting value in the table:
data_to_insert = [
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Need repair"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Need repair"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Ready to go"),
    ('electric_bike', 100, "Glasgow_Kelvin_College", "Need repair"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Need repair"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Need repair"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Need repair"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
    ('foot_bike', "", "Glasgow_Kelvin_College", "Ready to go"),
]

# Loop through the data and insert it into the table
for data in data_to_insert:
    c.execute("INSERT INTO Bike_info (type, battery_level, location, status) VALUES (?, ?, ?, ?)", data)
    print("Successfully insert data")
conn.commit()
conn.close()
