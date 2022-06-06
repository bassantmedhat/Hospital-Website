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
AdminName = []
pssn = 0

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
   required_email=mycursor.fetchone()[0]
   if(required_email==None):
      return False
   else :
      return True
      

def add(name,last_name,gender,age,SSn,PSSn,email,password,phone,visiting_hours, entry_date, Room_number,position="relative",):
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
      admin="INSERT INTO admin(ssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(admin,value)
   elif(position=='relative'):
      sql = "select id from patients where pssn=%s"
      val=(PSSn,)
      mycursor.execute(sql, val)
      id = mycursor.fetchone()[0]
      patient="INSERT INTO relatives(id,SSn,Fname,Lname,gender) VALUES ((select ID from patients where ID=%s),%s,%s,%s,%s)"
      value=(id,SSn,name,last_name,gender)
      mycursor.execute(patient,value)
      sql="INSERT INTO relative_phone(pid, relative_name, phone) values ((select ID from patients where ID=%s), %s, %s)"
      val=(id,name, phone)
      mycursor.execute(sql, val)
   elif(position =='patient'):
      patient="INSERT INTO patient(pssn,Fname,Lname,age,gender, visiting_hours, entry_date, Room_number) VALUES (%s,%s,%s,%s,%s, %s, %s, %s)"
      val=(SSn,name,last_name,age,gender,visiting_hours, entry_date, Room_number)
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
      sql='select id from relatives where SSn=%s'
      value=(ssn,)
      mycursor.execute(sql, value)
      id= mycursor.fetchone()
      sql = "select * from patients where id = %s"
      value = id
      mycursor.execute(sql,value)
      data = mycursor.fetchone()
      print(ssn)
      print(data)
      out.append(data)
   return (out)

def doctor_Patients(email):
   sql = "select ssn, position from email where email = %s"
   val = (email,)
   mycursor.execute(sql, val)
   posSsnList = mycursor.fetchone()
   position = posSsnList[1]
   ssn = posSsnList[0]
   out = [position]
   sql="select id from doctors where dssn=%s "
   val=(ssn,)
   mycursor.execute(sql, val)
   id = mycursor.fetchone()
   print(id)
   sql='select Pid from examine where Did=%s '
   val=(id[0],)#We used this notation [0] as  the id is returned in a tuple and mycursor can't execute a tuple instead you may use executemany
   mycursor.execute(sql, val)
   PData = mycursor.fetchall()
   for i in PData:
      sql= "select * from patients where id = %s"
      val=(i[0],)
      mycursor.execute(sql, val)
      out.append(mycursor.fetchone())
   out.append(ssn)
   return out

# name=last_name=gender=password=email=''
# age=SSn=0

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
      PSSn=int(request.form['PSSn'])
      SSn=int(request.form['SSN'])
      email=request.form['email']
      password=request.form['pass']
      position=request.form["position"]
      # position = 'doctor'
      phone = request.form["phone"]
      print(position)
      if(check_account(email)):
         res = "Sorry but this email is used before"
         return render_template("sign_up.html", result=res)
      else :
         add(name, last_name, gender, age, SSn, PSSn, email, password, phone, position)
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
         print("email_checked")
         data= select_page(email) #Retrive the data presented in the page for each email
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
               # return render_template('Patient.html')
               return render_template('Patient.html', data=data[1], relData=relData, Rphone=Rphone[0], email=email)
         elif (data[0] == 'doctor'):
             data=doctor_Patients(email)
             sql='select fname, lname from doctors where dssn=%s'
             val=(data[-1],)
             mycursor.execute(sql, val)
             Dname=mycursor.fetchone()
             print(data)
             return render_template('datatable.html', data=data[1:], DName=Dname)
         elif (data[0] == 'nurse'):
            return render_template('Nurse.html', data=data[1])
         elif(data[0]=='admin'):
            global AdminName
               #Code for getting the name of the admin and render it on the page
            sql="select ssn from email where email=%s"
            val=(email,)
            mycursor.execute(sql, val)
            AdSsn=mycursor.fetchone()[0]
            print(AdSsn)
            sql='select fname,lname from admin where ssn=%s'
            val=(AdSsn,)
            mycursor.execute(sql, val)
            AdName=mycursor.fetchone()
            AdminName = AdName
            print(AdName)
            return render_template('admin_home.html', Name=AdName[0]+' '+AdName[1])
            # return render_template('admin_home.html', data=data[1])
      else:
         print("not correct")
         res = "Incorrect password or e-mail if you're not a user then you can just "
         return render_template("sign_up.html", res=res)
   else :
      return render_template('sign_up.html')

