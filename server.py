from flask import Flask, redirect, url_for, request,render_template
from flask import Flask, render_template,Request, request
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="icu"
)
mycursor = mydb.cursor()
AdminName = []
pssn1 = 0
ssn1 = 0
id = 0

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

def Check_SSN(ssn):
   sql='select pssn from patients where pssn=%s'
   val=(ssn,)
   mycursor.execute(sql, val)
   pSsnCheck=mycursor.fetchone()
   sql = 'select ssn from email where ssn=%s'
   val = (ssn,)
   mycursor.execute(sql, val)
   SsnCheck = mycursor.fetchone()
   if(SsnCheck==None and pSsnCheck==None):
      return True
   else:
      return False

def add(name,last_name,gender,age,SSn,PSSn,email,password,phone,position="patient"):
   sql = "INSERT INTO Email (SSn,email,password,position) VALUES (%s,%s,%s,%s)"
   val=(SSn,email,password,position)
   mycursor.execute(sql,val)
   if(position=="doctor"):
      doctor="INSERT INTO doctors (dssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(doctor,value)
   elif(position=="nurse"):
      nurse="INSERT INTO nurses (Nssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(nurse,value)
   elif(position=="admin"):
      admin="INSERT INTO admin(ssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
      value=(SSn,name,last_name,age,gender)
      mycursor.execute(admin,value)
   elif(position=='patient'):
      sql = "select id from patients where pssn=%s"
      val=(PSSn,)
      mycursor.execute(sql, val)
      id = mycursor.fetchone()[0]
      print('this is the ssn',PSSn)
      print('This is the id')
      print(id)
      patient="INSERT INTO relatives(id,SSn,Fname,Lname,gender) VALUES ((select ID from patients where ID=%s),%s,%s,%s,%s)"
      value=(id,SSn,name,last_name,gender)
      mycursor.execute(patient,value)
      print('done r')
      sql="INSERT INTO relative_phone(pid, relative_name, phone) values ((select ID from patients where ID=%s), %s, %s)"
      val=(id,name, phone)
      mycursor.execute(sql, val)
      print('done rp')
   mydb.commit()



# def add(name,last_name,gender,age,SSn,PSSn,email,password,phone, entry_date, Room_number,position="relative"):
#    print('entered add')
#    if(position =='patient'):
#       print('enter patient')
#       patient="INSERT INTO patients(pssn,Fname,Lname,age,gender,entry_date) VALUES (%s,%s,%s,%s, %s, %s)"
#       val=(SSn,name,last_name,age,gender, entry_date)
#       mydb.commit()
#    else:
#     sql = "INSERT INTO Email (SSn,email,password,position) VALUES (%s,%s,%s,%s)"
#     val=(SSn,email,password,position)
#     mycursor.execute(sql,val)
#     if(position=="doctor"):
#       doctor="INSERT INTO doctors (dssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
#       value=(SSn,name,last_name,age,gender)
#       mycursor.execute(doctor,value)
#     elif(position=="nurse"):
#       nurse="INSERT INTO nurses(nssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
#       value=(SSn,name,last_name,age,gender)
#       mycursor.execute(nurse,value)
#     elif(position=="admin"):
#       admin="INSERT INTO admin(ssn,Fname,Lname,age,gender) VALUES (%s,%s,%s,%s,%s)"
#       value=(SSn,name,last_name,age,gender)
#       mycursor.execute(admin,value)
#     elif(position=='relative'):
#       sql = "select id from patients where pssn=%s"
#       val=(PSSn,)
#       mycursor.execute(sql, val)
#       id = mycursor.fetchone()[0]
#       patient="INSERT INTO relatives(id,SSn,Fname,Lname,gender) VALUES ((select ID from patients where ID=%s),%s,%s,%s,%s)"
#       value=(id,SSn,name,last_name,gender)
#       mycursor.execute(patient,value)
#       sql="INSERT INTO relative_phone(pid, relative_name, phone) values ((select ID from patients where ID=%s), %s, %s)"
#       val=(id,name, phone)
#       mycursor.execute(sql, val)
#    mydb.commit()

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
   global AdminName, dat, Dnam
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
             sql='select fname, lname, id from doctors where dssn=%s'
             val=(data[-1],)
             mycursor.execute(sql, val)
             Dname=mycursor.fetchone()
             Dnam = Dname
             dat=data
             print(data)
             if(data[1]==None):
                return render_template('datatable.html', DName=Dname)
             else:
               return render_template('datatable.html', data=data[1:], DName=Dname)
         elif (data[0] == 'nurse'):
            return render_template('Nurse.html', data=data[1])
         elif(data[0]=='admin'):
               #Code for getting the name of the admin and render it on the page
            sql="select ssn from email where email=%s"
            val=(email,)
            mycursor.execute(sql, val)
            AdSsn=mycursor.fetchone()[0]
            print(AdSsn)
            print('123')
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

