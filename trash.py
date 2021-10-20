from tkinter import messagebox
from kivy.app import App
from kivy.core import window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import pymysql


Window.size=(260, 480)

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.


# Declare both screens
class Welcome(Screen):
    pass

class LoginResident(Screen):
    def open(self):
       
        self.uname.text=""
        self.pwd.text="" 
        self.lblerror.text=""
        self.parent.current='registerresident'
    def welcome(self):
        self.uname.text=""
        self.pwd.text="" 
        self.lblerror.text=""
        self.parent.current='welcome'
    def login(self):    
        if self.uname.text=="" or self.pwd.text=="":
            self.lblerror.text="Username and Password are required"
        else:
            
                con=pymysql.connect(host="localhost", user="root", password="", database="db_event_management")
                cur=con.cursor()
                cur.execute("SELECT * FROM tbl_users where uname=%s and pwd=md5(%s)", (self.uname.text, self.pwd.text))

                row=cur.fetchone()
                if row==None:
                    self.uname.text=""
                    self.pwd.text=""
                    self.lblerror.text="Invalid Username or Password. Please try again"
                else: 
                    con=pymysql.connect(host="localhost", user="root", password="", database="db_event_management")
                    cur=con.cursor()
                    cur.execute("SELECT status FROM tbl_users where uname=%s and pwd=md5(%s) and status='new'", (self.uname.text, self.pwd.text))
                    row=cur.fetchone()
                    if row==None:
                        self.parent.current='registerresident'
                        self.uname.text=""
                        self.pwd.text=""
                        self.lblerror.text=""
                    else:
                        global win
                        win=self.uname.text
                        self.parent.current='address'
                        self.uname.text=""
                        self.pwd.text=""
                        self.lblerror.text=""
                
class RegisterResident(Screen):
    def open(self):
        self.lblsuccess.text=""
        self.uname.text=""
        self.pwd.text="" 
        self.fulln.text=""
        self.lblerror.text=""
        self.parent.current='loginresident'
    def register(self):
        if self.uname.text=="" or self.pwd.text=="" or self.fulln.text=="":
            self.lblerror.text="All fields are required"
        else:
            
                con=pymysql.connect(host="localhost", user="root", password="", database="db_event_management")
                cur=con.cursor()
                cur.execute("SELECT * FROM tbl_users where fname=%s", self.fulln.text)
                row=cur.fetchone()
                if row!=None:
                    self.lblsuccess.text=""
                    self.uname.text=""
                    self.pwd.text="" 
                    self.fulln.text=""
                    self.lblerror.text="User already exists. Please login or modify inputs to register"
                else: 
                    cur.execute("insert into tbl_users (fname, uname,pwd,status) values (%s,%s,md5(%s),'new')", (self.fulln.text, self.uname.text, self.pwd.text))
                    con.commit()
                    con.close()
                    self.lblerror.text=""
                    self.lblsuccess.text="Registered Successfully"
                    self.uname.text=""
                    self.pwd.text="" 
                    self.fulln.text=""  


class LoginStaff(Screen):
    def welcome(self):
        self.uname.text=""
        self.pwd.text="" 
        self.lblerror.text=""
        self.parent.current='welcome' 
    def login(self):    
        if self.uname.text=="" or self.pwd.text=="":
            self.lblerror.text="Username and Password are required"
        else:
            
                con=pymysql.connect(host="localhost", user="root", password="", database="db_event_management")
                cur=con.cursor()
                cur.execute("SELECT * FROM tbl_staffs where name=%s and pwd=md5(%s)", (self.uname.text, self.pwd.text))

                row=cur.fetchone()
                if row==None:
                    self.uname.text=""
                    self.pwd.text=""
                    self.lblerror.text="Invalid user. Try again"
                else: 
                    con=pymysql.connect(host="localhost", user="root", password="", database="db_event_management")
                    cur=con.cursor()
                    cur.execute("SELECT status FROM tbl_staffs where name=%s and pwd=md5(%s) ", (self.uname.text, self.pwd.text))
                    row=cur.fetchone()
                    self.parent.current='registerresident'
                    self.uname.text=""
                    self.pwd.text=""
                    self.lblerror.text=""
                    

class Address(Screen):
    def address(self):    
        if self.no.text=="" or self.st.text==""  or self.brgy.text=="":
            self.lblerror.text="All fields are required"
            
        else:
                global add
                add=self.no.text+' '+self.st.text+' '+self.brgy.text
                con=pymysql.connect(host="localhost", user="root", password="", database="db_event_management")
                cur=con.cursor()
                cur.execute("UPDATE tbl_users set address=%s where fname=%s", (add, win))
                con.commit()
                self.parent.current='phone'
                self.no.text=""
                self.st.text=""
                self.brgy.text=""
                

class Phone(Screen):
    def phone(self):    
        if self.no.text=="":
            self.lblerror.text="Contact Number is required"
            
        else:
                con=pymysql.connect(host="localhost", user="root", password="", database="db_event_management")
                cur=con.cursor()
                cur.execute("UPDATE tbl_users set phone=%s , status='active' where fname=%s", (self.no.text, win))
                con.commit()
                self.parent.current='welcome'
                self.no.text=""
          
class Home(Screen):
    pass
class SettingsScreen(Screen):
    pass
class WindowManager(ScreenManager):
    pass

class ETrashApp(App):
    

    def build(self):
        # Create the screen manager
        Window.clearcolor=(225/255,234/255,249/255,1) 
        
        return Builder.load_file('trash.kv')

if __name__ == '__main__':
    ETrashApp().run()