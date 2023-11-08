import sqlite3
from datetime import datetime




conn = sqlite3.connect('RIDENOW.db')
print("Database connecting successfully")
c = conn.cursor()
conn.close()

# c.execute("""
#     SELECT name FROM Parking_lot
#     """)
# name = c.fetchall()
#
# for i in range(1, 11):
#     current_time = datetime.now()
#     date = current_time.date()
#     time = current_time.time()
#     for starting_location in name:
#         ending_location = "Main_Building"
#         c.execute("""
#             INSERT INTO Move (bike_id, starting_location, ending_location, bike_type, operator_id, move_date, move_time)
#             VALUES(?,?,?,?,?,?,?)
#             """, (i, starting_location, ending_location, "electric_bike", 2, date, time))
#         conn.commit()
#         print(i, "record insert to move table")

# Insert data for customer table:
# c.execute("""INSERT INTO Customer (customer_id, username, email, password) VALUES (2798523, "Kris", "kris@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 1 row data")
#
# c.execute("""INSERT INTO Customer (customer_id, username, email, password) VALUES (2861948, "Kira", "kira@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Customer (customer_id, username, email, password) VALUES (2727874, "Duffy", "xinyue@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Customer (customer_id, username, email, password) VALUES (2737427, "Zhirong", "Zhirong@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 4 row data")






# Insert account history data
# c.execute("""INSERT INTO Account_history (account_id, customer_id, in_flow, credit, date, starting_time, ending_time, total_time,
#     cost_1, cost_2, starting_location, ending_location)
#     VALUES (1, 1, 20.00, 10.00, "5/10/2023", "17:00", "18:00", "1:00", 1.5, "", "Main campus", "Westview" )""")
# conn.commit()
# print("Successfully insert 1 row data")

# c.execute("""INSERT INTO Account_history (account_id, customer_id, in_flow, credit, date, starting_time, ending_time, total_time,
#     cost_1, cost_2, starting_location, ending_location)
#     VALUES (2, 4, 100.00, 55.00, "4/10/2023", "12:00", "13:00", "1:00", "", 2.0, "Dunaskin Mill", "Main campus" )""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Account_history (account_id, customer_id, in_flow, credit, date, starting_time, ending_time, total_time,
#     cost_1, cost_2, starting_location, ending_location)
#     VALUES (3, 2, 33.00, 12.50, "1/10/2023", "13:00", "13:15", "0:15", 1.5, "", "Main campus", "Learing Hub" )""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Account_history (account_id, customer_id, in_flow, credit, date, starting_time, ending_time, total_time,
#     cost_1, cost_2, starting_location, ending_location)
#     VALUES (4, 3, 22.00, 15.50, "30/9/2023", "19:00", "22:00", "3:00", 1.5, "", "Main campus", "Glasgow Central Station")""")
# conn.commit()
# print("Successfully insert 4 row data")


# Insert bike_info data:
# c.execute("""INSERT INTO Bike_info (bike_id, battery_level, location, status, type)
#     VALUES (1, 100, "Main campus", "Ready to go", "E_bike")""")
# conn.commit()
# print("Successfully insert 1 row data")

# c.execute("""INSERT INTO Bike_info (bike_id, battery_level, location, status, type)
#     VALUES (2, 100, "Library", "Ready to go", "E_bike")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Bike_info (bike_id, battery_level, location, status, type)
#     VALUES (3, "", "Learning Hub", "Ready to go", "F_bike")""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Bike_info (bike_id, battery_level, location, status, type)
#     VALUES (4, "", "Main campus", "Need to repair", "F_bike")""")
# conn.commit()
# print("Successfully insert 4 row data")


