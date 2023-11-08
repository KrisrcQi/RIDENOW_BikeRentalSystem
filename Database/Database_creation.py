#! Bike rental system database creation for 2BIKE
import sqlite3

# # Creating or connecting a database
conn = sqlite3.connect('RIDENOW.db')
print("Database connecting successfully")
c = conn.cursor()

# # Drop tables:
# c.execute('DROP TABLE Bike_info')
# c.execute('DROP TABLE Bike')
# c.execute('DROP TABLE Customer')
# c.execute('DROP TABLE Error_journal')
# c.execute('DROP TABLE Manager')
# c.execute('DROP TABLE Operator')
# c.execute('DROP TABLE Parking_lot')
# c.execute('DROP TABLE Login_history')
# c.execute('DROP TABLE Tracking')
c.execute('DROP TABLE Credit_log')
conn.commit()



# Table creation
# Creating table of Bike_info:
# c.execute('''create table Bike_info(
#     bike_id integer primary key autoincrement,
#     type text not null,
#     battery_level integer not null,
#     location text not null,
#     status text not null,
#
#     foreign key(location) references Parking_lot(parking_lot_id));''')
# print("Table Bike_info created successfully")
# conn.commit()

#
# # Creating table of Error_journal:
# c.execute('''create table Error_journal(
#     error_journal_id integer primary key autoincrement,
#     bike_id integer not null,
#     bike_type text not null,
#     operator_id integer,
#     customer_id integer,
#     location text not null,
#     repair_message text not null,
#     pic text,
#     status text not null,
#     starting_time text,
#     starting_date text not null,
#     ending_time text,
#     ending_date text,
#     description text,
#
#     foreign key(bike_id) references Bike_info(bike_id),
#     foreign key(location) references Parking_lot(parking_lot_id),
#     foreign key(operator_id) references Operator(operator_id)
#     foreign key(customer_id) references Customer(customer_id)
#     );''')
# print("Table Error_journal created successfully")
# conn.commit()

# Creating table of Parking_lot:
# c.execute('''create table Parking_lot(
#     parking_lot_id integer primary key autoincrement,
#     name text not null,
#     num_bike integer not null,
#     address array not null);''')
# print("Table Parking_lot created successfully")
#
# create table of Tracking
# c.execute('''create table Tracking(
#     tracking_id integer primary key autoincrement,
#     bike_id integer not null,
#     start_location text not null,
#     end_location text,
#     start_time text not null,
#     end_time text,
#     total_rent_time text,
#
#     foreign key(bike_id) references Bike_info(bike_id),
#     foreign key(start_location) references Parking_lot(parking_lot_id)
#     foreign key(end_location) references Parking_lot(parking_lot_id)
#     )''')
# conn.commit()
# print("table created successfully")

# create table of Move
# c.execute('''create table Move(
#     move_id integer primary key autoincrement,
#     bike_id integer not null,
#     starting_location text not null,
#     ending_location text not null,
#
#     foreign key(bike_id) references Bike_info(bike_id)
#     foreign key(starting_location) references Parking_lot(parking_lot_id),
#     foreign key(ending_location) references Parking_lot(parking_lot_id)
#     )''')
# conn.commit()

# Creating table of Customer:
# c.execute('''create table Customer(
#     customer_id integer primary key autoincrement,
#     username text not null,
#     email text not null,
#     password text not null);''')
# print("Table Customer created successfully")
# conn.commit()
#
# # Creating table of Account_history:
# c.execute('''create table Account_history(
#     account_id integer primary key autoincrement,
#     customer_id integer not null,
#     in_flow float,
#     credit float,
#     date text,
#     starting_time text,
#     ending_time text,
#     total_time text,
#     cost_1 float,
#     cost_2 float,
#     starting_location text,
#     ending_location text,
#
#     foreign key(customer_id) references Customer(customer_id)
#     foreign key(starting_location) references Parking_lot(parking_lot_id)
#     foreign key(ending_location) references Parking_lot(parking_lot_id)
#     );''')
# print("Table Account_history created successfully")
# conn.commit()
#
# # Creating table of Operator:
# c.execute('''create table Operator(
#     operator_id integer primary key autoincrement,
#     username text not null,
#     email text not null,
#     password text not null
#     );''')
# print("Table Operator created successfully")
# conn.commit()
#
# # Creating table of Manager:
# c.execute('''create table Manager(
#     manager_id integer primary key autoincrement,
#     username text not null,
#     email text not null,
#     password text not null
#     );''')
# print("Table Manager created successfully")
# conn.commit()
#
# # create table of Credit_card:
# c.execute('''create table Credit_card(
#     card_id integer primary key autoincrement,
#     card_number integer not null,
#     date text not null,
#     expired_date text not null,
#     card_holder_name text not null,
#     CV_number integer not null,
#     customer_id integer not null,
#
#     foreign key(customer_id) references Customer(customer_id)
#     )''')
# conn.commit()
# conn.close()
#

#
# # create a new FK in the table:
# bike_info_table_name = 'bike_info'
# parking_lot_table_name = 'parking_lot'
# foreign_key_query = f"ALTER TABLE {bike_info_table_name} " \
#                     f"ADD FOREIGN KEY (parking_lot_id) " \
#                     f"REFERENCES {parking_lot_table_name}(id)"
# c.execute(foreign_key_query)
# print("FK created successfully")
# conn.commit()

# Creating table of Manager:
# c.execute('''create table Login_history(
#     login_id integer primary key autoincrement,
#     type text not null,
#     id integer not null,
#     username text not null,
#     email text not null,
#     password text not null,
#     login_time text not null
#     );''')
# print("Table Manager created successfully")
# conn.commit()

# # create table of Tracking
# c.execute('''create table Charge_history(
#     charge_id integer primary key autoincrement,
#     bike_id integer not null,
#     bike_type text not null,
#     operator_id integer not null,
#     battery integer not null,
#     charge_time text,
#     charge_location text,
#
#     foreign key(bike_id) references Bike_info(bike_id)
#     );''')
# conn.commit()
# print("table created successfully")
# conn.close()
# print("database closed")

# c.execute('''create table Repair_history(
#     repair_id integer primary key autoincrement,
#     operator_id integer not null,
#     bike_id integer not null,
#     error_type text not null,
#     repair_date text,
#     bike_type text,
#     repair_time text,
#
#     foreign key(bike_id) references Bike_info(bike_id),
#     foreign key(operator_id) references Operator(operator_id)
#     );''')
# conn.commit()
# print("table created successfully")
# conn.close()
# print("database closed")

# c.execute('''create table Credit_log(
#     log_id integer primary key autoincrement,
#     amount float not null,
#     type text not null,
#     customer_id text not null,
#     date text not null,
#
#
#     foreign key(customer_id) references Customer(customer_id)
#     );''')
# conn.commit()
# print("table created successfully")
conn.close()
print("database closed")




