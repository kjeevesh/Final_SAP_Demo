import mysql.connector

mydb = mysql.connector.connect(
  host="20.204.135.69",
  user="root",
  password="Azureuser@123"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE py_test_255")