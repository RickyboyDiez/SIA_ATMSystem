import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="atm"
)

def newpin(amount):
    global pinNew
    pinNew = amount

#function to display another frame
def show_frame(frame):
    frame.tkraise()

global accPin
def login():
    global accountNumber
    global accountbal
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="atm"
    )
    cursor = db.cursor()

    login_pin = loginFrame_inp.get()
    query = 'SELECT `acc_name`, `balance`, `pin`, `acc_num` from `person` WHERE `pin` = %s'
    val = (login_pin,)
    cursor.execute(query, val)
    user = cursor.fetchone()
    acc_name = user[0] if user else "N/A"
    accBalance = user[1] if user else 0
    accountbal = accBalance
    accPin = user[2] if user else 0
    accountNumber = user[3] if user else 0
    if user is not None:
        show_frame(mainFrame)
        balanceFrame_name.config(text=acc_name)
        balanceFrame_bal.config(text=accBalance)
        newpin(accPin)
    else:
        loginFrame_inp.delete(0, tk.END)
        loginFrame_accname.config(text="Invalid PIN", fg="white", bg="#023048", font=("Arial", 14, "bold"))
        loginFrame_accname.after(2000, revert_text)

def balance():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="atm"
    )
    cursor = db.cursor()

    pin = pinNew
    query = 'SELECT acc_name, balance from person WHERE pin = %s'
    cursor.execute(query, (pin,))
    ball = cursor.fetchone()
    acc_name = ball[0] if ball else "N/A"
    accBalance = ball[1] if ball else 0
    balanceFrame_name.config(text=acc_name)
    balanceFrame_bal.config(text=accBalance)
    show_frame(balanceFrame)

def deposit(amount=None):
    # Retrieve the account number from the input field
    # pin = pinNew

    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="atm"
    )
    cursor = db.cursor()

    # Check if the account exists
    query = "SELECT balance FROM person WHERE pin = %s"
    cursor.execute(query, (pinNew,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        if amount is None:
            amount = float(depositFrame_inp.get())  # Get the value from withdrawFrame_inp as a float

        # Update the account balance
        balance = balance + amount
        update_query = "UPDATE person SET balance = %s WHERE pin = %s"
        cursor.execute(update_query, (balance, pinNew))
        db.commit()

        # Display success message
        depositFrame_message.config(text="Withdrawal successful!")
        depositFrame.after(2000, lambda: show_frame(transactionFrame))
        withdrawFrame_message.after(2000, clear_message)

    # Close the database connection
    cursor.close()
    db.close()


def withdraw(amount=None):
    # Retrieve the account number from the input field
    pin = pinNew

    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="atm"
    )
    cursor = db.cursor()

    # Check if the account exists
    query = "SELECT balance FROM person WHERE pin = %s"
    cursor.execute(query, (pin,))
    result = cursor.fetchone()

    if result:
        balance = result[0]

        if amount is None:
            amount = float(withdrawFrame_inp.get())  # Get the value from withdrawFrame_inp as a float

        if balance >= amount:
            # Update the account balance
            balance = balance - amount
            update_query = "UPDATE person SET balance = %s WHERE pin = %s"
            cursor.execute(update_query, (balance, pin))
            db.commit()

            # Display success message
            withdrawFrame_message.config(text="Withdrawal successful!")
            withdrawFrame.after(2000, lambda: show_frame(transactionFrame))
            withdrawFrame_message.after(2000, clear_message)
        else:
            # Insufficient balance
            withdrawFrame_message.config(text="Insufficient balance!")
    else:
        # Account not found
        withdrawFrame_message.config(text="Account not found!")

    # Close the database connection
    cursor.close()
    db.close()

def revert_text():
    loginFrame_accname.config(text="Please enter your PIN")

def handle_deposit(event):
    deposit()

def handle_withdraw(event):
    withdraw()

def withdraw_frame(event):
    if withdrawFrame_inp.get() == "":
        show_frame(mainFrame)

def deposit_frame(event):
    if depositFrame_inp.get() == "":
        show_frame(mainFrame)

def transfer_frame(event):
    if transferFrame_inp.get() == "":
        show_frame(mainFrame)

def transfer1_frame(event):
    if transferFrame_inp1.get() == "":
        show_frame(mainFrame)

def transfer2_frame(event):
    if transferFrame_inp2.get() == "":
        show_frame(mainFrame)

def clear_message():
    withdrawFrame_message.config(text="")
    depositFrame_message.config(text="")

def transfer():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="atm"
    )
    cursor = db.cursor()
    transfer_name = transferFrame_inp.get()
    transfer_num = transferFrame_inp1.get()
    transfer_amount = float(transferFrame_inp2.get())
    main_num = accountNumber
    main_balance = accountbal
    balance = transfer_amount
    query = "SELECT acc_num, acc_name, balance from person where acc_num = %s and acc_name = %s"
    cursor.execute(query, (transfer_num, transfer_name,))
    result = cursor.fetchone()
    if result:
        numTransfer = result[0]
        nameTransfer = result[1]
        bal = result[2]
        if main_num != numTransfer:
            newBalance = balance + bal
            query = "UPDATE person SET balance = %s WHERE acc_num = %s AND acc_name = %s"
            cursor.execute(query, (newBalance, transfer_num, transfer_name))
            print('test')
            db.commit()
            query = "SELECT balance from person WHERE acc_num = %s"
            cursor.execute(query, (main_num,))
            result2 = cursor.fetchone()
            print('test1')
            if result2:
                print('test2')
                dedBalance = result2[0]
                dedNewBalance = dedBalance - transfer_amount
                query = "UPDATE person SET balance = %s WHERE acc_num = %s"
                cursor.execute(query, (dedNewBalance, main_num))
                print(dedNewBalance)
                db.commit()
    show_frame(transactionFrame)

