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

def check_password(email,password):
   sql='select password from email where email =%s'
   value=(email,)
   mycursor.execute(sql,value)
   email_password=mycursor.fetchone()
   if(password==''.join(email_password)):
      return True 
   else :
      return False

def check_account(email):
   sql="select email from email where email =%s"
   value=(email,)
   mycursor.execute(sql,value)
   required_email=mycursor.fetchone()
   if(required_email==None):
      return False
   else :
      return True
      

def add(name,last_name,gender,age,SSn,email,password,phone,position="patient"):
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
   elif(position=="admin"):
      admin="INSERT INTO nurses(ssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(admin,value)
   elif(position=='patient'):
      patient="INSERT INTO relatives(id,Fname,Lname,gender) VALUES ((select ID from patients where ID=%s),%s,%s,%s)"
      value=(SSn,name,last_name,gender)
      mycursor.execute(patient,value)
      sql="INSERT INTO relative_phone(pid, relative_name, phone) values ((select ID from patients where ID=%s), %s, %s)"
      val=(SSn,name, phone)
      mycursor.execute(sql, val)
   mydb.commit()

def select_page(email):
   sql = "select ssn, position from email where email = %s"
   val = (email,)
   mycursor.execute(sql, val)
   posSsnList = mycursor.fetchone()
   position = posSsnList[1]
   ssn = posSsnList[0]
   out = [position]
   if (position == 'patient' ):
      sql = "select * from patients where id = %s"
      value = (ssn,)
      mycursor.execute(sql, value)
      data = mycursor.fetchone()
      print(ssn)
      print(data)
      out.append(data)
      return(out)
   elif (position == 'doctor' ):
      return render_template('Patient.html')
   elif (position == 'nurse' ):
      return render_template('Patient.html')
   else:
      return render_template("add_member.html")
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
      position=request.form["position"]
      phone = request.form["phone"]
      print(position)
      if(check_account(email)):
         res = "Sorry but this email is used before"
         return render_template("sign_up.html", result= res)
      else :
         add(name, last_name, gender, age, SSn, email, password, phone, position)
         return render_template('index.html')
   else:
      return render_template('sign_up.html')


@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
   if(request.method=='POST'):
      email=request.form['your_name']
      password=request.form['your_pass']
      print(password)
      if(check_account(email) and check_password(email,password) ):
         data= select_page(email)
         print(data)
         print(data[0])
         if (data[0] == 'patient'):
               sql = "select * from relatives where id = %s"
               val = (data[1][0],)
               mycursor.execute(sql, val)
               relData = mycursor.fetchone()
               print(relData)
               sql1 = "select phone from relative_phone where pid = %s and Relative_name = %s "
               val1 = (data[1][0], relData[1])
               mycursor.execute(sql1, val1)
               Rphone = mycursor.fetchone()
               print(Rphone)
               return render_template('Patient.html', data=data[1], relData=relData, Rphone=Rphone[0], email=email)
         elif (data[0] == 'doctor'):
            return render_template('datatable.html', data=data[1])
         elif (data[0] == 'nurse'):
            return render_template('Nurse.html', data=data[1])
         elif(data[0]=='admin'):
            return render_template('admin_home.html', data=data[1])
         else:
            return render_template("ADD.html")
      else:
         res = "Incorrect password or e-mail if you're not a user then you can just "
         return render_template("sign_up.html", res=res)
   else :
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