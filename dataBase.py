import mysql.connector
from flask import Flask, redirect, url_for, request,render_template
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
#   database="ICU"
)
mycursor = mydb.cursor()
# done
'''
mycursor.execute("CREATE DATABASE ICU")
# mycursor.execute("CREATE TABLE doctors(  ID INT AUTO_INCREMENT , dssn bigINT unsigned,Fname varchar(256),Mname varchar(256),Lname varchar(256),age int, gender varchar(16) ,hiring_date DATE, PRIMARY KEY (ID) )")
# mycursor.execute("create table examine (Did int,Pid int )") 
# mycursor.execute("CREATE TABLE patients( ID INT AUTO_INCREMENT , pssn bigINT unsigned,Fname varchar(256),Mname varchar(256),Lname varchar(256),age int, gender varchar(16) , visiting_hours FLOAT,entry_date DATE,states varchar(256),Room_number int,cost double,PRIMARY KEY (ID) )") 
# mycursor.execute("CREATE TABLE disease(id int,FOREIGN KEY (ID) REFERENCES patients(ID),Pssn bigint unsigned,disease varchar(256) )")
# mycursor.execute("CREATE table relatives( ID INT, FOREIGN KEY (ID) REFERENCES patients(ID),Fname varchar(256),Mname varchar(256),Lname varchar(256),gender varchar(16))")
# mycursor.execute("Create TABLE NURSES(ID int ,Nssn bigint unsigned ,Fname varchar(256),Mname varchar(256),Lname varchar(256),age int ,gender varchar(16),Hiring_date date,primary key(ID) )")
# mycursor.execute("CREATE TABLE MEDICINE(ID int AUTO_INCREMENT,Name varchar(256),code varchar(16),availability boolean ,primary key(id) ) ")
# mycursor.execute("CREATE TABLE Relative_Phone(PID int,Relative_name varchar(256) , FOREIGN KEY (PID) REFERENCES patients(ID), phone int ) ")
# mycursor.execute("create table admin (id int auto_increment,ssn bigint unsigned ,fname varchar(256) ,lname varchar(256),age int,gender varchar(256),primary key(id)) ")
# mycursor.execute("create table Email(SSn bigint unsigned,email varchar(256),password varchar(256),position varchar(256) )")

# #relations 

# mycursor.execute("CREATE TABLE MANAGE(DID INT,NID INT)")
# mycursor.execute("CREATE TABLE GIVE (NID INT ,MID INT )")
# mycursor.execute("CREATE TABLE CHECKED(NID INT , PID INT)")
# mycursor.execute("CREATE TABLE WRITE_FOR(DID INT ,MID INT)")
# mycursor.execute("CREATE TABLE TAKE(PID INT,MID INT) ")

'''












# def account_exist(email,password ):
#    sql="select email,password from email where email =%s"
#    value=(email,)
#    mycursor.execute(sql,value)
#    required_email=mycursor.fetchone()
#    if(required_email==None):
#       return False
#    else :
#       return True 
# print(account_exist("mas@gmail.com",'123456789'))

# x="select password,email from email where email = %s"
# value=('ms@gmail.com',)
# mycursor.execute(x,value)
# for x in mycursor.fetchall():
#   print(x)
#   print(len(x))


# mycursor.execute("CREATE TABLE DEPENDENT() ")
# mycursor.execute('SHOW DATABASES')
# for x in mycursor:
#   print(x)