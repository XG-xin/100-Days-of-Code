import random
import smtplib
import pandas
import datetime as dt

now = dt.datetime.now()
month = now.month
day = now.day

my_email = {email}
password = {password}

data = pandas.read_csv("birthdays.csv")
print(data)
print(data.iterrows())
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
print(birthdays_dict)

with open("letter_templates/letter_1.txt") as file:
    letter_1 = file.read()
with open("letter_templates/letter_2.txt") as file:
    letter_2 = file.read()
with open("letter_templates/letter_3.txt") as file:
    letter_3 = file.read()
letter_list = [letter_1, letter_2,letter_3]

if (month, day) in birthdays_dict:
    letter_text = random.choice(letter_list)
    new_letter = letter_text.replace("[NAME]", birthdays_dict[(month, day)]["name"])
    print(new_letter)
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs={receiver_email},
            msg=f"Subject:Happy Birthday\n\n{new_letter}"
        )