#this function for selecting the page for data
# @app.route("/add_member/<type>", methods=['POST', 'GET'])
# def add_member(type):
#    if(type=='sign_up'):
#       return render_template('addpatientform.html')
#    else:
#       return render_template('add_member.html')

#This code is for generating the data of the members according to position
@app.route('/show_member/<position>', methods=['GET','POST'])
def show_member(position):
   global pssn
   global AdminName
   if (request.method == 'POST'):
      print(position)
      if (position == 'patient'):
         pssn = request.form['pssn']
         print( '#'*20, '\n', pssn)
         sql = 'select * from patients'
         mycursor.execute(sql)
         PData = mycursor.fetchall()
         if(pssn != 0 ):
            sql = 'DELETE FROM patients WHERE pssn=%s '
            val=(pssn,)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=0')
            mycursor.execute(sql, val)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=1')
            mydb.commit()
         return render_template('app-calendar.html', data=PData)
      elif (position == 'nurse'):
         sql = 'select * from nurses'
         mycursor.execute(sql)
         NData = mycursor.fetchall()
         print(NData)
         return render_template('app-chat.html', data=NData)
      elif (position == 'doctor'):
         sql = 'select * from doctors'
         mycursor.execute(sql)
         DData = mycursor.fetchall()
         print('*' * 30)
         print(AdminName)
         return render_template('ticket-list.html', data=DData)
      elif (position == 'admin'):
         return render_template('admin_home.html', Name=AdminName[0] + ' ' + AdminName[1])
      return render_template('index.html')
   else:
      print(position)
      if(position=='patient'):
         print( '#'*20, '\n', pssn)
         sql = 'select * from patients'
         mycursor.execute(sql)
         PData=mycursor.fetchall()
         return render_template('app-calendar.html', data=PData)
      elif(position=='nurse'):
         sql = 'select * from nurses'
         mycursor.execute(sql)
         NData = mycursor.fetchall()
         print(NData)
         return render_template('app-chat.html', data=NData)
      elif(position=='doctor'):
         sql = 'select * from doctors'
         mycursor.execute(sql)
         DData = mycursor.fetchall()
         print('*' * 30)
         print(AdminName)
         return render_template('ticket-list.html', data=DData)
      elif (position == 'admin'):
         return render_template('admin_home.html', Name=AdminName[0]+' '+AdminName[1])
      return render_template('index.html')

#Previnting to Cache the data like executing the back arrow
@app.after_request
def after_request(response):
   response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
   response.headers["Pragma"] = "no-cache"
   response.headers["Expires"] = "0"
   return response

#app.route

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
@app.route("/add_member/<type>", methods=['POST', 'GET'])
def add_member(type):
   print('I"M in')
   if (request.method =='POST'):
      if (type == 'sign_up'):
         print('Entered sign-up')
         name = request.form['name']
         last_name = request.form['last_name']
         Rname = request.form['Rname']
         Remail = request.form['email']
         Rlast_name = request.form['Rlast_name']
         entryDate = request.form['entry']
         ssn = request.form['ssn']
         age = request.form['age']
         room_no = request.form['room_no']
         gender=request.form['gender']
         add(name, last_name, gender, age, ssn, None, None, None, None, None, entryDate, room_no, position='patient')
         return render_template('admin_home.html')
   elif(type=='member'):
         return render_template('add_member.html')
   else:
      return render_template('addpatientform.html')

if __name__ == '__main__':
   app.run()