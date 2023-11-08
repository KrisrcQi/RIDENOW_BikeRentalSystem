import sqlite3
from datetime import datetime, timedelta

# # Notes of bugs
# need add an insert customer_id or operator_id when renting a bike / solved
# bug about bike reduce / solved
# submit button clicked successfully return to report main page / solved
# detail of status no display / solved
# confirm payment display and renew the credit new amount / solved
# edit and confirm new username can't display immediately / solved
# rental contract deducted customer credit / solved
# electric function and cost function adjustment / solved
# map / solved
# display wrong row of customer info / solved

# error_journal has a no used column






class CusOpenDatabase:

    def __init__(self):

        self.open_database()

    def open_database(self):

        self.conn = sqlite3.connect("RIDENOW.db")
        self.c = self.conn.cursor()

    def __del__(self):

        self.conn.close()

    def select_parking_location(self):      # get the name list of Parking_lot

        self.c.execute("""
            SELECT name FROM Parking_lot
            """)
        parking_location = self.c.fetchall()
        return parking_location

    def get_address(self, name):

        self.c.execute("""
            SELECT address FROM Parking_lot WHERE name = ?
            """, (name,))
        address = self.c.fetchall()
        print(address, "is the current riding start point")

        return address

    def get_bike_number(self, selected_category, selected_parking_name):        # get the available bike number

        if selected_category == "electric_bike":
            self.c.execute("""
                SELECT electric_bike FROM Parking_lot WHERE name = ?
                """, (selected_parking_name,))
            bike_number_selected = self.c.fetchall()
        else:
            self.c.execute("""
                SELECT electric_scooter FROM Parking_lot WHERE name = ?
                """, (selected_parking_name,))
            bike_number_selected = self.c.fetchall()
        print("The available bike number: ")
        print(bike_number_selected)
        return bike_number_selected

    def insert_rentTrackData(self, category, location_name):        # insert a rental track info to Tracking table

        # get the first available bike for rental
        selected_status = "Ready to go"
        self.c.execute("""
            SELECT * FROM Bike_info WHERE location = ? AND type = ? AND status = ?
            """, (location_name, category, selected_status))
        available_bike = self.c.fetchall()
        renting_bike = available_bike[0]    # rent out the first available bike in the whole list
        renting_bike_id = renting_bike[0]   # check its bike_id
        print(f"The renting bike_info: \n{renting_bike}")
        print(f"bike_id: {renting_bike_id}")

        # insert the rental tracking info
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        userdata = self.get_loginData()
        guid = userdata[2]
        if userdata[1] == "customer":
            self.c.execute("""
                INSERT INTO Tracking (bike_id, bike_type, battery_level, start_location, start_time, customer_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (renting_bike[0], renting_bike[1], renting_bike[2], renting_bike[3], current_time, guid))
            self.conn.commit()
            print("insert tracking history record successfully.")

        elif userdata[1] == "operator":
            self.c.execute("""
                INSERT INTO Tracking (bike_id, bike_type, battery_level, start_location, start_time, operator_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (renting_bike[0], renting_bike[1], renting_bike[2], renting_bike[3], current_time, guid))
            self.conn.commit()
            print("insert tracking history record successfully.")
        else:
            self.c.execute("""
                INSERT INTO Tracking (bike_id, bike_type, battery_level, start_location, start_time)
                VALUES (?, ?, ?, ?, ?)
                """,(renting_bike[0], renting_bike[1], renting_bike[2], renting_bike[3], current_time))
            self.conn.commit()
            print("insert tracking history record successfully.")

        # update total number and type number of specific rent-out bike for start_location
        if renting_bike[1] == "electric_bike":
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (renting_bike[3],))
            rented_bike_start_locationInfo = self.c.fetchall()
            print(rented_bike_start_locationInfo)
            print("This Parking_lot has total ", rented_bike_start_locationInfo[0][2], "bike remained")
            updated_total_num = rented_bike_start_locationInfo[0][2] - 1
            updated_electric_bike_num = rented_bike_start_locationInfo[0][4] - 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_bike = ? WHERE name = ?
                """, (updated_total_num, updated_electric_bike_num, renting_bike[3]))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a E_B out)")
        else:
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (renting_bike[3],))
            rented_bike_start_locationInfo = self.c.fetchall()
            print(rented_bike_start_locationInfo)
            print("This Parking_lot has total ", rented_bike_start_locationInfo[0][2], "bike remained")
            updated_total_num = rented_bike_start_locationInfo[0][2] - 1
            updated_foot_bike_num = rented_bike_start_locationInfo[0][5] - 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_scooter = ? WHERE name = ?
                """, (updated_total_num, updated_foot_bike_num, renting_bike[3]))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a F_B out)")

        # update bike status:
        on_renting = "On Rental Contract"
        self.c.execute("""
            UPDATE Bike_info SET status = ? WHERE bike_id = ?
            """, (on_renting, renting_bike[0]))
        self.conn.commit()
        print("Bike_Status updated successfully!(ON RENTAL)")

        current_ride = self.get_currentBikeInfo()

        return current_ride

    def get_currentBikeInfo(self):      # get the current renting bike info

        self.c.execute("""
            SELECT * FROM Tracking
            """)
        current_rent_bike = self.c.fetchall()
        latest_row = current_rent_bike[-1]      # check the current rent bike, which is the latest updated tracking

        return latest_row

    def insert_returnBikeTrackData(self, riding_time):        # insert a return bike track info to Tracking table

        print("Total riding time is: ", riding_time)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latest_riding = self.get_currentBikeInfo()
        print(latest_riding)
        self.c.execute("""
            UPDATE Tracking SET end_time = ?, total_rent_time = ? WHERE tracking_id = ?
            """, (current_time, riding_time, latest_riding[0]))
        self.conn.commit()
        print("insert return bike tracking history record successfully.")
        print(latest_riding)

    def insert_return_location(self, get_location):     # insert return bike location and update bike numbers and status

        # insert end_location for tracking table
        latest_riding = self.get_currentBikeInfo()
        price = self.get_price()
        print(latest_riding)
        self.c.execute("""
            UPDATE Tracking SET end_location = ?, price = ? WHERE tracking_id = ?
            """, (get_location, price, latest_riding[0]))
        self.conn.commit()
        print("insert return location record successfully.")

        # update battery_level
        self.get_ePower()

        # update return bike number for end_location in Parking_lot table
        latest_riding = self.get_currentBikeInfo()
        print(latest_riding)
        if latest_riding[7] == "electric_bike":
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (latest_riding[3],))
            rented_bike_start_locationInfo = self.c.fetchall()
            updated_total_num = rented_bike_start_locationInfo[0][2] + 1
            updated_electric_bike_num = rented_bike_start_locationInfo[0][4] + 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_bike = ? WHERE name = ?
                """, (updated_total_num, updated_electric_bike_num, latest_riding[3]))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a E_B in)")
        else:
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (latest_riding[3],))
            rented_bike_start_locationInfo = self.c.fetchall()
            updated_total_num = rented_bike_start_locationInfo[0][2] + 1
            updated_foot_bike_num = rented_bike_start_locationInfo[0][5] + 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_scooter = ? WHERE name = ?
                """, (updated_total_num, updated_foot_bike_num, latest_riding[3]))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a F_B in)")

        # update bike status:
        ready = "Ready to go"
        self.c.execute("""
            UPDATE Bike_info SET status = ?, location = ? WHERE bike_id = ?
            """, (ready, get_location, latest_riding[1]))
        self.conn.commit()
        print("Bike_Status updated successfully!(Bike Return)")

    def get_price(self):

        # get the latest_riding data and riding_time
        riding_info = self.get_currentBikeInfo()
        riding_time = riding_info[6]
        print("getprice", riding_info)
        # Split the string into hours, minutes, and seconds
        time_parts = riding_time.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2].split('.')[0])
        milliseconds = int(time_parts[2].split('.')[1])

        # Create a timedelta object with the parsed values
        riding_time = timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

        # Calculate the total seconds in the timedelta
        total_seconds = riding_time.total_seconds()

        # setting the first 10 seconds
        first_10_second = 10

        # Calculate the income with the price setting: first hour: 2 Pounds, later hour: 1.5 Pounds/hour
        # Test price setting is first 10 seconds: 10 Pounds, later price: 0.2 Pounds/second

        # # Define pricing
        first_10s_price = 10
        additional_price = 1

        # Calculate rent cost:
        if total_seconds <= first_10_second:
            income = first_10s_price
        else:
            income = first_10s_price + (total_seconds - first_10_second) * additional_price

        print("Income: ${}".format(income))


        return income

    def get_ePower(self):

        # get the latest_riding data and riding_time
        riding_info = self.get_currentBikeInfo()
        riding_time = riding_info[6]
        bike_id = riding_info[1]
        print("Bike_id", bike_id)

        # split the string into hours, minutes, and seconds
        time_parts = riding_time.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2].split('.')[0])
        milliseconds = int(time_parts[2].split('.')[1])

        # create a timedelta object with the parsed values
        riding_time = timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

        # calculate the total seconds in the timedelta
        total_seconds = riding_time.total_seconds()

        # electric cost setting: 1% per seconds
        e_cost = 1

        # total electric cost
        total_e_cost = int(e_cost * total_seconds)
        print("Current riding cost battery: ", total_e_cost, "%")
        remained_battery = 100 - total_e_cost
        if remained_battery < 0:
            print("Run out of bike's battery! Please charge now!")
            remained_battery = 0
            self.c.execute("""
                UPDATE Tracking SET battery_level = ? WHERE bike_id = ?
                """, (remained_battery, bike_id))
            self.conn.commit()
            print("Tracking battery_level updated successfully. (Battery died, charge needed)")

            self.c.execute("""
                UPDATE Bike_info SET battery_level = ? WHERE bike_id = ?
                """, (remained_battery, bike_id))
            self.conn.commit()
            print("Bike_info battery_level updated successfully. (Battery died, charge needed)")
        else:
            self.c.execute("""
                UPDATE Tracking SET battery_level = ? WHERE bike_id = ?
                """, (remained_battery, bike_id))
            self.conn.commit()
            print("Tracking battery_level updated successfully.", remained_battery, "%")

            self.c.execute("""
                UPDATE Bike_info SET battery_level = ? WHERE bike_id = ?
                """, (remained_battery, bike_id))
            self.conn.commit()
            print("Bike_info battery_level updated successfully.", remained_battery, "%")

    def get_current_credit(self):

        userdata = self.get_loginData()
        customer_id = userdata[2]
        self.c.execute("""
                    SELECT credit FROM Customer WHERE customer_id = ?
                    """, (customer_id,))
        old_credit = self.c.fetchall()
        old_credit = float(old_credit[0][0])

        return old_credit

    def charge_fee(self):

        userdata = self.get_loginData()
        customer_id = userdata[2]
        cost = self.get_price()
        old_credit = self.get_current_credit()
        new_credit = old_credit - cost
        self.c.execute("""
            UPDATE Customer SET credit = ? WHERE customer_id = ?
            """, (new_credit, customer_id))
        self.conn.commit()
        print("Customer's credit record updated successfully.")

    def insert_account_history_spend(self):

        # insert Account_history:
        cost = self.get_price()
        latest_riding = self.get_currentBikeInfo()
        userdata = self.get_loginData()
        customer_id = userdata[2]
        self.c.execute("""
                    SELECT credit FROM Customer WHERE customer_id = ?
                    """, (customer_id,))
        old_credit = self.c.fetchall()

        self.c.execute("""
            INSERT INTO Account_history (customer_id, credit, starting_time, ending_time, total_time, cost_1, 
            starting_location, ending_location, type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_id, old_credit[0][0], latest_riding[4], latest_riding[5], latest_riding[6], cost,
                  latest_riding[2], latest_riding[3], "Spend"))
        self.conn.commit()
        print("New Account_history inserted successfully! (Spend)")

    def get_loginData(self):

        self.c.execute("""
            SELECT * FROM Login_history
            """)
        login_data = self.c.fetchall()
        latest_login = login_data[-1]
        return latest_login

    def update_newUsername(self, new_username):
        userdata = self.get_loginData()
        customer_id = userdata[2]
        try:
            self.c.execute("""
                UPDATE Customer SET username = ? WHERE customer_id = ?
                """, (new_username, customer_id))
            self.conn.commit()
            print("Username updated successfully!")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def update_newEmail(self, new_userEmail):
        userdata = self.get_loginData()
        customer_id = userdata[2]
        try:
            self.c.execute("""
                UPDATE Customer SET email = ? WHERE customer_id = ?
                """, (new_userEmail, customer_id))
            self.conn.commit()
            print("Email updated successfully!")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def check_myPassword(self):
        userdata = self.get_loginData()
        customer_id = userdata[2]
        self.c.execute("""
            SELECT * FROM Customer WHERE customer_id = ?
            """, (customer_id,))
        user_info = self.c.fetchall()
        user_password = user_info[0][3]
        return user_password

    def update_myNewPassword(self, new_password):
        userdata = self.get_loginData()
        customer_id = userdata[2]
        self.c.execute("""
            UPDATE Customer SET password = ? WHERE customer_id = ?
            """, (new_password, customer_id))
        self.conn.commit()
        print("New Password is updated successfully!")

    def get_card_number(self):
        self.c.execute("""
            SELECT card_number FROM Credit_card 
            """)
        card_number = self.c.fetchall()
        return card_number

    def insert_newCardInfo(self, entry_cardNum, entry_cv, entry_expiry, entry_holder):
        userLogined = self.get_loginData()
        customer_id = userLogined[2]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # id not null, need to extract ids
        self.c.execute("""
            INSERT INTO Credit_card (card_number, CV_number, expired_date, card_holder_name, date, customer_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (entry_cardNum, entry_cv, entry_expiry, entry_holder, current_time, customer_id))
        self.conn.commit()
        print("Insert a new card record successfully.")

    def update_credit(self, value):

        # update customer credit
        userdata = self.get_loginData()
        customer_id = userdata[2]
        old_credit = userdata[-1]
        new_credit = old_credit + value
        self.c.execute("""
            UPDATE Customer SET credit = ? WHERE customer_id = ?
            """, (new_credit, customer_id))
        self.conn.commit()
        print("Top_Up finished!")

        # insert a record of Account_history
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.c.execute("""
            INSERT INTO Account_history (customer_id, in_flow, credit, date, type)
            VALUES (?, ?, ?, ?, ?)
            """, (customer_id, value, new_credit, current_time, "Top-up"))
        self.conn.commit()
        print("Adding a new Account_history record successfully! (Top-up)")

    def insert_report(self, report_time, location, bike_type, desc, img_path, err_type):
        guid = self.get_loginData()[2]
        bike_id = self.get_currentBikeInfo()[1]
        self.c.execute("""
            INSERT INTO Error_journal (customer_id, bike_id, starting_date, location, bike_type, description, pic, 
            repair_message, status)
            values(?,?,?,?,?,?,?,?,?)
            """, [guid, bike_id, report_time, location, bike_type, desc, img_path, err_type, "Need to repair"])
        self.conn.commit()

    def select_report_detail(self, report_id):

        self.c.execute("""
            select * from Error_journal where error_journal_id=?
            """, [report_id])
        record = self.c.fetchone()

        return record

    def select_processingRecords(self):

        guid = self.get_loginData()[2]
        self.c.execute(
            """select * from Error_journal where customer_id=? and status='Need to repair'""",
            [guid])
        records = self.c.fetchall()

        return records

    def select_transactionRecords(self, transaction_type):

        userdata = self.get_loginData()
        guid = userdata[2]
        print(guid)
        selected_transaction_type = transaction_type
        if selected_transaction_type == "Top-up":
            self.c.execute("""
                select * from Account_history where customer_id=? and type=?
                """, (guid, selected_transaction_type,))
            records = self.c.fetchall()

            return records
        else:
            selected_transaction_type = "Spend"
            self.c.execute("""
                select * from Account_history where customer_id=? and type=?
                """, (guid, selected_transaction_type,))
            records = self.c.fetchall()
            return records

    def select_rentalHistory(self, select_rent_location, selected_rentbike_type):
        userdata = self.get_loginData()
        guid = userdata[2]

        sql = """select * from Tracking where customer_id=?"""
        args = [guid]
        if select_rent_location:
            sql += " and start_location=? "
            args.append(select_rent_location)
        if selected_rentbike_type:
            sql += " and bike_type=? "
            args.append(selected_rentbike_type)
        self.c.execute(sql, tuple(args))
        records = self.c.fetchall()

        return records

    def select_errHistory(self, report_history_location, report_err_type):

        userdata = self.get_loginData()
        guid = userdata[2]

        sql = "select * from Error_journal where customer_id=?"
        args = [guid]
        if report_history_location:
            sql += " and location=? "
            args.append(report_history_location)
        if report_err_type:
            sql += " and repair_message=? "
            args.append(report_err_type)
        self.c.execute(sql, tuple(args))
        records = self.c.fetchall()

        return records

    def get_customer_credit(self):

        userdata = self.get_loginData()
        customer_id = userdata[2]

        self.c.execute("""
                    select credit from Customer where customer_id=?
                    """, [customer_id])
        credit = self.c.fetchone()
        return credit



class OperatorDatabase:

    def __init__(self):

        self.open_database()

    def open_database(self):

        self.conn = sqlite3.connect("RIDENOW.db")
        self.c = self.conn.cursor()

    def close_database(self):

        self.conn.close()

    # ****************************************get_chargeData*******4situations
    def get_chargeData(self, get_chargeLocation, get_type):  # getting info for charge list

        self.c.execute("""
            SELECT * FROM Bike_info WHERE location = ? and type = ? ORDER BY battery_level
            """, (get_chargeLocation, get_type))
        charge_data = self.c.fetchall()
        return charge_data

    def get_chargeData_l(self, get_chargeLocation):  # getting info for charge list

        self.c.execute("""
            SELECT * FROM Bike_info WHERE location = ? 
            ORDER BY battery_level""", (get_chargeLocation,))
        charge_data = self.c.fetchall()
        return charge_data

    def get_chargeData_t(self, get_type):  # getting info for charge list

        self.c.execute("""
            SELECT * FROM Bike_info WHERE type = ? 
            ORDER BY battery_level""", (get_type,))
        charge_data = self.c.fetchall()
        return charge_data

    def get_chargeData_no(self):  # getting info for charge list

        self.c.execute("""
            SELECT * FROM Bike_info ORDER BY battery_level""")
        charge_data = self.c.fetchall()
        return charge_data

    # ****************************************get_chargeHistory*******4situations
    def get_chargeHistory(self, date, get_type, oid):
        self.c.execute("""
                SELECT bike_id,bike_type,charge_date,operator_id,battery,charge_time FROM Charge_history
                WHERE charge_date = ? and bike_type = ? and operator_id=?
                ORDER BY charge_date ASC 
                """, (date, get_type, oid))
        charge_history = self.c.fetchall()
        return charge_history

    def get_chargeHistory_d(self, date, oid):
        self.c.execute("""
                 SELECT bike_id,bike_type,charge_date,operator_id,battery,charge_time FROM Charge_history
                 WHERE charge_date = ? and operator_id=?
                 ORDER BY charge_date ASC""", (date, oid))
        charge_history = self.c.fetchall()
        return charge_history

    def get_chargeHistory_t(self, get_type, oid):
        self.c.execute("""
                 SELECT bike_id,bike_type,charge_date,operator_id,battery,charge_time FROM Charge_history
                 WHERE bike_type = ? and operator_id=?
                 ORDER BY charge_date ASC""", (get_type, oid))
        charge_history = self.c.fetchall()
        return charge_history

    def get_chargeHistory_no(self, oid):
        self.c.execute("""
                 SELECT bike_id,bike_type,charge_date,operator_id,battery,charge_time FROM Charge_history
                 WHERE operator_id=?
                 ORDER BY charge_date ASC""", (oid,))
        charge_history = self.c.fetchall()
        return charge_history

    # ****************************************get_repairData*******4situations
    def get_repairData(self, get_location, get_type):  # getting info for repair list
        stat = "Need to repair"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,location,starting_time,starting_date FROM Error_journal 
            WHERE location = ? and repair_message = ? and status = ?
            ORDER BY starting_date ASC""", (get_location, get_type, stat))
        repair_data = self.c.fetchall()
        return repair_data

    def get_repairData_l(self, get_location):  # getting info for repair list
        stat = "Need to repair"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,location,starting_time,starting_date FROM Error_journal 
            WHERE location = ? and status = ?
            ORDER BY starting_date ASC""", (get_location, stat))
        repair_data = self.c.fetchall()
        return repair_data

    def get_repairData_t(self, get_type):  # getting info for repair list
        stat = "Need to repair"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,location,starting_time,starting_date FROM Error_journal 
            WHERE repair_message = ? and status = ?
            ORDER BY starting_date ASC""", (get_type, stat))
        repair_data = self.c.fetchall()
        return repair_data

    def get_repairData_no(self):  # getting info for repair list
        print("A")
        stat = "Need to repair"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,location,starting_time,starting_date FROM Error_journal 
            WHERE status = ? ORDER BY starting_date ASC """, (stat,))
        repair_data = self.c.fetchall()
        return repair_data

    # ****************************************get_repairHistory*******4situations
    def get_repairHistory(self, date, get_repairType, oid):  # getting info for repair list
        status = "Completed"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,ending_date,location,ending_time,
            starting_time,starting_date,operator_id,pic,status 
            FROM Error_journal WHERE ending_date = ? and repair_message = ? and status=? and operator_id=?
            ORDER BY ending_date ASC """, (date, get_repairType, status, oid))
        repair_history = self.c.fetchall()
        return repair_history

    def get_repairHistory_d(self, date, oid):  # getting info for repair list
        status = "Completed"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,ending_date,location,ending_time,
            starting_time,starting_date,operator_id,pic,status 
            FROM Error_journal WHERE ending_date = ? and status=? and operator_id=?
            ORDER BY ending_date ASC """, (date, status, oid))
        repair_history = self.c.fetchall()
        return repair_history

    def get_repairHistory_t(self, get_repairType, oid):  # getting info for repair list
        status = "Completed"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,ending_date,location,ending_time,
            starting_time,starting_date,operator_id,pic,status 
            FROM Error_journal WHERE repair_message = ? and status=? and operator_id=?
            ORDER BY ending_date ASC """, (get_repairType, status, oid))
        repair_history = self.c.fetchall()
        return repair_history

    def get_repairHistory_no(self, oid):  # getting info for repair list
        status = "Completed"
        self.c.execute("""
            SELECT bike_id,bike_type,repair_message,ending_date,location,ending_time,
            starting_time,starting_date,operator_id,pic,status 
            FROM Error_journal WHERE status=? and operator_id=? 
            ORDER BY ending_date ASC """, (status, oid))
        repair_history = self.c.fetchall()
        return repair_history

    def get_loginData(self):
        self.c.execute("""
            SELECT * FROM Login_history
            """)
        login_data = self.c.fetchall()
        latest_login = login_data[-1]
        return latest_login

    def bikeType(self):
        type = ["electric_bike", "electric_scooter"]
        return type

    def errorType(self):
        self.c.execute("""
            SELECT DISTINCT repair_message FROM Error_journal
            """)
        error_data = self.c.fetchall()
        return error_data

    def insertChargeHistory(self, bike_id, bike_type, operator_id, battery, charge_time, charge_location, charge_date):
        # def insertChargeHistory(self, data):
        self.c.execute("""
            INSERT INTO Charge_history (bike_id,bike_type,operator_id,battery,charge_time,charge_location,charge_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (bike_id, bike_type, operator_id, battery, charge_time, charge_location, charge_date))
        print("Successfully insert data")
        self.conn.commit()

    def modifybattery(self, bike_id):
        battery = 100
        self.c.execute("""
            UPDATE Bike_info SET battery_level = ? WHERE bike_id = ?
            """, (battery, bike_id))
        self.conn.commit()

    def modifyrepair(self, operator_id, status, ending_time, ending_date, bike_id):
        self.c.execute("""
            UPDATE Error_journal SET operator_id = ? , status=?, ending_time=? , ending_date=? WHERE bike_id = ?
            """, (operator_id, status, ending_time, ending_date, bike_id))
        self.conn.commit()

    def modifystate(self, bike_id):
        status = "Ready to go"
        self.c.execute("""
            UPDATE Bike_info SET status=? WHERE bike_id = ?
            """, (status, bike_id))
        self.conn.commit()

    def getchargedate(self):
        self.c.execute("""
            SELECT charge_date FROM Charge_history
            """)
        date = self.c.fetchall()
        return date

    def get_riding_location(self):
        self.c.execute("""
            SELECT bike_id,MAX(bike_type) AS bike_type, MAX(start_location) AS start_location, 
            MAX(start_time) AS start_time, AVG(battery_level) AS battery_level
            FROM Tracking 
            WHERE end_location IS NULL
            GROUP BY bike_id
            ORDER BY bike_id ASC""")
        riding_location = self.c.fetchall()
        return riding_location

    def get_parking_location(self):

        sta = "On Rental Contract"
        self.c.execute("""
            SELECT bike_id,type,location, battery_level FROM Bike_info
            WHERE bike_id NOT IN
            (SELECT bike_id FROM Tracking WHERE end_location IS NULL)
            ORDER BY bike_id ASC""")
        parking_location = self.c.fetchall()

        return parking_location