def transcomp():
    show_frame(transcompFrame)
    transcompFrame.after(2000, lambda: window.destroy())

window = tk.Tk()
window.title("Simple ATM")
window.geometry('1115x576')
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

transcompFrame = tk.Frame(window)
transactionFrame = tk.Frame(window)
depositFrame = tk.Frame(window)
withdrawFrame = tk.Frame(window)
balanceFrame = tk.Frame(window)
transferFrame = tk.Frame(window)
mainFrame = tk.Frame(window)
loginFrame = tk.Frame(window)

# Load the image file using PIL
image = Image.open("logo.png")

# Convert the image to support transparency
image = image.convert("RGBA")

# Create a Tkinter-compatible image
logo_image = ImageTk.PhotoImage(image)
# Create a style object
style = ttk.Style()

# Configure the style with desired font size
style.configure("TButton", font=("Arial", 20))

for frame in (transcompFrame, transactionFrame, loginFrame, mainFrame, depositFrame, withdrawFrame, balanceFrame, transferFrame):
    frame.grid(row=0, column=0, sticky='nsew')

# loginFrame
loginFrame.configure(background="#023048")
# logo
loginFrame_logo = tk.Label(loginFrame, image=logo_image, borderwidth=0, highlightthickness=0)
loginFrame_logo.grid(row=0, column=0, columnspan=2, sticky="n")
loginFrame.grid_rowconfigure(0, weight=1)
loginFrame.grid_columnconfigure(0, weight=1)

loginFrame_inp = tk.Entry(loginFrame, justify='center', show='*', width=50)
loginFrame_inp.grid(row=1, column=0, columnspan=6, sticky="n", ipady=10)
loginFrame_inp.grid_rowconfigure(0, weight=1)
loginFrame_inp.grid_columnconfigure(0, weight=1)

loginFrame_accname = tk.Label(loginFrame, text="Please enter your PIN", fg="white", bg="#023048", font=("Arial", 14, "bold"))
loginFrame_accname.grid(row=2, column=0, columnspan=6, sticky="n")
loginFrame_accname.grid_rowconfigure(0, weight=1)
loginFrame_accname.grid_columnconfigure(0, weight=1)

loginFrame_button = ttk.Button(loginFrame, text="Login", width=15, command=lambda: login())
loginFrame_button.grid(row=3, column=0, columnspan=6, sticky="n", pady=100)
loginFrame_button.grid_rowconfigure(0, weight=1)
loginFrame_button.grid_columnconfigure(0, weight=1)

# mainFrame
mainFrame.configure(background="#023048")
# logo
mainFrame_logo = tk.Label(mainFrame, image=logo_image, borderwidth=0, highlightthickness=0)
mainFrame_logo.grid(row=0, column=0, columnspan=2, sticky="n")
mainFrame.grid_rowconfigure(0, weight=1)
mainFrame.grid_columnconfigure(0, weight=1)

mainFrame_b1 = ttk.Button(mainFrame, text="WITHDRAW", style="TButton", width=15,
                          command=lambda: show_frame(withdrawFrame))
