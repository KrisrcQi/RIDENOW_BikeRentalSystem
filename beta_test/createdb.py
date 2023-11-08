#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sqlite3

conn = sqlite3.connect('2BIKE_2.db')
c = conn.cursor()
sql="insert into Tracking (bike_id,start_location,end_location,start_time,end_time,total_rent_time,bike_type,price,battery_level,custom_id) values(?,?,?,?,?,?,?,?,?,?)"
for _time in ['2023-10-28','2023-10-27','2023-10-26','2023-10-25','2023-10-24','2023-10-23','2023-10-22']:
    for i in range(10,24):
        hour=random.randint(10,23)
        c.execute(sql,(435,'Glasgow_Central_Station','Kelvinhaugh_St','{} 10:00:50.850761'.format(_time),'{} {}:11:55.217145'.format(_time,str(10+hour)),'0:00:04.36','foot_bike',3,100,'123456',))

    conn.commit()
#
# sql="insert into Charge_history (bike_id,bike_type,operator_id,battery,charge_time,charge_location) values(?,?,?,?,?,?)"
# for _time in ['2023-10-28','2023-10-27','2023-10-26','2023-10-25','2023-10-24','2023-10-23','2023-10-22']:
#     for i in range(10,random.randint(10,23)):
#         hour=random.randint(10,23)
#         c.execute(sql,(435,'electric_bike',1,1,'{} {}:11:55.217145'.format(_time,str(hour)),'Glasgow_Central_Station',))
#
# conn.commit()