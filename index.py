#Billing App
# note: display resolution 1920x1080
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
from tkinter.ttk import Treeview
from tkinter import messagebox
import sqlite3
from ttkwidgets.autocomplete import AutocompleteCombobox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage


root = customtkinter.CTk()
root.title("Ak App")
root.geometry('1920x1080+0+0')               #'1150x650+100+20'

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


#product db
connection=sqlite3.connect('Database.db')
cursor=connection.cursor()
cursor.execute('create table if not exists product_details (name text,quantity int,cost int)')

cursor.execute('create table if not exists employee_details (employee text,age int, qualification text,gender text,contact int,mail text)')

cursor.execute('create table if not exists customer_details (Customer Name text,Contact No int,Mail Id text,Product Name text,Cost int,Quantity text)')

#login page background image
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo

image = Image.open('i.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = ttk.Label(root, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)

#manager or employee login page

def home():

    root.withdraw()

    global win

    win = customtkinter.CTkToplevel()
    win.title("Ak App")
    win.geometry('1920x1080+0+0')

    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("green")

    def resize_image(event):
        new_width = event.width
        new_height = event.height
        image = copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        label.config(image = photo)
        label.image = photo

    image = Image.open('i.jpg')
    copy_of_image = image.copy()
    photo = ImageTk.PhotoImage(image)
    label = ttk.Label(win, image = photo)
    label.bind('<Configure>', resize_image)
    label.pack(fill=BOTH, expand = YES)


    title=customtkinter.CTkLabel(win,text="Login As ?",font=("Berlin Sans FB Demi",30),fg_color="black")
    title.place(x=380,y=150)

    b=customtkinter.CTkButton(win,text="Manager",font=("Centaur",20,"bold"),bg_color="black",width=130,height=130,corner_radius=30,fg_color="#191B1C",command=manager)
    b.place(x=250,y=300)


    b=customtkinter.CTkButton(win,text="Employee",font=("Centaur",20,"bold"),bg_color="black",width=130,height=130,corner_radius=30,fg_color="#191B1C",command=employee)
    b.place(x=550,y=300)

#manager page

def manager():

    win.withdraw()

    w = customtkinter.CTkToplevel()
    w.geometry('1920x1080+0+0')
    w.title("ak app")

    # product add db
    def add():
        product = product_entry.get()
        cost = cost_entry.get()
        quantity = quantity_entry.get()
        cursor.execute('insert into product_details values(?,?,?)', [product, cost, quantity])
        connection.commit()
        messagebox.showinfo('From Ak App', "Items Added Successfully!!")
        product_entry.delete(0, END)
        cost_entry.delete(0, END)
        quantity_entry.delete(0, END)

    # employee add db

    def add_employee():
        name = employee_name_entry.get()
        age = age_entry.get()
        qualification = qualification_entry.get()
        gender = gender_entry.get()
        contact = contact_entry.get()
        mail = mail_entry.get()
        cursor.execute('insert into employee_details values(?,?,?,?,?,?)',[name, age, qualification, gender, contact, mail])
        connection.commit()
        messagebox.showinfo('From Ak App', "Employee Added Successfully!!")
        employee_name_entry.delete(0, END)
        age_entry.delete(0, END)
        qualification_entry.delete(0, END)
        gender_entry.delete(0, END)
        contact_entry.delete(0, END)
        mail_entry.delete(0, END)

#product page update prodcut option

    def update_item(event):

        global updatewindow
        global product,cost,quantity

        updatewindow = customtkinter.CTkToplevel()
        updatewindow.geometry("600x400+730+250")
        updatewindow.config(background="#5C666B")

        product_title = customtkinter.CTkLabel(updatewindow, text="Update Items", font=("Berlin Sans FB Demi", 18),
                                               fg_color="#5C666B", text_color="black")
        product_title.place(x=30, y=50)

        product=StringVar()
        product_name_title = customtkinter.CTkLabel(updatewindow, text="Product Name ",
                                                    font=("Centaur", 20, "bold"),
                                                    fg_color="#5C666B", text_color="black")
        product_name_title.place(x=130, y=100)

        cost=IntVar()
        cost_title = customtkinter.CTkLabel(updatewindow, text="Cost ", font=("Centaur", 20, "bold"),
                                            fg_color="#5C666B", text_color="black")
        cost_title.place(x=130, y=150)

        quantity=IntVar()
        quantity_title = customtkinter.CTkLabel(updatewindow, text="Quantity ", font=("Centaur", 20, "bold"),
                                                fg_color="#5C666B", text_color="black")
        quantity_title.place(x=130, y=200)

        product_entry = customtkinter.CTkEntry(updatewindow,textvariable=product, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                               border_color="#191B1C", text_color="white")
        product_entry.place(x=280, y=100)

        cost_entry = customtkinter.CTkEntry(updatewindow,textvariable=cost, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                            border_color="#191B1C", text_color="white")
        cost_entry.place(x=280, y=150)

        quantity_entry = customtkinter.CTkEntry(updatewindow,textvariable=quantity, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                                border_color="#191B1C", text_color="white")
        quantity_entry.place(x=280, y=200)

        update_button = customtkinter.CTkButton(updatewindow, text="Update", font=("Centaur", 17),
                                             bg_color="#5C666B", width=100, corner_radius=30, fg_color="#191B1C",
                                             command=update)
        update_button.place(x =300, y=300)

        selected_item=tree.selection()

        values=tree.item(selected_item,"values")


        product.set(values[0])
        cost.set(values[1])
        quantity.set(values[2])

#product page delete option

    def delete(event):
        selected_item=tree.selection()

        values=tree.item(selected_item,"values")
        name=values[0]

        res=messagebox.askyesno("From App","Are you sure ?")
        if res:
            cursor.execute('delete from product_details where name=?',[name])
            connection.commit()
            stock_details()

#product page updadte product db
    def update():
        name=product.get()
        price=cost.get()
        qty=quantity.get()
        cursor.execute('update product_details set cost=?,quantity=? where name=?',[price,qty,name] )
        connection.commit()

        updatewindow.withdraw()
        stock_details()


#employee update page

    def update_emp(event):

        global updatewindowemp

        updatewindowemp = customtkinter.CTkToplevel()
        updatewindowemp.geometry("750x400+600+240")
        updatewindowemp.config(background="#5C666B")

        global ename, age, qualification, gender, contact, mail

        update_employee_title = customtkinter.CTkLabel(updatewindowemp, text="Update Employee",
                                                       font=("Berlin Sans FB Demi", 18), fg_color="#5C666B",
                                                       text_color="black")
        update_employee_title.place(x=30, y=50)

        ename = StringVar()
        employee_name_title = customtkinter.CTkLabel(updatewindowemp, text="Employee Name ",
                                                     font=("Centaur", 20, "bold"), fg_color="#5C666B",
                                                     text_color="black")
        employee_name_title.place(x=50, y=120)

        age = IntVar()
        age_title = customtkinter.CTkLabel(updatewindowemp, text="Age ", font=("Centaur", 20, "bold"),
                                           fg_color="#5C666B", text_color="black")
        age_title.place(x=50, y=170)

        qualification = StringVar()
        qualification_title = customtkinter.CTkLabel(updatewindowemp, text="Qualification ",
                                                     font=("Centaur", 20, "bold"), fg_color="#5C666B",
                                                     text_color="black")
        qualification_title.place(x=50, y=220)

        employee_name_entry = customtkinter.CTkEntry(updatewindowemp, textvariable=ename, font=("Centaur", 20),
                                                     fg_color="#5C666B",
                                                     width=180, border_color="#191B1C", text_color="white")
        employee_name_entry.place(x=200, y=120)

        age_entry = customtkinter.CTkEntry(updatewindowemp, textvariable=age, font=("Centaur", 20), fg_color="#5C666B",
                                           width=180,
                                           border_color="#191B1C", text_color="white")
        age_entry.place(x=200, y=170)

        qualification_entry = customtkinter.CTkEntry(updatewindowemp, textvariable=qualification, font=("Centaur", 20),
                                                     fg_color="#5C666B",
                                                     width=180, border_color="#191B1C", text_color="white")
        qualification_entry.place(x=200, y=220)

        # add employee right
        gender = StringVar()
        gender_title = customtkinter.CTkLabel(updatewindowemp, text="Gender ", font=("Centaur", 20, "bold"),
                                              fg_color="#5C666B", text_color="black")
        gender_title.place(x=430, y=120)

        contact = IntVar()
        contact_title = customtkinter.CTkLabel(updatewindowemp, text="Contact No ", font=("Centaur", 20, "bold"),
                                               fg_color="#5C666B",
                                               text_color="black")
        contact_title.place(x=430, y=170)

        mail = StringVar()
        mail_title = customtkinter.CTkLabel(updatewindowemp, text="Mail Id ", font=("Centaur", 20, "bold"),
                                            fg_color="#5C666B", text_color="black")
        mail_title.place(x=430, y=220)

        gender_entry = customtkinter.CTkEntry(updatewindowemp, textvariable=gender, font=("Centaur", 20),
                                              fg_color="#5C666B", width=180,
                                              border_color="#191B1C", text_color="white")
        gender_entry.place(x=540, y=120)

        contact_entry = customtkinter.CTkEntry(updatewindowemp, textvariable=contact, font=("Centaur", 20),
                                               fg_color="#5C666B", width=180,
                                               border_color="#191B1C", text_color="white")
        contact_entry.place(x=540, y=170)

        mail_entry = customtkinter.CTkEntry(updatewindowemp, textvariable=mail, font=("Centaur", 20),
                                            fg_color="#5C666B", width=180,
                                            border_color="#191B1C", text_color="white")
        mail_entry.place(x=540, y=220)

        update_button = customtkinter.CTkButton(updatewindowemp, text="Update", font=("Centaur", 17),
                                                bg_color="#5C666B", width=100, corner_radius=30, fg_color="#191B1C",
                                                command=update_e)
        update_button.place(x=350, y=320)

        selected_item=tree.selection()

        values=tree.item(selected_item,"values")


        ename.set(values[0])
        age.set(values[1])
        qualification.set(values[2])
        gender.set(values[3])
        contact.set(values[4])
        mail.set(values[5])


#employee delete option
    def delete_emp(event):
        selected_item=tree.selection()

        values=tree.item(selected_item,"values")
        employee=values[0]

        res=messagebox.askyesno("From App","Are you sure you want to delete ?")
        if res:
            cursor.execute('delete from employee_details where employee=?',[employee])
            connection.commit()

            stock_details_emp()


    def update_e():
        employee=ename.get()
        emp_age= age.get()
        emp_qualification=qualification.get()
        emp_gender=gender.get()
        emp_contact=contact.get()
        emp_mail=mail.get()

        cursor.execute('update employee_details set age=?,qualification=?,gender=?,contact=?,mail=? where employee=?',[emp_age ,emp_qualification,emp_gender,emp_contact,emp_mail,employee] )
        connection.commit()

        updatewindowemp.withdraw()
        stock_details_emp()



#product stock detail

    def stock_details():

        frame = customtkinter.CTkFrame(product_frame, width=800, height=380, fg_color="#474D50", bg_color="#5C666B",
                                       corner_radius=20)
        frame.place(x=130, y=200)


        data = cursor.execute('select * from product_details')
        d = data.fetchall()

        style = ttk.Style(w)
        style.theme_use("default")
        style.configure("Treeview", fieldbackground="#474D50",background="#474D50", foreground="white", rowheight=35,font=("Centaur",17,"bold"), borderwidth=7, relief="raised")
        style.configure("Treeview.Heading", fieldbackground="#5C666B", background="black", foreground="white",font=("Centaur",20,"bold"))
        style.map("Treeview", background=[("selected", "#1F663A")])
        global tree


        tree = Treeview(frame, columns=('col1', 'col2', 'col3'), show='headings')
        tree.heading('col1', text='Product')
        tree.heading('col2', text='Cost')
        tree.heading('col3', text='Quantity')
        tree.place(x=50, y=50,width=1100,height=470)

        for i in d:
            tree.insert("", "end", values=i)

        tree.bind('<Return>', update_item)
        tree.bind("<Double-1>", update_item)
        tree.bind('<Delete>', delete)

#product add item

    def add_item():

        global product_entry, cost_entry, quantity_entry

        frame = customtkinter.CTkFrame(product_frame, width=800, height=380, fg_color="#474D50", bg_color="#5C666B",
                                       corner_radius=20)
        frame.place(x=130, y=200)

        product_title = customtkinter.CTkLabel(product_frame, text="Add Items", font=("Berlin Sans FB Demi", 18),
                                               fg_color="#474D50", text_color="black")
        product_title.place(x=200, y=250)

        product_name_title = customtkinter.CTkLabel(product_frame, text="Product Name ",
                                                    font=("Centaur", 20, "bold"),
                                                    fg_color="#474D50", text_color="black")
        product_name_title.place(x=300, y=320)

        cost_title = customtkinter.CTkLabel(product_frame, text="Cost ", font=("Centaur", 20, "bold"),
                                            fg_color="#474D50", text_color="black")
        cost_title.place(x=300, y=370)

        quantity_title = customtkinter.CTkLabel(product_frame, text="Quantity ", font=("Centaur", 20, "bold"),
                                                fg_color="#474D50", text_color="black")
        quantity_title.place(x=300, y=420)

        product_entry = customtkinter.CTkEntry(product_frame, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                               border_color="#191B1C", text_color="white")
        product_entry.place(x=500, y=320)

        cost_entry = customtkinter.CTkEntry(product_frame, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                            border_color="#191B1C", text_color="white")
        cost_entry.place(x=500, y=370)

        quantity_entry = customtkinter.CTkEntry(product_frame, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                                border_color="#191B1C", text_color="white")
        quantity_entry.place(x=500, y=420)

        add_button = customtkinter.CTkButton(product_frame, text="Add", font=("Centaur", 17),
                                             bg_color="#474D50", width=100, corner_radius=30, fg_color="#191B1C",
                                             command=add)
        add_button.place(x=500, y=500)


 # prodct main page

    def product_page():

        global product_frame

        product_frame = customtkinter.CTkFrame(main_frame, width=1050, height=700, fg_color="#5C666B")
        product_frame.place(x=0, y=0)

        lb2 = customtkinter.CTkLabel(product_frame, text="Product Details", font=("Berlin Sans FB Demi", 25),
                                     fg_color="#5C666B", text_color="black")
        lb2.place(x=450, y=40)

        product_entry = customtkinter.CTkEntry(product_frame, font=("Centaur", 20), fg_color="#5C666B", width=200,
                                               border_color="#191B1C", text_color="black")
        product_entry.place(x=100, y=140)

        search_button = customtkinter.CTkButton(product_frame, text="Search", font=("Centaur", 13), bg_color="#5C666B",
                                                width=50, height=10,corner_radius=60, fg_color="#191B1C")
        search_button.place(x=325, y=145)

        add_product_button = customtkinter.CTkButton(product_frame, text="Add Product", font=("Centaur", 17),
                                                     bg_color="#5C666B", width=100,corner_radius=30, fg_color="#191B1C", command=add_item)
        add_product_button.place(x=500, y=600)

        lb12 = customtkinter.CTkLabel(product_frame, text="Welcome to Product Page", font=("Magneto", 40),
                                      fg_color="#5C666B", text_color="black")
        lb12.place(x=300, y=340)

        stock_product = customtkinter.CTkButton(product_frame, text="Stock Details", font=("Centaur", 17),
                                                bg_color="#5C666B", width=200,corner_radius=30, fg_color="#191B1C",command=stock_details)
        stock_product.place(x=750, y=140)


#employee stock details


    def stock_details_emp():

        frame = customtkinter.CTkFrame(employee_frame, width=800, height=380, fg_color="#474D50", bg_color="#5C666B",
                                       corner_radius=20)
        frame.place(x=130, y=200)


        data = cursor.execute('select * from employee_details')
        d = data.fetchall()

        style = ttk.Style(w)
        style.theme_use("default")
        style.configure("Treeview", fieldbackground="#474D50",background="#474D50", foreground="white", rowheight=35,font=("Centaur",17,"bold"), borderwidth=7, relief="raised")
        style.configure("Treeview.Heading", fieldbackground="#5C666B", background="black", foreground="white",font=("Centaur",18,"bold"))
        style.map("Treeview", background=[("selected", "#1F663A")])

        global tree

        tree = Treeview(frame, columns=('col1', 'col2', 'col3','col4','col5','col6'), show='headings')
        tree.heading('col1', text='Name')
        tree.heading('col2', text='Age')
        tree.heading('col3', text='Qualification')
        tree.heading('col4', text='Gender')
        tree.heading('col5', text='Contact')
        tree.heading('col6', text='mail')
        tree.place(x=50, y=50,width=1100,height=470)

        for i in d:
            tree.insert("", "end", values=i)


        tree.bind('<Return>', update_emp)
        tree.bind("<Double-1>", update_emp)
        tree.bind('<Delete>', delete_emp)



#employee add option

    def add_emp():

        global employee_name_entry, age_entry, qualification_entry, gender_entry, contact_entry, mail_entry

        frame = customtkinter.CTkFrame(employee_frame, width=800, height=380, fg_color="#474D50",
                                       bg_color="#5C666B", corner_radius=20)
        frame.place(x=130, y=200)

        add_employee_title = customtkinter.CTkLabel(employee_frame, text="Add Employee",
                                                    font=("Berlin Sans FB Demi", 18), fg_color="#474D50",
                                                    text_color="black")
        add_employee_title.place(x=180, y=250)

        employee_name_title = customtkinter.CTkLabel(employee_frame, text="Employee Name ",
                                                     font=("Centaur", 20, "bold"), fg_color="#474D50",
                                                     text_color="black")
        employee_name_title.place(x=180, y=320)

        age_title = customtkinter.CTkLabel(employee_frame, text="Age ", font=("Centaur", 20, "bold"),
                                           fg_color="#474D50", text_color="black")
        age_title.place(x=180, y=370)

        qualification_title = customtkinter.CTkLabel(employee_frame, text="Qualification ",
                                                     font=("Centaur", 20, "bold"), fg_color="#474D50",
                                                     text_color="black")
        qualification_title.place(x=180, y=420)

        employee_name_entry = customtkinter.CTkEntry(employee_frame, font=("Centaur", 20), fg_color="#5C666B",
                                                     width=180, border_color="#191B1C", text_color="white")
        employee_name_entry.place(x=330, y=320)

        age_entry = customtkinter.CTkEntry(employee_frame, font=("Centaur", 20), fg_color="#5C666B", width=180,
                                           border_color="#191B1C", text_color="white")
        age_entry.place(x=330, y=370)

        qualification_entry = customtkinter.CTkEntry(employee_frame, font=("Centaur", 20), fg_color="#5C666B",
                                                     width=180, border_color="#191B1C", text_color="white")
        qualification_entry.place(x=330, y=420)

        # add employee right
        gender_title = customtkinter.CTkLabel(employee_frame, text="Gender ", font=("Centaur", 20, "bold"),
                                              fg_color="#474D50", text_color="black")
        gender_title.place(x=560, y=320)

        contact_title = customtkinter.CTkLabel(employee_frame, text="Contact No ", font=("Centaur", 20, "bold"),
                                               fg_color="#474D50",
                                               text_color="black")
        contact_title.place(x=560, y=370)

        mail_title = customtkinter.CTkLabel(employee_frame, text="Mail Id ", font=("Centaur", 20, "bold"),
                                            fg_color="#474D50", text_color="black")
        mail_title.place(x=560, y=420)

        gender_entry = customtkinter.CTkEntry(employee_frame, font=("Centaur", 20), fg_color="#5C666B", width=180,
                                              border_color="#191B1C", text_color="white")
        gender_entry.place(x=680, y=320)

        contact_entry = customtkinter.CTkEntry(employee_frame, font=("Centaur", 20), fg_color="#5C666B", width=180,
                                               border_color="#191B1C", text_color="white")
        contact_entry.place(x=680, y=370)

        mail_entry = customtkinter.CTkEntry(employee_frame, font=("Centaur", 20), fg_color="#5C666B", width=180,
                                            border_color="#191B1C", text_color="white")
        mail_entry.place(x=680, y=420)

        add_button = customtkinter.CTkButton(employee_frame, text="Add", font=("Centaur", 17),
                                             bg_color="#474D50", width=100, corner_radius=30, fg_color="#191B1C",
                                             command=add_employee)
        add_button.place(x=500, y=500)

# employee main Page
    def employee_page():

        global employee_frame

        # employee main page
        employee_frame = customtkinter.CTkFrame(main_frame, width=1050, height=700, fg_color="#5C666B")
        employee_frame.place(x=0, y=0)

        employee_lable = customtkinter.CTkLabel(employee_frame, text="Employee Info", font=("Berlin Sans FB Demi", 25),
                                                fg_color="#5C666B", text_color="black")
        employee_lable.place(x=450, y=40)

        employee_search_entry = customtkinter.CTkEntry(employee_frame, font=("Centaur", 20), fg_color="#5C666B",
                                                       width=200,border_color="#191B1C", text_color="black")
        employee_search_entry.place(x=100, y=140)

        search_button = customtkinter.CTkButton(employee_frame, text="Search", font=("Centaur", 13), bg_color="#5C666B",
                                                width=50, height=10,corner_radius=60, fg_color="#191B1C")
        search_button.place(x=325, y=145)

        employee_detail_btn = customtkinter.CTkButton(employee_frame, text="Employee Details", font=("Centaur", 17),
                                                      bg_color="#5C666B", width=200,
                                                      corner_radius=30, fg_color="#191B1C",command=stock_details_emp)
        employee_detail_btn.place(x=750, y=140)

        add_emp_button = customtkinter.CTkButton(employee_frame, text="Add Employee", font=("Centaur", 17),
                                                 bg_color="#5C666B", width=100,corner_radius=30, fg_color="#191B1C", command=add_emp)
        add_emp_button.place(x=500, y=600)

        lb12 = customtkinter.CTkLabel(employee_frame, text="Welcome to Employee Page", font=("Magneto", 40),
                                      fg_color="#5C666B", text_color="black")
        lb12.place(x=300, y=340)

#customer delete option
    def delete_customer(event):

        selected_item = tree.selection()

        values = tree.item(selected_item, "values")
        Customer = values[0]

        res = messagebox.askyesno("From App", "Are you sure you want to delete ?")
        if res:
            cursor.execute('delete from customer_details where Customer=?', [Customer])
            connection.commit()

            customer_page()

#customer main page
    def customer_page():

        customer_frame = customtkinter.CTkFrame(main_frame, width=1050, height=700, fg_color="#5C666B",)
        customer_frame.place(x=0, y=0)

        customer_lable = customtkinter.CTkLabel(customer_frame, text="Customer Details",
                                                font=("Berlin Sans FB Demi", 25), fg_color="#5C666B",text_color="black")
        customer_lable.place(x=450, y=40)

        frame = customtkinter.CTkFrame(customer_frame, width=800, height=500, fg_color="#474D50", bg_color="#5C666B",
                                       corner_radius=20)
        frame.place(x=130, y=100)

        data = cursor.execute('select * from customer_details')
        d = data.fetchall()

        style = ttk.Style(w)
        style.theme_use("default")
        style.configure("Treeview", fieldbackground="#474D50", background="#474D50", foreground="white", rowheight=35,
                        font=("Centaur", 17, "bold"), borderwidth=7, relief="raised")
        style.configure("Treeview.Heading", fieldbackground="#5C666B", background="black", foreground="white",
                        font=("Centaur", 20, "bold"))
        style.map("Treeview", background=[("selected", "#1F663A")])
        global tree

        tree = Treeview(frame, columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'), show='headings')
        tree.heading('col1', text='Name')
        tree.heading('col2', text='Contact')
        tree.heading('col3', text='Mail')
        tree.heading('col4', text='Product')
        tree.heading('col5', text='Cost')
        tree.heading('col6', text='Quantity')

        tree.place(x=50, y=50, width=1100, height=670)

        for i in d:
            tree.insert("", "end", values=i)

        tree.bind('<Delete>', delete_customer)


#contact main page

    def contact_page():
        contact_frame = customtkinter.CTkFrame(main_frame, width=1050, height=700, fg_color="#5C666B")
        contact_frame.place(x=0, y=0)

        lb5 = customtkinter.CTkLabel(contact_frame, text="Contact Info", font=("Berlin Sans FB Demi", 25),
                                     fg_color="#5C666B", text_color="black")
        lb5.place(x=500, y=80)

        lb5 = customtkinter.CTkLabel(contact_frame, text="Mobile No : 0123456789", font=("Centaur", 20, "bold"),
                                     fg_color="#5C666B", text_color="black")
        lb5.place(x=250, y=200)

        lb5 = customtkinter.CTkLabel(contact_frame, text="Mail Id : akshop@gmail.com", font=("Centaur", 20, "bold"),
                                     fg_color="#5C666B",text_color="black")
        lb5.place(x=250, y=250)

        lb5 = customtkinter.CTkLabel(contact_frame, text="Address : AK Shop, Padanthalumoodu",
                                     font=("Centaur", 20, "bold"), fg_color="#5C666B",text_color="black")
        lb5.place(x=250, y=300)

#about main page
    def about_page():
        about_frame = customtkinter.CTkFrame(main_frame, width=1050, height=700, fg_color="#5C666B")
        about_frame.place(x=0, y=0)

        lb6 = customtkinter.CTkLabel(about_frame, text="About", font=("Berlin Sans FB Demi", 25),
                                     fg_color="#5C666B", text_color="black")
        lb6.place(x=500, y=80)

        lb6 = customtkinter.CTkLabel(about_frame, text="Updating.......", font=("Centaur", 20, "bold"),
                                     fg_color="#5C666B", text_color="black")
        lb6.place(x=480, y=300)

#indicate option manager
    def hide_indicators():
        product_indicate.configure(bg_color="#191B1C")
        customer_indicate.configure(bg_color="#191B1C")
        employee_indicate.configure(bg_color="#191B1C")
        contact_indicate.configure(bg_color="#191B1C")
        about_indicate.configure(bg_color="#191B1C")
        exit_indicate.configure(bg_color="#191B1C")

    def delete_page():
        for frame in main_frame.winfo_children():
            frame.destroy()

    def indicate(lb, page):
        hide_indicators()
        lb.configure(bg_color="white")
        delete_page()
        page()

#manager main page
    frame = customtkinter.CTkFrame(w, fg_color="#191B1C")
    frame.pack(side=LEFT)
    frame.pack_propagate(False)
    frame.configure(width=250, height=800)

    main_frame = customtkinter.CTkFrame(w, fg_color="#5C666B")
    main_frame.place(x=250, y=0)
    main_frame.configure(height=800, width=1100)

    main_page_title=customtkinter.CTkLabel(main_frame, text="Welcome to AK Shop", font=("Magneto", 40),text_color="black")
    main_page_title.place(x=300,y=300)

    title = customtkinter.CTkLabel(frame, text="AK", font=("Magneto", 20))
    title.place(x=40, y=30)

    product_btn = customtkinter.CTkButton(frame, text="Product", width=190, font=("times", 15), fg_color="#5C666B",
                                          command=lambda: indicate(product_indicate, product_page))
    product_btn.place(x=30, y=80)

    product_indicate = customtkinter.CTkLabel(frame, text="")
    product_indicate.place(x=3, y=80)

    employee_btn = customtkinter.CTkButton(frame, text="Employee", width=190, font=("times", 15), fg_color="#5C666B",
                                           command=lambda: indicate(employee_indicate, employee_page))
    employee_btn.place(x=30, y=120)

    employee_indicate = customtkinter.CTkLabel(frame, text="")
    employee_indicate.place(x=3, y=120)

    customer_btn = customtkinter.CTkButton(frame, text="Customer", width=190, font=("times", 15), fg_color="#5C666B",
                                           command=lambda: indicate(customer_indicate, customer_page))
    customer_btn.place(x=30, y=160)

    customer_indicate = customtkinter.CTkLabel(frame, text="")
    customer_indicate.place(x=3, y=160)

    contact_btn = customtkinter.CTkButton(frame, text="Contact", width=190, font=("times", 15), fg_color="#5C666B",
                                          command=lambda: indicate(contact_indicate, contact_page))
    contact_btn.place(x=30, y=200)

    contact_indicate = customtkinter.CTkLabel(frame, text="")
    contact_indicate.place(x=3, y=200)

    about_btn = customtkinter.CTkButton(frame, text="About", width=190, font=("times", 15), fg_color="#5C666B",
                                        command=lambda: indicate(about_indicate, about_page))
    about_btn.place(x=30, y=240)

    about_indicate = customtkinter.CTkLabel(frame, text="")
    about_indicate.place(x=3, y=240)

    exit_btn = customtkinter.CTkButton(frame, text="Exit", width=190, font=("times", 15), fg_color="#5C666B",
                                       command=lambda: indicate(exit_indicate, frame.quit))
    exit_btn.place(x=30, y=580)

    exit_indicate = customtkinter.CTkLabel(frame, text="")
    exit_indicate.place(x=3, y=580)


#EMPLOYEE PAGE

#bill page add to card auto fill option
def auto_fill(event):

    name=val1.get()
    data=cursor.execute('select quantity,cost from product_details where name=?',[name])
    d=data.fetchone()
    val2.set(1)
    val3.set(d[1])

#bill page cost and quantity mul
def price(event):

     value1=val2.get()
     value2=val3.get()

     val3.set(value1*value2)

#billpage insert product details in bill tree
def print_bil():
    tree.insert("","end",values=(val1.get(),val2.get(),val3.get()))
    column_values=[]
    for i in tree.get_children():
        value=int(tree.item(i,"values")[2])

        if value:
            column_values.append(value)
    global total

    total=sum(column_values)
    bill_total.configure(text=total)

    name = name_entry.get()
    contact = mobile_entry.get()
    mail = mail_entry.get()
    product = product_entry.get()
    cost = cost_entry.get()
    quantity = quantity_entry.get()
    cursor.execute('insert into customer_details values(?,?,?,?,?,?)', [name, contact, mail, product, cost, quantity])
    connection.commit()
    messagebox.showinfo('From Ak App', "items Added Successfully!!")
    #
    # product_entry.delete(0, END)
    # cost_entry.delete(0, END)
    # quantity_entry.delete(0, END)

    bill_name.configure(text=name)
    bill_num.configure(text=contact)
    bill_mail.configure(text=mail)

    update_date(bill_date)  # Start updating the date label
    update_time(bill_time)  # Start updating the time label

#current date
def update_date(label):
    global current_date
    current_date = datetime.now().strftime("%d-%m-%Y")
    label.configure(text=current_date)
    label.after(1000, update_date, label)  # Update every second (1000 milliseconds)

#current time
def update_time(label):
    global current_time
    current_time = datetime.now().strftime("%H:%M:%S")
    label.configure(text=current_time)
    label.after(1000, update_time, label)  # Update every second (1000 milliseconds)

#del row from treeview table
def delete_selected_row():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

#delete all data in print bill
def clear_label_data():
    bill_name.configure(text="")
    bill_num.configure(text="")
    bill_mail.configure(text="")
    bill_date.configure(text="")
    bill_time.configure(text="")
    bill_total.configure(text="")
    tree.delete(*tree.get_children())


#employee main page
def employee():

    win.withdraw()

    global name_entry,mobile_entry,mail_entry,product_entry,cost_entry,quantity_entry

    window = customtkinter.CTkToplevel()
    window.title("Ak App")
    window.geometry('1920x1080+0+0')
    window.config(background="#5C666B")


    title = customtkinter.CTkLabel(window, text="Bill System", font=("Berlin Sans FB Demi", 35), fg_color="#5C666B",
                                   text_color="#191B1C")
    title.place(x=570, y=10)

    # Top frame customer details in bill page
    frame = customtkinter.CTkFrame(master=window, width=1260, height=100, corner_radius=20, fg_color="#5C666B",
                                   bg_color="#5C666B", border_width=3, border_color="black")
    frame.place(x=10, y=60)

    customer_title = customtkinter.CTkLabel(window, text="Customer Details", font=("Berlin Sans FB Demi", 18),
                                            fg_color="#5C666B", text_color="black")
    customer_title.place(x=30, y=70)

    name_title = customtkinter.CTkLabel(window, text="Customer Name :", font=("Centaur", 20, "bold"),
                                        fg_color="#5C666B", text_color="black")
    name_title.place(x=60, y=110)

    mobile_title = customtkinter.CTkLabel(window, text="Mobile Number :", font=("Centaur", 20, "bold"),
                                          fg_color="#5C666B", text_color="black")
    mobile_title.place(x=480, y=110)

    email_title = customtkinter.CTkLabel(window, text="E-mail Id :", font=("Centaur", 20, "bold"), fg_color="#5C666B",
                                         text_color="black")
    email_title.place(x=900, y=110)

    name_entry = customtkinter.CTkEntry(window, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                        border_color="#191B1C", text_color="white")
    name_entry.place(x=210, y=110)

    mobile_entry = customtkinter.CTkEntry(window, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                          border_color="#191B1C", text_color="white")
    mobile_entry.place(x=630, y=110)

    mail_entry = customtkinter.CTkEntry(window, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                        border_color="#191B1C", text_color="white")
    mail_entry.place(x=1000, y=110)

    # LEFT FRAME product details in bill page


    left_frame = customtkinter.CTkFrame(master=window, width=460, height=500, corner_radius=20, fg_color="#5C666B",
                                        bg_color="#5C666B", border_width=3, border_color="black")
    left_frame.place(x=10, y=180)

    product_title = customtkinter.CTkLabel(window, text="Product Details", font=("Berlin Sans FB Demi", 18),
                                           fg_color="#5C666B", text_color="black")
    product_title.place(x=30, y=200)

    product_name_title = customtkinter.CTkLabel(window, text="Product Name :", font=("Centaur", 20, "bold"),
                                                fg_color="#5C666B", text_color="black")
    product_name_title.place(x=60, y=250)

    quantity_title = customtkinter.CTkLabel(window, text="Quantity :", font=("Centaur", 20, "bold"), fg_color="#5C666B",
                                            text_color="black")
    quantity_title.place(x=60, y=300)

    cost_title = customtkinter.CTkLabel(window, text="Cost :", font=("Centaur", 20, "bold"), fg_color="#5C666B",
                                        text_color="black")
    cost_title.place(x=60, y=350)



#bill page product details insert


    data=cursor.execute("select name from product_details")
    a=list()
    for i in data:
        a.extend(i)
        a.sort(reverse=False)


    global val1,val2,val3
    val1=StringVar()
    val2=IntVar()
    val3=IntVar()


    product_entry = AutocompleteCombobox(window,font=("Centaur", 20), width=25,height=10,
                                          completevalues=a,textvariable=val1)
    product_entry.configure(background="lightgray")
    product_entry.place(x=300, y=380)
    product_entry.focus()
    product_entry.current(1)
    product_entry.bind('<Return>',auto_fill)


    quantity_entry = customtkinter.CTkEntry(window,textvariable=val2, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                            border_color="#191B1C", text_color="white")
    quantity_entry.place(x=200, y=300)

    quantity_entry.bind('<Return>',price)

    cost_entry = customtkinter.CTkEntry(window,textvariable=val3, font=("Centaur", 20), fg_color="#5C666B", width=230,
                                        border_color="#191B1C", text_color="white")
    cost_entry.place(x=200, y=350)

#button options in bill page

    add_button = customtkinter.CTkButton(window, text="Add item", font=("Centaur", 17), bg_color="#5C666B", width=100,
                                         corner_radius=30, fg_color="#191B1C",command=print_bil)
    add_button.place(x=100, y=440)

    remove_button = customtkinter.CTkButton(window, text="Delete", font=("Centaur", 17), bg_color="#5C666B", width=100,
                                            corner_radius=30, fg_color="#191B1C",command=delete_selected_row)
    remove_button.place(x=280, y=440)

    bill_title = customtkinter.CTkLabel(window, text="Bill Options", font=("Berlin Sans FB Demi", 18),
                                        fg_color="#5C666B", text_color="black")
    bill_title.place(x=30, y=500)

    send_button = customtkinter.CTkButton(window, text="Send Email", font=("Centaur", 17), bg_color="#5C666B",
                                          width=100, corner_radius=30, fg_color="#191B1C",command=generate_bill_pdf)
    send_button.place(x=100, y=550)

    clear_button = customtkinter.CTkButton(window, text="Clear", font=("Centaur", 17), bg_color="#5C666B", width=100,
                                           corner_radius=30, fg_color="#191B1C",command=clear_label_data)
    clear_button.place(x=280, y=550)

    exit_button = customtkinter.CTkButton(window, text="Exit", font=("Centaur", 17), bg_color="#5C666B", width=100,
                                          corner_radius=30, fg_color="#191B1C", command=window.quit)
    exit_button.place(x=190, y=610)

    # right FRAME billframe label


    right_frame = customtkinter.CTkFrame(master=window, width=783, height=500, corner_radius=20, fg_color="#5C666B",
                                         bg_color="#5C666B", border_width=3, border_color="black")
    right_frame.place(x=485, y=180)

    bill_title = customtkinter.CTkLabel(window, text="AK Shop", font=("Copperplate Gothic Bold", 18),
                                        fg_color="#5C666B", text_color="black")
    bill_title.place(x=820, y=200)

    address_title = customtkinter.CTkLabel(window, text="Padanthalumoodu", font=("Copperplate Gothic Bold", 18),
                                           fg_color="#5C666B", text_color="black")
    address_title.place(x=770, y=220)

    no_title = customtkinter.CTkLabel(window, text="Contact No :0123456789", font=("Copperplate Gothic Bold", 18),
                                      fg_color="#5C666B", text_color="black")
    no_title.place(x=740, y=240)

    m_title = customtkinter.CTkLabel(window, text="Mail Id :akshop@gmail.com", font=("Copperplate Gothic Bold", 18),
                                     fg_color="#5C666B", text_color="black")
    m_title.place(x=732, y=260)

    cname_title = customtkinter.CTkLabel(window, text="Customer Name :", font=("Copperplate Gothic Bold", 18),
                                         fg_color="#5C666B", text_color="black")
    cname_title.place(x=540, y=290)

    mob_title = customtkinter.CTkLabel(window, text="Mobile No :", font=("Copperplate Gothic Bold", 18),
                                       fg_color="#5C666B", text_color="black")
    mob_title.place(x=540, y=310)

    ma_title = customtkinter.CTkLabel(window, text="Mail Id :", font=("Copperplate Gothic Bold", 18),
                                      fg_color="#5C666B", text_color="black")
    ma_title.place(x=540, y=330)

    date_title = customtkinter.CTkLabel(window, text="Date :", font=("Copperplate Gothic Bold", 18), fg_color="#5C666B",
                                        text_color="black")
    date_title.place(x=1020, y=290)

    t_title = customtkinter.CTkLabel(window, text="Time :", font=("Copperplate Gothic Bold", 18), fg_color="#5C666B",
                                     text_color="black")
    t_title.place(x=1020, y=310)

    total_title = customtkinter.CTkLabel(window, text="TOTAL :", font=("Copperplate Gothic Bold", 20),
                                         fg_color="#5C666B", text_color="black")
    total_title.place(x=980, y=630)


    global bill_name,bill_num,bill_mail,bill_date,bill_time,bill_total

    bill_name=customtkinter.CTkLabel(window,text="", font=("Copperplate Gothic Bold", 15),
                                         fg_color="#5C666B", text_color="black")
    bill_name.place(x=730,y=290)

    bill_num=customtkinter.CTkLabel(window,text="", font=("Copperplate Gothic Bold", 15),
                                         fg_color="#5C666B", text_color="black")
    bill_num.place(x=670,y=310)

    bill_mail=customtkinter.CTkLabel(window,text="", font=("Copperplate Gothic Bold", 15),
                                         fg_color="#5C666B", text_color="black")
    bill_mail.place(x=640,y=330)

    bill_date=customtkinter.CTkLabel(window,text="", font=("Copperplate Gothic Bold", 15),
                                         fg_color="#5C666B", text_color="black")
    bill_date.place(x=1080,y=290)

    bill_time=customtkinter.CTkLabel(window,text="", font=("Copperplate Gothic Bold", 15),
                                         fg_color="#5C666B", text_color="black")
    bill_time.place(x=1080,y=310)


    bill_total=customtkinter.CTkLabel(window,text="", font=("Copperplate Gothic Bold", 20),
                                         fg_color="#5C666B", text_color="black")
    bill_total.place(x=1090,y=630)


#bill frame treeview option
    style = ttk.Style(window)
    style.theme_use("default")
    style.configure("Treeview", fieldbackground="#474D50", background="#474D50", foreground="white", rowheight=35,
                    font=("Centaur", 17, "bold"), borderwidth=7, relief="raised")
    style.configure("Treeview.Heading", fieldbackground="#5C666B", background="black", foreground="white",
                    font=("Centaur", 18, "bold"))
    style.map("Treeview", background=[("selected", "#1F663A")])

    global tree

    tree = Treeview(window, columns=("column1", "column2", "column3"), show="headings")
    tree.heading("column1", text="Product Name")
    tree.heading("column2", text="Quantity")
    tree.heading("column3", text="Price")
    tree.place(x=820, y=560, width=990, height=370)



#generate email button
def generate_bill_pdf():

    to= mail_entry.get()
    user="aksharass128@gmail.com"
    password="zsma rypl aaoh gxkl"


    try:
        filename = "bill.pdf"
        c = canvas.Canvas(filename, pagesize=letter)

        items = tree.get_children()
        y_position = 480  # Starting y-position for drawing items

        #customer selected product details in pdf
        for item in items:
            values = tree.item(item, "values")
            product, quantity, price = values

            c.setFont("Helvetica",14)

            # Draw product, quantity, and price
            c.drawString(100, y_position, product)
            c.drawString(280, y_position, quantity)
            c.drawString(470, y_position, price)

            y_position -= 30  # Move to the next line


        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 500, "Product")
        c.drawString(280, 500, "Quantity")
        c.drawString(470, 500, "Price")
        c.drawString(80, 540, "___________________________________________________")



        c.drawString(320, 150, f"TOTAL AMOUNT :    {total}")
        c.drawString(80, 180, "___________________________________________________")

        #current date and time
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M:%S")


        c.setFont("Helvetica", 12)
        c.drawString(100, 640, f"Customer Name: {name_entry.get()}")
        c.drawString(100, 600, f"Contact No: {mobile_entry.get()}")
        c.drawString(100, 560, f"Mail id: {mail_entry.get()}")
        c.drawString(400, 640, f"Date: {current_date}")
        c.drawString(400, 600, f"Time: {current_time}")

        # Draw the bill pdf content
        c.setFont("Helvetica-Bold", 16)
        c.drawString(280, 750, "AK Shop")
        c.drawString(240, 730, "Padanthalumoodu")
        c.drawString(220, 710, "Contact no:1234567890")
        c.drawString(205, 690, "Mail id:akshop@gmail.com")
        c.drawString(80, 670, "___________________________________________________")


        # Save the PDF
        c.save()

        name_entry.delete(0, END)
        mobile_entry.delete(0, END)
        mail_entry.delete(0, END)

        # mail content
        msg = EmailMessage()
        msg.set_content(
            f"Greetings from Ak shop  \n\nDear {name_entry.get()},\n\n        Just a quick note to say thank you for choosing us.\n        We appreciate your support and look forward to serving you again soon!   \n\nBest regards,\n Ak Shop")

        msg['subject'] = "Thank You for Your Recent Purchase!"
        msg["from"] = user
        msg["to"] = to

        #mail -send pdf
        with open(filename, 'rb') as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

        messagebox.showinfo("Success", f"Email sent successfully! as {filename}")


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


#  main page frame

frame =customtkinter.CTkFrame(master=root, width=400, height=400,corner_radius=40,fg_color="#191B1C",bg_color="black")
frame.place(x=200,y=100)


title=customtkinter.CTkLabel(root,text="AK",font=("Magneto",35),fg_color="#191B1C",)
title.place(x=365,y=150)

sign_title=customtkinter.CTkLabel(root,text="Sign In",font=("Centaur",30),fg_color="#191B1C",)
sign_title.place(x=360,y=220)

user_label=customtkinter.CTkLabel(root,text="Username",font=("Centaur",20),fg_color="#191B1C",)
user_label.place(x=250,y=280)

pass_label=customtkinter.CTkLabel(root,text="Password",font=("Centaur",20),fg_color="#191B1C",)
pass_label.place(x=250,y=340)

name_entry=customtkinter.CTkEntry(root,font=("Centaur",10),fg_color="#191B1C",width=200)
name_entry.place(x=350,y=280)

pass_entry=customtkinter.CTkEntry(root,font=("Centaur",10),fg_color="#191B1C",width=200)
pass_entry.place(x=350,y=340)


b=customtkinter.CTkButton(root,text="Login",font=("Centaur",17),bg_color="#191B1C",width=100,corner_radius=30,command=home)
b.place(x=350,y=410)


root.mainloop()