mainFrame_b1.grid(row=1, column=0, sticky="nw", ipadx=120, ipady=20, pady=1)
mainFrame_b2 = ttk.Button(mainFrame, text="BALANCE", style="TButton", width=15,
                          command=lambda: balance())
mainFrame_b2.grid(row=1, column=1, sticky="e", ipadx=120, ipady=20, pady=1)
mainFrame_b3 = ttk.Button(mainFrame, text="DEPOSIT", style="TButton", width=15,
                          command=lambda: show_frame(depositFrame))
mainFrame_b3.grid(row=2, column=0, sticky="nw", ipadx=120, ipady=20, pady=80)
mainFrame_b4 = ttk.Button(mainFrame, text="TRANSFER", style="TButton", width=15,
                          command=lambda: show_frame(transferFrame))
mainFrame_b4.grid(row=2, column=1, sticky="e", ipadx=120, ipady=20, pady=80)

# withdrawFrame
withdrawFrame.configure(background="#023048")
# logo
withdrawFrame_logo = tk.Label(withdrawFrame, image=logo_image, borderwidth=0, highlightthickness=0)
withdrawFrame_logo.grid(row=0, column=0, columnspan=5, sticky="nw")
withdrawFrame.grid_rowconfigure(0, weight=1)
withdrawFrame.grid_columnconfigure(0, weight=1)

withdrawFrame_ins = tk.Label(withdrawFrame,
                             text="Select an amount OR enter \n another amount and press ENTER to withdraw. \n Press BACKSPACE to return to the homepage.", fg="white",
                             bg="#023048", font=("Arial", 20, "bold"))
withdrawFrame_ins.grid(row=1, column=0, columnspan=6, sticky="n")
withdrawFrame_ins.grid_rowconfigure(0, weight=1)
withdrawFrame_ins.grid_columnconfigure(0, weight=1)

withdrawFrame_inp = tk.Entry(withdrawFrame, justify='center', font=("Arial", 15))
withdrawFrame_inp.grid(row=2, column=0, columnspan=6, sticky="n", pady=20, ipady=20, ipadx=100)
withdrawFrame_inp.grid_rowconfigure(0, weight=1)
withdrawFrame_inp.grid_columnconfigure(0, weight=1)
withdrawFrame_inp.bind('<Return>', handle_withdraw)
withdrawFrame_inp.bind('<BackSpace>', withdraw_frame)

withdrawFrame_b1 = tk.Button(withdrawFrame, text="₱1,000.00", width=15, command=lambda: withdraw(1000))
withdrawFrame_b1.grid(row=4, column=0, sticky="nw", ipadx=120, ipady=20, pady=1)
withdrawFrame_b2 = tk.Button(withdrawFrame, text="₱5,000.00", width=15, command=lambda: withdraw(5000))
withdrawFrame_b2.grid(row=5, column=0, sticky="nw", ipadx=120, ipady=20, pady=30)
withdrawFrame_b3 = tk.Button(withdrawFrame, text="₱8,000.00", width=15, command=lambda: withdraw(8000))
withdrawFrame_b3.grid(row=4, column=2, sticky="e", ipadx=120, ipady=20, pady=1)
withdrawFrame_b4 = tk.Button(withdrawFrame, text="₱10,000.00", width=15, command=lambda: withdraw(10000))
withdrawFrame_b4.grid(row=5, column=2, sticky="e", ipadx=120, ipady=20, pady=30)

withdrawFrame_message = tk.Label(withdrawFrame, text="", fg="white", bg="#023048", font=("Arial", 15))
withdrawFrame_message.grid(row=6, column=0, columnspan=6, sticky="n")

# depositFrame
depositFrame.configure(background="#023048")
# logo
depositFrame_logo = tk.Label(depositFrame, image=logo_image, borderwidth=0, highlightthickness=0)
depositFrame_logo.grid(row=0, column=0, columnspan=5, sticky="nw")
depositFrame.grid_rowconfigure(0, weight=1)
depositFrame.grid_columnconfigure(0, weight=1)

depositFrame_ins = tk.Label(depositFrame, text="Select an amount OR enter \n another amount and press ENTER to deposit. \n Press BACKSPACE to return to the homepage.",
                            fg="white", bg="#023048", font=("Arial", 20, "bold"))
depositFrame_ins.grid(row=1, column=0, columnspan=8, sticky="n")
depositFrame_ins.grid_rowconfigure(0, weight=1)
depositFrame_ins.grid_columnconfigure(0, weight=1)