# Insert Credit_card data:
# c.execute("""INSERT INTO Credit_card (card_id, card_holder_name, card_number, customer_id, CV_number, date, expired_date)
#     VALUES (1, "Kris", 5502130022450476, 1, 394, "5/10/2013", "8/2025")""")
# conn.commit()
# print("Successfully insert 1 row data")
#
# c.execute("""INSERT INTO Credit_card (card_id, card_holder_name, card_number, customer_id, CV_number, date, expired_date)
#     VALUES (2, "Kris", 5236497993045254, 1, 083, "5/10/2013", "8/2025")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Credit_card (card_id, card_holder_name, card_number, customer_id, CV_number, date, expired_date)
#     VALUES (3, "Kira", 1234567890987654, 2, 114, "5/10/2013", "6/2026")""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Credit_card (card_id, card_holder_name, card_number, customer_id, CV_number, date, expired_date)
#     VALUES (4, "Xinyue", 9807123456781234, 3, 987, "5/10/2013", "7/2026")""")
# conn.commit()
# print("Successfully insert 4 row data")


# Insert error_journal data:
# c.execute("""INSERT INTO Error_journal (error_journal_id, bike_id, starting_time, ending_time, location, operator_id,
#     pic, repair_message, status)
#     VALUES (1, 1, "19:00", "22:00", "Glasgow Queen station", 1, "", "Wheel", "Need to repair")""")
# conn.commit()
# print("Successfully insert 1 row data")

# c.execute("""INSERT INTO Error_journal (error_journal_id, bike_id, starting_time, ending_time, location, operator_id,
#     pic, repair_message, status)
#     VALUES (2, 4, "13:00", "15:00", "Main Campus", 1, "", "Brake", "Need to repair")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Error_journal (error_journal_id, bike_id, starting_time, ending_time, location, operator_id,
#     pic, repair_message, status)
#     VALUES (3, 2, "17:00", "18:00", "Library", 1, "", "Seat", "Need to repair")""")
# conn.commit()
# print("Successfully insert 3 row data")


# Insert data for Manager table:
# c.execute("""INSERT INTO Manager (manager_id, username, email, password) VALUES (1, "Christin", "Christin@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 1 row data")

# c.execute("""INSERT INTO Manager (manager_id, username, email, password) VALUES (2, "Corina", "Corina@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Manager (manager_id, username, email, password) VALUES (3, "Seraphine", "Seraphine@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 3 row data")


# Insert data for Move table:
# c.execute("""INSERT INTO Move (move_id, bike_id, ending_location, starting_location)
#     VALUES (1, 1, "Main campus", "QMU")""")
# conn.commit()
# print("Successfully insert 1 row data")
#
# c.execute("""INSERT INTO Move (move_id, bike_id, ending_location, starting_location)
#     VALUES (2, 4, "ARC", "Adam Smith Building")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Move (move_id, bike_id, ending_location, starting_location)
#     VALUES (3, 2, "Main Building", "Art School")""")
# conn.commit()
# print("Successfully insert 3 row data")


# Insert data for Operator table:
# c.execute("""INSERT INTO Operator (operator_id, username, email, password)
#     VALUES (1, "Mike", "Mike@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 1 row data")
#
# c.execute("""INSERT INTO Operator (operator_id, username, email, password)
#     VALUES (2, "Carlos", "Carlos@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Operator (operator_id, username, email, password)
#     VALUES (3, "Matilda", "Matilda@gmail", "123456")""")
# conn.commit()
# print("Successfully insert 3 row data")


