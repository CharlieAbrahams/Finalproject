from flask import Flask, render_template, request
import sqlite3 as sql
from flask import render_template
import os

app = Flask(__name__)
full_filename = os.path.join('static', 'menu.png')

@app.route('/')
@app.route('/home.html')
def home():
   return render_template("home.html", checken = full_filename)

@app.route('/student.html')
def new_student():
   return render_template('student.html', checken = full_filename)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("list.html",msg = msg, checken = full_filename)
         con.close()
         
@app.route('/list.html')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows, checken = full_filename)

if __name__ == '__main__':
 app.run(debug = True,)