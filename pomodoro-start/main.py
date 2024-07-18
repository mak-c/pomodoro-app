from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global reps
    reps = 0
    window.after_cancel(timer)
    start_button.config(state='active')
    timer_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    check_label.config(text="")


def focus_window(option):
    if option == "on":
        window.deiconify()
        window.focus_force()
        window.attributes('-topmost', 1)
    elif option == "off":
        window.attributes('-topmost', 0)


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    start_button.config(state='disabled')
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="BREAK", fg=RED)
        focus_window("on")
        window.bell()
        reset_timer()
    elif reps % 2 != 0:
        count_down(work_sec)
        timer_label.config(text="WORK", fg=GREEN)
        focus_window("off")
        window.bell()
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="BREAK", fg=PINK)
        focus_window("on")
        window.bell()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    mins, secs = divmod(count, 60)
    canvas.itemconfig(timer_text, text=f"{mins}:{secs:02d}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        mark = ""
        for _ in range(math.floor(reps / 2)):
            mark += "✔"
        check_label.config(text=mark)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", pady=0, padx=0, bg="white", borderwidth=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", pady=0, padx=0, bg="white", borderwidth=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_label = Label(text="", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 30), padx=10, pady=10)
check_label.grid(column=1, row=3)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))
canvas.grid(column=1, row=1)

window.mainloop()
