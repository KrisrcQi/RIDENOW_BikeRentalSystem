# RideNow
![RideNow Logo](logo.png)
RideNow is an E-vehicle shared system designed to provide users with a convenient and fast way to travel.  

Built using python language, importing Tkinter GUI library, connecting to sqlite, and in doing so providing an intuitive interface, secure local database storage, and a lightweight and efficient design for a premium E-vehicle shared experience.


## System Features
The RideNow system consists of three user identities, and the following is a description of the functions of the triple identity:  
* Customer: Customers can rent and return vehicles anywhere in the city, report defects, and pay for their accounts.  
* Operator: The Operator is responsible for tracking the real-time location of the vehicle, recharging depleted vehicles, repairing defective vehicles, and adjusting the location of the vehicle as needed.  
* Manager: The Manager generates visual reports of vehicle activity over a specific time period.  

## System and Environment Requirements
RideNow supports different operating systems (Windows, MacOS)  
There are a few more environments needed to run the project:  
PyCharm IDE / Spyder (Anaconda3)   
Python 3.7 or higher

## Running the project
To run the project, you need to run the **main.py** through the above-mentioned IDE. This python script will install all
required packages if not installed already and start the application to show the login page.
```
python main.py
```

## Application Testing
To access features of RideNow as a user,You can login using the following credentials: 

* Customer: 
  * UserID: 2861948 
  * Password: 123456  
* Operator: 
  * UserID: 2       
  * Password: 123456
* Manager: 
  * UserID: 2 
  * Password: 123456

Our registration function only opens up access to the Customer identity, you can register Customer to log in.  
The tests of our project are mainly accummulated during 2023-10-25 to 2023-10-31, by selecting the date of this period will produce the rich data visualization in the manager section.