depositFrame_inp = tk.Entry(depositFrame, justify='center', font=("Arial", 15))
depositFrame_inp.grid(row=2, column=0, columnspan=8, sticky="n", pady=20, ipady=20, ipadx=100)
depositFrame_inp.grid_rowconfigure(0, weight=1)
depositFrame_inp.grid_columnconfigure(0, weight=1)
depositFrame_inp.bind('<Return>', handle_deposit)
depositFrame_inp.bind('<BackSpace>', deposit_frame)

depositFrame_b1 = tk.Button(depositFrame, text="₱1,000.00", width=15, command=lambda: deposit(1000))
depositFrame_b1.grid(row=4, column=0, sticky="nw", ipadx=120, ipady=20, pady=1)
depositFrame_b2 = tk.Button(depositFrame, text="₱5,000.00", width=15, command=lambda: deposit(5000))
depositFrame_b2.grid(row=5, column=0, sticky="nw", ipadx=120, ipady=20, pady=30)
depositFrame_b3 = tk.Button(depositFrame, text="₱8,000.00", width=15, command=lambda: deposit(8000))
depositFrame_b3.grid(row=4, column=2, sticky="e", ipadx=120, ipady=20, pady=1)
depositFrame_b4 = tk.Button(depositFrame, text="₱10,000.00", width=15, command=lambda: deposit(10000))
depositFrame_b4.grid(row=5, column=2, sticky="e", ipadx=120, ipady=20, pady=30)

depositFrame_message = tk.Label(depositFrame, text="", fg="white", bg="#023048", font=("Arial", 15))
depositFrame_message.grid(row=6, column=0, columnspan=6, sticky="n")

# balanceFrame
balanceFrame.configure(background="#023048")
# logo
balanceFrame_logo = tk.Label(balanceFrame, image=logo_image, borderwidth=0, highlightthickness=0)
balanceFrame_logo.grid(row=0, column=0, columnspan=5, sticky="nw")
balanceFrame.grid_rowconfigure(0, weight=1)
balanceFrame.grid_columnconfigure(0, weight=1)

balanceFrame_name = tk.Label(balanceFrame, text="", font=('Arial 19 bold underline'), fg="#FBBF49",
                             bg="#023048")
balanceFrame_name.grid(row=1, column=0, columnspan=6, sticky="n")
balanceFrame_name.grid_rowconfigure(0, weight=1)
balanceFrame_name.grid_columnconfigure(0, weight=1)

balanceFrame_accname = tk.Label(balanceFrame, text="Account Name", font=('Arial 11 bold'), fg="white", bg="#023048")
balanceFrame_accname.grid(row=2, column=0, columnspan=2, sticky="n")
balanceFrame_x = tk.Label(balanceFrame, text="", bg="#023048")
balanceFrame_x.grid(row=3, column=0, columnspan=5, sticky="n")
balanceFrame_bal = tk.Label(balanceFrame, text="", font=('Arial 20 bold underline'), fg="#FBBF49",
                            bg="#023048")
balanceFrame_bal.grid(row=4, column=0, columnspan=5, sticky="n")
balanceFrame_desc = tk.Label(balanceFrame, text="is the cash available for withdrawal", font=('Arial 11 bold'),
                             fg="white", bg="#023048")
balanceFrame_desc.grid(row=5, column=0, columnspan=5, sticky="n")
balanceFrame_wbutton = ttk.Button(balanceFrame, text="WITHDRAW", width=15, command=lambda: show_frame(withdrawFrame))
balanceFrame_wbutton.grid(row=6, column=0, sticky="w", ipadx=120, ipady=20, pady=1)
balanceFrame_obutton = ttk.Button(balanceFrame, text="OTHER", width=15, command=lambda: show_frame(mainFrame))
balanceFrame_obutton.grid(row=6, column=1, sticky="e", ipadx=120, ipady=20, pady=80)

# transferFrame
transferFrame.configure(background="#023048")
# logo
transferFrame_logo = tk.Label(transferFrame, image=logo_image, borderwidth=0, highlightthickness=0)
transferFrame_logo.grid(row=0, column=0, sticky="nw")
transferFrame.grid_rowconfigure(0, weight=1)
transferFrame.grid_columnconfigure(0, weight=1)

transferFrame_inp = ttk.Entry(transferFrame, justify='center', width=70)
transferFrame_inp.grid(row=1, column=0, columnspan=6, sticky="n", ipady=10)
transferFrame_inp.grid_rowconfigure(0, weight=1)
transferFrame_inp.grid_columnconfigure(0, weight=1)
transferFrame_inp.bind('<BackSpace>', transfer_frame)

