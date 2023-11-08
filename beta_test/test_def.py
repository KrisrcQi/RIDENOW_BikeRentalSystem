import random
import string
import numpy as np
import sqlite3
from ManipulateDatabase import OperatorDatabase
from tkinter import *
import tkintermapview           # https://github.com/TomSchimansky/TkinterMapView


# def generate_username(length=8):
#     # You can customize the characters or words used in the username
#     characters = string.ascii_letters + string.digits  # includes letters and digits
#     username = ''.join(random.choice(characters) for _ in range(length))
#     return username
#
# name = "User{}".format(generate_username(8))
#
# print(name)
#
# id_data = [(2727874,), (2737427,), (2798523,), (2861948,), (2988533,), (2988539,), (2988578,)]
#
# # Extract the integers and convert them to strings
# id_strings = [str(item[0]) for item in id_data]
#
# # Join the strings into a single string
# result_string = ', '.join(id_strings)
#
# # Print or use the result
# print(result_string)

# conn = sqlite3.connect("RIDENOW.db")
# c = conn.cursor()
#
# selected_category = "electric_bike"
# selected_location = "Glasgow central station"
#
# if selected_category == "electric_bike":
#     # Use the column name, not the placeholder, in the WHERE clause
#     c.execute("SELECT electric_bike FROM Parking_lot WHERE name = ?", (selected_location,))
#     bike_number_selected = c.fetchall()
# else:
#     # Use the column name, not the placeholder, in the WHERE clause
#     c.execute("SELECT foot_bike FROM Parking_lot WHERE name = ?", (selected_location,))
#     bike_number_selected = c.fetchall()
#
# print(bike_number_selected)

# data = [(5502130022450476,), (5236497993045254,), (1234567890987654,), (9807123456781234,)]
#
# for tup in data:
#     for num in tup:
#         print(num)
#
# numbers = [num for tup in data for num in tup]
# print(numbers)
#
# def mask_card_number(card_number):
#     # Ensure the card number is a string
#     card_number = str(card_number)
#
#     # Keep the last 4 digits
#     last_4_digits = card_number[-4:]
#
#     # Mask the rest with "x"
#     masked_part = "x" * (len(card_number) - 4)
#
#     # Add spaces every 4 "x" characters
#     masked_number = " ".join([masked_part[i:i+4] for i in range(0, len(masked_part), 4)])
#
#     # Combine the masked part with the last 4 digits
#     masked_card_number = masked_number + last_4_digits
#
#     return masked_card_number
#
# # Example usage:
# maskedCard = []
# for card_number in numbers:
#     masked_card = mask_card_number(card_number)
#     maskedCard.append(masked_card)
# print(maskedCard)  # Outputs "x x x x 3456"

# root = Tk()
# root.title("map")
# root.geometry("900x700")
#
# l_map = LabelFrame(root)
# l_map.pack(pady=20)
#
# map_widget = tkintermapview.TkinterMapView(l_map, width = 800, height = 600, corner_radius=0)
# map_widget.set_position(55.87180409870281, -4.288428799073684)
#
# root.mainloop()