# insert Parking_lot data:
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (10, "[55.87107534990584, -4.299838643941384]", "Kelvinhall", 10)""")
# conn.commit()
# print("Successfully insert 1 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (11, "[55.87480385766344, -4.279536962315601]", "Kelvinbridge", 15)""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (12, "[55.87177020851412, -4.2688939569467195]", "St. George's Cross", 20)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (13, "[55.868543686616796, -4.259581327251547]", "Cowcaddens", 12)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (14, "[55.85759992586805, -4.255192345837397]", "St. Enoch", 27)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (15, "[55.86259540216528, -4.253294334439605]", "Buchanan Street", 10)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (16, "[55.865954781770284, -4.2514818064037465]", "Buchanan Bus Station", 32)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (17, "[55.86245302556574, -4.242558245927205]", "University of Strathclyde", 25)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (18, "[55.867078661892215, -4.249868115827654]", "Glasgow Caledonian University", 28)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (19, "[55.87565841454545, -4.22796175233819]", "Costco Glasgow", 25)""")
# conn.commit()
# print("Successfully insert 3 row data")
#
# c.execute("""INSERT INTO Parking_lot (parking_lot_id, address, name, num_bike)
#     VALUES (20, "[55.88069533226686, -4.229041114760715]", "Glasgow Kelvin College", 30)""")
# conn.commit()
# print("Successfully insert 3 row data")

# insert Tracking data:
# c.execute("""INSERT INTO Tracking (tracking_id, bike_id, location, time)
#     VALUES (1, 2, "Kelvinhaugh St", "1:00")""")
# conn.commit()
# print("Successfully insert 1 row data")
#
# c.execute("""INSERT INTO Tracking (tracking_id, bike_id, location, time)
#     VALUES (2, 4, "ARC", "0:30")""")
# conn.commit()
# print("Successfully insert 2 row data")
#
# c.execute("""INSERT INTO Tracking (tracking_id, bike_id, location, time)
#     VALUES (4, 3, "Math School", "0:15")""")
# conn.commit()
# print("Successfully insert 3 row data")

# Kris = "Kris"
# Duffy = "Duffy"
# id_kris = 2798523
# id_kira = 2861948
# id_duffy = 2727874
# id_zhirong = 2737427
#
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 5 WHERE parking_lot_id = 1""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 15 WHERE parking_lot_id = 2""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 25 WHERE parking_lot_id = 3""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 10 WHERE parking_lot_id = 4""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 17 WHERE parking_lot_id = 5""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 10 WHERE parking_lot_id = 6""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 18 WHERE parking_lot_id = 7""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 7 WHERE parking_lot_id = 8""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 11 WHERE parking_lot_id = 9""")
# conn.commit()
# c.execute("""UPDATE Parking_lot SET foot_bike_number = 5 WHERE parking_lot_id = 10""")
# conn.commit()




# # Delete data
# c.execute("""DELETE FROM Customer WHERE customer_id = 2798591""")
# conn.commit()



# Add a new column for electric bike number
# c.execute('ALTER TABLE Tracking ADD COLUMN operator_id INT;')

# Add a new column for foot bike number
# c.execute('ALTER TABLE Move ADD COLUMN move_date TEXT;')
#
# c.execute('ALTER TABLE Move ADD COLUMN move_time TEXT;')


# Commit the changes and close the connection
# conn.commit()
# print("Adding new column successfully!")
# conn.close()


# Change the column name from 'old_column_name' to 'new_column_name' in the 'your_table_name' table
# c.execute('ALTER TABLE Parking_lot RENAME COLUMN electric_bike_number TO electric_bike;')
# c.execute('ALTER TABLE Parking_lot RENAME COLUMN foot_bike_number TO foot_bike;')

# c.execute("""SELECT * FROM Parking_lot""")
# data = c.fetchall()
# print(data)




# c.execute("""
#     UPDATE Error_journal SET bike_type = ? WHERE bike_type = ?
#     """, ("electric_scooter", "foot_bike"))

# old_column_name = 'foot_bike'
# new_column_name = 'electric_scooter'
#
# # 1. Create a new table with the desired column name
# c.execute(f"ALTER TABLE Parking_lot RENAME COLUMN {old_column_name} TO {new_column_name}")
#
# # 2. Copy data from the old table to the new table with the new column name
# c.execute(f"CREATE TABLE temp AS SELECT *, {old_column_name} AS {new_column_name} FROM Parking_lot;")
# c.execute(f"DROP TABLE Parking_lot;")
# c.execute(f"ALTER TABLE temp RENAME TO Parking_lot;")









