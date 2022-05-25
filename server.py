from flask import Flask, redirect, url_for, request,render_template
from flask import Flask, render_template,Request, request
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="ICU"
)
mycursor = mydb.cursor()

def add(name,last_name,gender,age,SSn,email,password,position="patient"):
   sql = "INSERT INTO Email (SSn,email,password,position) VALUES (%s,%s,%s,%s)"
   val=(SSn,email,password,position)
   mycursor.execute(sql,val)
   if(position=="doctor"):
      doctor="INSERT INTO doctors (dssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(doctor,value)
   elif(position=="nurse"):
      nurse="INSERT INTO nurses(nssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(nurse,value)
   elif(position=='patient'):
      patient="INSERT INTO patients(pssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(patient,value)
   mydb.commit()


name=last_name=gender=password=email=''
age=SSn=0
app = Flask(__name__)
@app.route('/',methods=['get','post'])
def index():
   return render_template('index.html')
@app.route('/sign_up',methods=['GET','POST'])
def sign_up():
   if(request.method=='POST'):
      name=request.form['name']
      last_name=request.form['last_name']
      gender=request.form['gander']
      age=int(request.form['age'])
      SSn=int(request.form['SSN'])
      email=request.form['email']
      password=request.form['pass']
      add(name,last_name,gender,age,SSn,email,password)
      return render_template('index.html')
   else:
      return render_template('sign_up.html')

# mycursor.execute("insert into Email(email,password) values(email,password)")

# @app.route('/',methods=['get','post'])
# def index():
#    if(request.method=='POST'):
#       name=request.form['user Name']
#       if(name=="abram"):
#          return render_template('welcome.html')
#       else:
#          return render_template('index.html')
   
# @app.route('/main')
# def main():
#    return render_template('/main.html')

if __name__ == '__main__':
   app.run()
