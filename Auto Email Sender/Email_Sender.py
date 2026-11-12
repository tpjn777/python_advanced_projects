from tkinter import *
import smtplib
import re


root = Tk()
root.title("Promail Application")

f1 = Frame(root, width=1000, height=800)
f1.pack(side=TOP)

label1 = Label(f1, width=25, text='Enter your Credentials', font=("Calibri 18 bold"))
label1.grid(row=0, columnspan=3, pady=10, padx=10)

label2=Label(f1, text="Email").grid(row=1, sticky=E, pady=5, padx=10)
label3 = Label(f1, text="Password").grid(row=2, sticky=E, pady=5, padx=10)

entry1= Entry(f1)
entry2= Entry(f1, show="*")

entry1.grid(row=1, column=1, pady=5)
entry2.grid(row=2, column=1)

btn1 = Button(f1, text="Login", width=10, bg="black", fg="white", command=lambda: login())
btn1.grid(row=3, columnsoan=3, pady=10)

f2 = Frame(root)
f2.pack(side=TOP, expand=NO, fill=NONE)

label4 = Label(f2, width=20, bg="cyan", fg="red", text='log in Success', font=('Calibri 12 bold'))
label4.grid(row=0, column=0, columnspan=2, pady=5)

btn2 = Button(f2, text="Logout", width=10, bg="black", fg="white", command=lambda: logout())
btn2.grid(row=0, column=4, sticky=E, pady=10,  padx=(5,0))