from tkinter import *
from tkinter import messagebox
import random
import string
from typing import NewType
import pyperclip
import json 

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(8))
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    new_data = {
        website : {
            "email" : email,
            "password" : password 
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="You left some info empty! \nPlease fill the empty fields.")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w" ) as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
        
            with open("data.json", "w") as file:
                json.dump(data,file,indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    with open("data.json","r") as file:
        file = json.load(file)
        website = website_entry.get()
        try:
            messagebox.showinfo(title=f"{website}", message=f"email : {file[website]['email']}\n password: {file[website]['password']}")
        except KeyError:
            messagebox.showinfo(title="Error", message=f"There is no credentials for {website}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="@Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=17)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "email@domain.com")
password_entry = Entry(width=17)
password_entry.grid(row=3, column=1)
# Buttons
generate_password_button = Button(text="GeneratePassword", command=generate_password)
generate_password_button.grid(row=3, column=2,columnspan=1)
add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", command=search)
search_button.grid(row=1,column=2)
window.mainloop()
