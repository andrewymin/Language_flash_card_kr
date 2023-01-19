from tkinter import *
import pandas
import random
import json


# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
LANGUAGE_TO_LEARN = "Korean"
FILE_LANGUAGE_NAME = "korean"
current_card = {}
to_learn = {}
try:
    data_df = pandas.read_csv(f"data/{FILE_LANGUAGE_NAME}_words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv(f"data/{FILE_LANGUAGE_NAME}_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data_df.to_dict(orient="records")
# print(data_dict)

# ---------------------------- WORD GENERATOR ------------------------------- #


def next_card():
    global flip_timer, current_card
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_image, image=card_front_image)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_language, text=LANGUAGE_TO_LEARN, fill="black")
    canvas.itemconfig(flash_word, text=f"{current_card[LANGUAGE_TO_LEARN]}", fill="black")
    flip_timer = window.after(3000, flip_card)


# ---------------------------- FLIP ------------------------------- #


def flip_card():
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(title_language, text="English", fill="white")
    canvas.itemconfig(flash_word, text=f"{current_card['English']}", fill="white")


# ---------------------------- SAVING ------------------------------- #


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv(f"data/{FILE_LANGUAGE_NAME}_words_to_learn.csv", index=False)

    next_card()


# ---------------------------- UI ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, next_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_image)
title_language = canvas.create_text(400, 150, text="Language", font=(FONT_NAME, 40, "italic"))
flash_word = canvas.create_text(400, 263, text="Word", font=(FONT_NAME, 50, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
unknown_img = PhotoImage(file="images/wrong.png")
unknown = Button(image=unknown_img, highlightthickness=0, command=next_card)
unknown.grid(column=0, row=1)

learned_img = PhotoImage(file="images/right.png")
learned = Button(image=learned_img, highlightthickness=0, command=is_known)
learned.grid(column=1, row=1)

next_card()

window.mainloop()
