

import mysql.connector as mycon
from tkinter import *
from tkinter import messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import ttk
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import seaborn as sn


dolce = Tk()
dolce.geometry("880x800")
dolce.title("Input and Table")

#update entry widgets
a = StringVar()
e2 = Entry(master=dolce, textvar=a)
e2.place(x=400, y=60, width=60)
b = StringVar()
e3 = Entry(master=dolce, textvar=b)
e3.place(x=480, y=60, width=60)
c = StringVar()
e4 = Entry(master=dolce, textvar=c)
e4.place(x=560, y=60, width=60)
d = StringVar()
e5 = Entry(master=dolce, textvar=d)
e5.place(x=640, y=60, width=60)
e = StringVar()
e6 = Entry(master=dolce, textvar=e)
e6.place(x=720, y=60, width=60)



h=StringVar() #delete entry
e9 = Entry(master=dolce, textvar=h)
e9.place(x=800, y=140, width=60)



#display data through Treeview, or essentially creating the graph/chart that displays the given data
tree = ttk.Treeview(dolce, selectmode='browse')
tree.place(x=10, y=10)
#yview scans/calculates the location of the scrollbar (width, length, height) as well as the size of the bar.  
vsb = ttk.Scrollbar(dolce, orient="vertical", command=tree.yview)
vsb.place(x=368, y=10, height=225)

tree.configure(yscrollcommand=vsb.set) #displays only the selected range, it has to be determined by yview

tree["columns"] = ("1", "2", "3", "4", "5")
tree['show'] = 'headings'
tree.column("1", width=70, anchor='c')
tree.column("2", width=70, anchor='c')
tree.column("3", width=70, anchor='c')
tree.column("4", width=70, anchor='c')
tree.column("5", width=70, anchor='c')


tree.heading("1", text="Id")
tree.heading("2", text="School_hrs")
tree.heading("3", text="Self_hrs")
tree.heading("4", text="Tuition_hrs")
tree.heading("5", text="Passed")

#fill the treeview at the form upload
myconnection = mycon.connect(host="localhost",
                             user="root",
                             password="",
                             database="health")

mycursor = myconnection.cursor() #cursor is to query in 2D array
sql = "SELECT * FROM npexam"
mycursor.execute(sql) #execute is to pass sql to MariaDB
   
#my cursor = [ [1, x1, x2, x3], [2, x1, x2, x3], [?]]
#The element of 2D array is still a 1D array.
for x in mycursor:
   
    tree.insert("", 'end', values=( x[0], x[1], x[2], x[3], x[4]))



#draw the simple linear regression at the form upload
student_hrs = []
self_hrs = []
tuition_hrs = []
passed = []


sql = "SELECT * FROM npexam"
mycursor.execute(sql) #execute is to pass sql to MariaDB
   
for x in mycursor:
    student_hrs.append(float(x[1]))
    self_hrs.append(float(x[2]))
    tuition_hrs.append(float(x[3]))
    passed.append(float(x[4]))
   
myconnection.commit()


fig = Figure(figsize = (3,3), dpi = 100)
plot1 = fig.add_subplot(111)
plot1.scatter(student_hrs, self_hrs)
   
canvas = FigureCanvasTkAgg(fig, master=dolce)
canvas.draw()
canvas.get_tk_widget().place(x=40, y=280)  
   
toolbar = NavigationToolbar2Tk(canvas, dolce)
toolbar.place(x=40, y=580)
toolbar.update()

def show(): #connects the mysql database to python
   
    for item in tree.get_children():
        tree.delete(item)
   
    myconnection = mycon.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="health")

    mycursor = myconnection.cursor() #cursor is to query in 2D array
    sql = "SELECT * FROM npexam"
    mycursor.execute(sql) #execute is to pass sql to MariaDB
   
    #my cursor = [ [1, x1, x2, x3], [2, x1, x2, x3], [?]]
    #The element of 2D array is still a 1D array.
    for x in mycursor:
       
        tree.insert("", 'end', values=( x[0], x[1], x[2], x[3], x[4]))

    myconnection.commit()


b1 = Button(master=dolce, text="Show", command=show)
b1.place(x=400, y=20)

