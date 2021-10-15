from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Ariel"
current_card = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dic = original_data.to_dict(orient="record")
else:
    data_dic = data.to_dict(orient="records")
print(data_dic)

# ======================================Flip card================================================= #

def flip_card():
    global current_card
    canvas.itemconfig(image_on_canvas, image=card_back_image)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    # print(eng_word)
    # title_label.config(bg=BACKGROUND_COLOR, fg="white")


# ======================================IMPORT CSV FILE================================================= #

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dic)
    french_word = current_card["French"]
    eng_word = current_card["English"]
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french_word, fill="black")
    canvas.itemconfig(image_on_canvas, image=card_front_image)
    flip_timer = window.after(3000, flip_card)

# ======================================REMOVE FROM LIST================================================= #

def remove():
    global data_dic
    data_dic.remove(current_card)
    print(len(data_dic))
    data_file = pandas.DataFrame(data_dic)
    data_file.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ======================================UI SETUP================================================= #
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR,)


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

image_on_canvas = canvas.create_image(400, 263, image=card_front_image)
# canvas.itemconfig(image_on_canvas, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

title_text = canvas.create_text(400, 150, text="title", font="FONT 40 italic")
word_text = canvas.create_text(400, 263, text="French", font="FONT 60 bold")


# Buttons
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=remove)
right_button.grid(column=1, row=1)





flip_timer = window.after(3000, flip_card)
next_card()


window.mainloop()