####################################################

    def get_MoveData(self):  # getting info for move list

        self.c.execute("""
            SELECT name, num_bike, electric_bike, electric_scooter FROM Parking_lot
            ORDER BY num_bike DESC 
            """)
        move_data = self.c.fetchall()

        return move_data

    def get_MoveLocationData(self, bid):  # getting info for move list

        self.c.execute("""
            SELECT bike_id ,type ,location FROM Bike_info 
            where location = ?
            group by type
            """, (bid,))
        move_data = self.c.fetchall()

        return move_data

    # In different situations
    def get_moveHistory(self, date, get_type):

        self.c.execute("""
            SELECT bike_id,bike_type,ending_location,starting_location,operator_id FROM Move 
            WHERE move_date = ? and bike_type = ?
            """, (date, get_type))
        move_history = self.c.fetchall()

        return move_history

    # no
    def get_moveHistory_no(self):

        self.c.execute("""
            SELECT bike_id,bike_type,ending_location,starting_location,operator_id FROM Move 
            ORDER BY move_date ASC
            """)
        move_history = self.c.fetchall()
        print("This is move_history: ", move_history)

        return move_history

    def get_moveHistory_d(self, date):

        self.c.execute("""
            SELECT bike_id,bike_type,ending_location,starting_location,operator_id FROM Move 
            WHERE move_date = ?
            ORDER BY move_date ASC
            """, (date,))
        move_history = self.c.fetchall()

        return move_history

    def get_moveHistory_t(self, get_type):

        self.c.execute("""
            SELECT bike_id,bike_type,ending_location,starting_location,operator_id FROM Move 
            WHERE bike_type = ?
            """, (get_type,))
        move_history = self.c.fetchall()

        return move_history

    def get_LocationData(self, location):

        sta = "On Rental Contract"
        self.c.execute("""
                 SELECT bike_id,type,location FROM Bike_info 
                 WHERE location = ? and status != ?

                 """, (location, sta))
        LocationData = self.c.fetchall()

        return LocationData

    def get_address(self):

        self.c.execute("""
            SELECT address FROM Parking_lot
            """)
        address = self.c.fetchall()

        return address

    def movingbike(self, bike_id, bike_type, fromLocation, toLocation):

        if bike_type == "electric_bike":

            # reduce the fromLocation Parking_lot's bike numbers
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (fromLocation,))
            fromLocationInfo = self.c.fetchall()
            print(fromLocationInfo)
            print("This Parking_lot has total ", fromLocationInfo[0][2], "bike remained")
            updated_total_num = fromLocationInfo[0][2] - 1
            updated_electric_bike_num = fromLocationInfo[0][4] - 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_bike = ? WHERE name = ?
                """, (updated_total_num, updated_electric_bike_num, fromLocation))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a E_B reduced)")

            # add to toLocation Parking_lot's bike numbers
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (toLocation,))
            print(toLocation, "move to this location")
            toLocationInfo = self.c.fetchall()
            print(toLocationInfo)
            print("This Parking_lot has total ", toLocationInfo[0][2], "bike remained")
            updated_total_num = toLocationInfo[0][2] - 1
            updated_electric_bike_num = toLocationInfo[0][4] - 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_bike = ? WHERE name = ?
                """, (updated_total_num, updated_electric_bike_num, toLocation))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a E_B added)")
        else:
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (fromLocation,))
            fromLocationInfo = self.c.fetchall()
            print(fromLocationInfo)
            print("This Parking_lot has total ", fromLocationInfo[0][2], "bike remained")
            updated_total_num = fromLocationInfo[0][2] - 1
            updated_foot_bike_num = fromLocationInfo[0][5] - 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_scooter = ? WHERE name = ?
                """, (updated_total_num, updated_foot_bike_num, fromLocation))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a F_B reduced)")

            # add to toLocation Parking_lot's bike numbers
            self.c.execute("""
                SELECT * FROM Parking_lot WHERE name = ?
                """, (toLocation,))
            toLocationInfo = self.c.fetchall()
            print(toLocationInfo)
            print("This Parking_lot has total ", toLocationInfo[0][2], "bike remained")
            updated_total_num = toLocationInfo[0][2] - 1
            updated_electric_bike_num = toLocationInfo[0][4] - 1
            self.c.execute("""
                UPDATE Parking_lot SET num_bike = ?, electric_bike = ? WHERE name = ?
                """, (updated_total_num, updated_electric_bike_num, toLocation))
            self.conn.commit()
            print("parking_lot bike numbers updated successfully!(a E_B added)")

        # update bike_location:
        self.c.execute("""
            UPDATE Bike_info SET location = ? WHERE bike_id = ?
            """, (toLocation, bike_id))
        self.conn.commit()
        print("Bike_location updated successfully!(Changed by moving)")