def update():
    #Method1: inserting entries to MariaDB
    myconnection = mycon.connect(user="root",
                                 host="localhost",
                                 password="",
                                 database="health")
    mycursor = myconnection.cursor()
    sql = "UPDATE npexam SET school_hrs = %s, self_hrs = %s, tuition_hrs = %s, passed = %s WHERE id = %s"
    val = (str(b.get()), str(c.get()), str(d.get()), str(e.get()), str(a.get())) #entry boxes
   
    mycursor.execute(sql, val)

    myconnection.commit()
   
    #la = Label(master=dolce, text="1 record was updated")
    #la.place(x=20, y=680)
    messagebox.showinfo("Results", "1 record was updated")
   
b3 = Button(master=dolce, text="Update", command=update)
b3.place(x=810, y=20)

def delete():
    #Method1: Deleting a row by id in MariaDB
    myconnection = mycon.connect(user="root",
                                 host="localhost",
                                 password="",
                                 database="health")
    mycursor = myconnection.cursor()
    sql = "DELETE FROM npexam WHERE id=" + h.get()
    mycursor.execute(sql)

    myconnection.commit()
   
    #la = Label(master=dolce, text="1 record was deleted")
    #la.place(x=20, y=680)
    messagebox.showinfo("Results", "1 record was deleted")
   
b4 = Button(master=dolce, text="Delete", command=delete)
b4.place(x=815, y=100)

def plot():

    student_hrs = []
    self_hrs = []
    tuition_hrs = []
    passed = []
   
    myconnection = mycon.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="health")

    mycursor = myconnection.cursor() # cursor is to query
    sql = "SELECT * FROM npexam"
    mycursor.execute(sql) #execute is to pass sql to MariaDB
   
    for x in mycursor:
        student_hrs.append(float(x[1]))
        self_hrs.append(float(x[2]))
        tuition_hrs.append(float(x[3]))
        passed.append(float(x[4]))
   
    myconnection.commit()
   
   
    fig = Figure(figsize = (3,3), dpi = 100)
    plot1 = fig.add_subplot(111)
    plot1.scatter(student_hrs, self_hrs)
   
    canvas = FigureCanvasTkAgg(fig, master=dolce)
    canvas.draw()
    canvas.get_tk_widget().place(x=40, y=280)  
   
    toolbar = NavigationToolbar2Tk(canvas, dolce)
    toolbar.place(x=40, y=580)
    toolbar.update()
   
b5 = Button(master=dolce, text="Plot", command=plot)
b5.place(x=825, y=180)

lab = Label(text="Simple linear regression")
lab.place(x=40, y=250)

le = Label(text="Testing data ratio (0.0 - 1.0) = ")
le.place(x=400, y=250)
aa = StringVar()
ee6 = Entry(master=dolce, textvar=aa)
ee6.place(x=560, y=250, width=60)

lbb = Label(text="n_estimators = ")
lbb.place(x=620, y=250)
bb = StringVar()
ee7 = Entry(master=dolce, textvar=bb)
ee7.place(x=700, y=250, width=60)

def forecast():
    try:
       
        mydb = mycon.connect(host="localhost",
                                       user="root",
                                       password="",
                                       database="health")
        mycursor = mydb.cursor()
        query = "SELECT * FROM npexam"
        df = pd.read_sql(query, con = mydb)
        #df is a dataframe formed by pandas
        print(df.head(12))
       
        mydb.commit()
   
        X = df[['school_hrs', 'self_hrs','tution_hrs']]
        y = df['passed']
       
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size= float(aa.get()) ,random_state=0)
       
        clf = RandomForestClassifier(n_estimators= int(bb.get()))
        clf.fit(X_train,y_train)
       
        y_pred=clf.predict(X_test)
       
       
        lla = Label(dolce, text="Accuracy = ")
        lla.place(x=520, y=750)
       
        k=StringVar()
        e10 = Entry(master=dolce, textvar=k)
        e10.place(x=600, y=750, width=60)
       
       
        k.set("%.2f" % (100*metrics.accuracy_score(y_test, y_pred)))
        #la.place(x=10, y=750)
       
        confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
        #sn.heatmap(confusion_matrix, annot=True)
       
        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.subplots()
        sn.heatmap(confusion_matrix, annot=True,  ax=ax)
       
        canvas = FigureCanvasTkAgg(fig, master=dolce)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=280)  
       
        toolbar = NavigationToolbar2Tk(canvas, dolce)
        toolbar.place(x=400, y=680)
        toolbar.update()
    except:
        messagebox.showinfo("error", "Enter inputs properly")
   
   
b6 = Button(master=dolce, text="Random Forest", command=forecast)
b6.place(x=780, y=250)

dolce.mainloop()