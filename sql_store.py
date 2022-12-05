import sqlite3
import mysql
import pandas as pd
from mysql.connector import Error, errorcode
from _kluce import *


def create_server_connection(host_name=hostsql, user_name="vovo", user_password=vovo_pass_sql):  # passql
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"Something is wrong with your user name or password.. : '{err}'")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(f"Error: '{err}'")
    return connection


def create_db_connection(host_name=hostsql, user_name="vovo", user_password=vovo_pass_sql, dbname='vovo'):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=dbname
        )
        print("MySQL Database connection successful")
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"Something is wrong with your user name or password.. : '{err}'")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(f"Error: '{err}'")
    return connection


def create_database(connection, query, clm=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, clm)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query, clm):
    cursor = connection.cursor()
    try:
        cursor.execute(query, clm)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

create_weather_table = """
CREATE TABLE weather (
  el_id INT PRIMARY KEY,
  town VARCHAR(40) NOT NULL,
  wheather_station VARCHAR(40) NOT NULL,
  ws_id INT,
  temp VARCHAR(10) NOT NULL,
  temp_unit VARCHAR(3),
  humidity VARCHAR(10) NOT NULL,
  hum_unit VARCHAR(3),
  pressure VARCHAR(10) NOT NULL,
  press_unit VARCHAR(5),
  rain_hrs VARCHAR(10),
  rain_hrs_unit VARCHAR(4),
  rain_day VARCHAR(10),
  rain_day_unit VARCHAR(4),
  wind_dir VARCHAR(10),
  wind_vitesse VARCHAR(10),
  wind_vitesse_unit VARCHAR(4),
  wind_rafale VARCHAR(10),
  wind_rafale_unit VARCHAR(4),
  dob TIMESTAMP
  );
"""




"""
INSERT INTO weather VALUES
(1,  'James', 'Smith', 'ENG', NULL, '1985-04-20', 12345, '+491774553676'),
(2, 'Stefanie',  'Martin',  'FRA', NULL,  '1970-02-17', 23456, '+491234567890'), 
(3, 'Steve', 'Wang',  'MAN', 'ENG', '1990-11-12', 34567, '+447840921333'),
(4, 'Friederike',  'Müller-Rossi', 'DEU', 'ITA', '1987-07-07',  45678, '+492345678901'),
(5, 'Isobel', 'Ivanova', 'RUS', 'ENG', '1963-05-30',  56789, '+491772635467'),
(6, 'Niamh', 'Murphy', 'ENG', 'IRI', '1995-09-08',  67890, '+491231231232');
"""

def dooit():
    connection = create_db_connection()  # Connect to the Database
    execute_query(connection, create_weather_table, None)  # Execute our defined query

def insert_weather(str, clm):
    connection = connection = create_db_connection()
    execute_query(connection, str, clm)

def volaj(budm = {'town': 'Budmerice', 'wheather_station': 'NetAtmo WS 1: Kaplnka', 'ws_id': '1', 'temp': 5.0, 'temp_unit': '°C', 'humidity': 100.0, 'hum_unit': '%', 'pressure': 1024.6, 'press_unit': 'mBar', 'rain_hrs': '', 'rain_hrs_unit': '', 'rain_day': '', 'rain_day_unit': '', 'wind_dir': '', 'wind_vitesse': '', 'wind_vitesse_unit': '', 'wind_rafale': '', 'wind_rafale_unit': ''}):
    placeholders = ', '.join(['%s'] * len(budm))
    columns = ', '.join(budm.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('weather', columns, placeholders)
    print (sql )
    print(list(budm.values()))
    insert_weather(sql, list(budm.values()))