@app.route('/writeprescriotion', methods=['POST', 'GET'])
def WP():
   if(request.method=='POST'):
      global dat
      global Dnam
      dID= Dnam[2]
      # DID = request.form['DID']
      PID = request.form['PID']
      prescription =request.form['Pres']
      sql = 'insert into write_Prescription_for (DID,PID,Prescription) values (%s,%s,%s)'
      val=(dID, PID, prescription)
      mycursor.execute(sql, val)
      mydb.commit()
      print('From WR', PID, dID, prescription)
      if(PID):
         return render_template('datatable.html', data=dat[1:], DName=Dnam)
      else:
         return('Very sad Anyway')
@app.route('/add_patient',methods=['GET','POST'])
def add_patient():
   global AdminName
   if(request.method=='POST'):
      name = request.form['name']
      last_name = request.form['last_name']
      Doctor_id = request.form['doc-id']
      disease = request.form['disease']
      entry_date = request.form['entry']
      PSSn = request.form['SSN']
      age = request.form['age']
      room_no = request.form['room_no']
      gender=request.form['gander']
      if(Check_SSN(PSSn)):
         patient_data(name,last_name,Doctor_id,disease,entry_date,PSSn,age,room_no,gender)
         print('done successfully')
         return render_template('admin_home.html',Name=AdminName[0]+' ' + AdminName[1])
      else:
         print("not correct")
         res = "This SSN is already exist "
         return render_template("addpatientform.html", res=res)
def patient_data(name,last_name,Doc_id,disease,entry_date,PSSn,age,room_no,gender):
   sql='insert into patients(Fname,Lname,PSSn,age,gender,entry_date,room_number) values(%s,%s,%s,%s,%s,%s,%s)'
   value=(name,last_name,PSSn,age,gender,entry_date, room_no)
   mycursor.execute(sql,value)
   Id='select id from patients where pssn=%s'
   Val=(PSSn,)
   mycursor.execute(Id, Val)
   Pid=mycursor.fetchone()
   print(Pid)
   sql='insert into examine (Pid, Did) values (%s,%s)'
   val=(Pid[0],Doc_id)
   mycursor.execute(sql,val)
   Add_to_Disease(Pid[0],disease,PSSn)
   mydb.commit()
def Add_to_Disease(id,disease,pssn):
   sql='insert into disease(id,pssn,disease) values (%s,%s,%s)'
   val=(id,pssn,disease)
   mycursor.execute(sql,val)
#this function for selecting the page for data
@app.route("/add_member/<type>", methods=['POST', 'GET'])
def add_member(type):
   if(type=='sign_up'):
      return render_template('addpatientform.html')
   else:
      return render_template('add_member.html')