transferFrame_accname = tk.Label(transferFrame, text="Account Name", bg="#023048", fg="white", font=('Arial 11 bold'))
transferFrame_accname.grid(row=2, column=0, columnspan=6, sticky="n")
transferFrame_accname.grid_rowconfigure(0, weight=1)
transferFrame_accname.grid_columnconfigure(0, weight=1)

transferFrame_inp1 = ttk.Entry(transferFrame, justify='center', width=70)
transferFrame_inp1.grid(row=3, column=0, columnspan=6, sticky="n", ipady=10)
transferFrame_inp1.grid_rowconfigure(0, weight=1)
transferFrame_inp1.grid_columnconfigure(0, weight=1)
transferFrame_inp1.bind('<BackSpace>', transfer1_frame)

transferFrame_accnum = tk.Label(transferFrame, text="Account Number", bg="#023048", fg="white", font=('Arial 11 bold'))
transferFrame_accnum.grid(row=4, column=0, columnspan=6, sticky="n")
transferFrame_accnum.grid_rowconfigure(0, weight=1)
transferFrame_accnum.grid_columnconfigure(0, weight=1)

transferFrame_inp2 = ttk.Entry(transferFrame, justify='center', width=70)
transferFrame_inp2.grid(row=5, column=0, columnspan=6, sticky="n", ipady=10)
transferFrame_inp2.grid_rowconfigure(0, weight=1)
transferFrame_inp2.grid_columnconfigure(0, weight=1)
transferFrame_inp2.bind('<BackSpace>', transfer2_frame)

transferFrame_amount = tk.Label(transferFrame, text="Enter Amount to Transfer", bg="#023048", fg="white",
                                font=('Arial 11 bold'))
transferFrame_amount.grid(row=6, column=0, columnspan=6, sticky="n")
transferFrame_amount.grid_rowconfigure(0, weight=1)
transferFrame_amount.grid_columnconfigure(0, weight=1)

transferFrame_obutton = ttk.Button(transferFrame, text="Transfer", width=15, command=lambda: transfer())
transferFrame_obutton.grid(row=7, column=0, columnspan=6, sticky="n", ipadx=120, ipady=20, pady=30)
transferFrame_obutton.grid_rowconfigure(0, weight=1)
transferFrame_obutton.grid_columnconfigure(0, weight=1)



# transactionFrame
transactionFrame.configure(background="#023048")
# logo
transactionFrame_logo = tk.Label(transactionFrame, image=logo_image, borderwidth=0, highlightthickness=0)
transactionFrame_logo.grid(row=0, column=0, sticky="nw")
transactionFrame.grid_rowconfigure(0, weight=1)
transactionFrame.grid_columnconfigure(0, weight=1)

transactionFrame_question = tk.Label(transactionFrame, text="Do you wish to have another transaction?", bg="#023048", fg="white", font=('Arial 20 bold'))
transactionFrame_question.grid(row=1, column=0, columnspan=6, sticky="n")
transactionFrame_question.grid_rowconfigure(0, weight=1)
transactionFrame_question.grid_columnconfigure(0, weight=1)

transactionFrame_ybutton = ttk.Button(transactionFrame, text="YES", width=15, command=lambda: show_frame(mainFrame))
transactionFrame_ybutton.grid(row=2, column=0,sticky="w", ipadx=0, ipady=10, pady=10)

transactionFrame_nbutton = ttk.Button(transactionFrame, text="NO", width=15, command=lambda: transcomp())
transactionFrame_nbutton.grid(row=2, column=1, columnspan=6, sticky="e", ipadx=10, ipady=10, pady=100)


# transcompleteFrame
transcompFrame.configure(background="#023048")
# logo
transcompFrame_logo = tk.Label(transcompFrame, image=logo_image, borderwidth=0, highlightthickness=0)
transcompFrame_logo.grid(row=0, column=0, sticky="nw")
transcompFrame.grid_rowconfigure(0, weight=1)
transcompFrame.grid_columnconfigure(0, weight=1)

transcompFrame_question = tk.Label(transcompFrame, text="TRANSACTION COMPLETE", bg="#023048", fg="white", font=('Arial 20 bold'))
transcompFrame_question.grid(row=1, column=0, columnspan=6, sticky="n", pady=200)
transcompFrame_question.grid_rowconfigure(0, weight=1)
transcompFrame_question.grid_columnconfigure(0, weight=1)

window.mainloop()

