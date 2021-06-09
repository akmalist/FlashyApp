from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# reading CSV using pandas
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ----------------------------NEXT CARD ------------------------------- #

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(old_image, image=card_front)
    flip_timer = window.after(3000, flip_side)
    print(current_card["French"])


def flip_side():
    canvas.itemconfig(old_image, image=card_back)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=current_card["English"])


def known_words():
    to_learn.remove(current_card)
    df = pandas.DataFrame(to_learn)
    df.to_csv("words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, flip_side)
canvas = Canvas()
canvas.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

old_image = canvas.create_image(400, 263, image=card_front)

# ---------------------------- BUTTON ------------------------------- #
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

right_button = Button(image=right_image, highlightthickness=0, command=known_words)

right_button.grid(row=1, column=1, pady=50)

wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0, pady=50)

# Creating text in canvas
card_title = canvas.create_text(400, 150, font=("Ariel", 34, "italic"), text="")
card_word = canvas.create_text(400, 263, font=("Ariel", 48, "bold"), text="")

next_card()

window.mainloop()