#This code is for generating the data of the members according to position
@app.route('/show_member/<position>', methods=['GET','POST'])
def show_member(position):
   c = 0
   global ssn1, pssn1
   global AdminName, id, pos
   if (request.method == 'POST'):
      pos = position
      print(position)
      if (position == 'patient'):
         print( '#'*20, '\n', pssn1)
         sql = 'select * from patients'
         mycursor.execute(sql)
         PData = mycursor.fetchall()
         # pssn1 = request.form['pssn']
         pid = request.form['pid']
         if(pid != 0 ):
            # sql='select id from patients where pssn=%s'
            # val=(pssn1,)
            # mycursor.execute(sql, val)
            # print("%%%%",pssn1,"%%%%")
            # pid = mycursor.fetchone()[0]
            # print(pid)
            Examine='delete from examine where Pid=%s'
            ExamineVal=(pid,)
            mycursor.execute(Examine,ExamineVal)
            sql = 'DELETE FROM patients WHERE id=%s '
            val=(pid,)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=0')
            mycursor.execute(sql, val)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=1')
            mydb.commit()
         return render_template('app-calendar.html', data=PData, Name=AdminName[0] + ' ' + AdminName[1])
      elif (position == 'nurse'):
         # ssn1 = request.form['ssn']
         nid = request.form['nid']
         sql = 'select * from nurses'
         mycursor.execute(sql)
         NData = mycursor.fetchall()
         print(NData)
         if (nid != 0):
            # sql = 'select id from nurses where nssn=%s'
            # val = (ssn1,)
            # mycursor.execute(sql, val)
            # nid = mycursor.fetchone()[0]
            # print(nid)
            # # Examine = 'delete from examine where Pid=%s'
            # # ExamineVal = (nid[0],)
            # # mycursor.execute(Examine, ExamineVal)
            sql = 'DELETE FROM nurses WHERE id=%s '
            val = (nid,)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=0')
            mycursor.execute(sql, val)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=1')
            mydb.commit()
         return render_template('app-chat.html', data=NData, Name=AdminName[0] + ' ' + AdminName[1])
      elif (position == 'doctor'):
         # ssn1 = request.form['ssn']
         did = request.form['did']
         sql = 'select * from doctors'
         mycursor.execute(sql)
         DData = mycursor.fetchall()
         print('*' * 30)
         print(AdminName)
         if (did != 0):
            # sql = 'select id from doctors where dssn=%s'
            # val = (ssn1,)
            # mycursor.execute(sql, val)
            # did = mycursor.fetchone()[0]
            # print(did)
            Examine = 'delete from examine where did=%s'
            ExamineVal = (did[0],)
            mycursor.execute(Examine, ExamineVal)
            sql = 'DELETE FROM doctors WHERE id=%s '
            val = (did,)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=0')
            mycursor.execute(sql, val)
            mycursor.execute('SET FOREIGN_KEY_CHECKS=1')
            mydb.commit()
         return render_template('ticket-list.html', data=DData,Name=AdminName[0] + ' ' + AdminName[1])
      elif (position == 'admin'):
         return render_template('admin_home.html', Name=AdminName[0] + ' ' + AdminName[1])
      return render_template('index.html')
   else:
      print(position)
      if(position=='patient'):
         print( '#'*20, '\n', pssn1)
         sql = 'select * from patients'
         mycursor.execute(sql)
         PData=mycursor.fetchall()
         return render_template('app-calendar.html', data=PData, Name=AdminName[0]+' '+AdminName[1])
      elif(position=='nurse'):
         sql = 'select * from nurses left outer join email on Nssn=SSn'
         mycursor.execute(sql)
         NData = mycursor.fetchall()
         print(NData)
         return render_template('app-chat.html', data=NData, Name=AdminName[0]+' '+AdminName[1])
      elif(position=='doctor'):
         sql = 'select * from doctors'
         mycursor.execute(sql)
         DData = mycursor.fetchall()
         print('*' * 30)
         print(AdminName)
         return render_template('ticket-list.html', data=DData, Name=AdminName[0]+' '+AdminName[1])
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


if __name__ == '__main__':
   app.run()