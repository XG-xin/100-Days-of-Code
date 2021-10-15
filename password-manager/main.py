from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)


def generate_password():
    char_list = [random.choice(letters) for char in range(nr_letters)]
    symbols_list = [random.choice(numbers) for sym in range(nr_symbols)]
    number_list = [random.choice(symbols) for num in range(nr_numbers)]

    password_list = char_list + symbols_list + number_list
    random.shuffle(password_list)

    password = "".join(password_list)
    pw_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = pw_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)

        else:
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, "end")
            pw_entry.delete(0, "end")

# ---------------------------- SEARCH --------------------------------- #


def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Data File Found")
    else:
        if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showwarning(title=website, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showwarning(title="Error", message=f"No details for {website} exists.")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
pw_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pw_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, sticky="ew")
website_entry.focus()
# print(website_entry.get())

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=21)
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew")
email_entry.insert(0, "example@gmail.com")
# print(email_entry.get())

pw_label = Label(text="Password:")
pw_label.grid(column=0, row=3)

pw_entry = Entry(width=21)
pw_entry.grid(column=1, row=3, sticky="ew")

pw_button = Button(text="Generate Password", command=generate_password)
pw_button.grid(column=2, row=3)

add_button = Button(text="Add", command=save)
add_button.config(width=36)
add_button.grid(column=1, row=4)

search_button = Button(text="Search", command=find_password)
search_button.config(width=14)
search_button.grid(column=2, row=1)

window.mainloop()
