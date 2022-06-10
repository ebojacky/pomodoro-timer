import tkinter
import math

# ---------------------------- CONSTANTS ------------------------------- #
YELLOW = "#FCFFC1"
GREEN = "#9BF4D5"
GREENER = "#1DAD9B"
GREENEST = "#346357"
REDISH = "#F55353"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- GLOBAL VARIABLES --------------------------#
timer_text = "00:00"
label_text = "Timer"
check = "✔"
checks = ""
modes = {"work": 0, "rest_short": 1, "rest_long": 2}
mode = None
successful_countdown = 0
my_timer_thread = ""


# ---------------------------- TIMER MECHANISM ------------------------------- #
def timer():
    set_mode()

    global mode, modes
    if mode == modes["work"]:
        countdown(int(WORK_MIN * 60))
    elif mode == modes["rest_short"]:
        countdown(int(SHORT_BREAK_MIN * 60))
    elif mode == modes["rest_long"]:
        countdown(int(LONG_BREAK_MIN * 60))


def set_mode():
    global mode, modes, successful_countdown, label_text, check, checks

    if successful_countdown in [0, 2, 4, 6]:
        mode = modes["work"]
        checks += check
        label_text = "Work"

    elif successful_countdown in [1, 3, 5]:
        mode = modes["rest_short"]
        label_text = "Short Rest"

    elif successful_countdown in [7]:
        mode = modes["rest_long"]
        label_text = "Long Rest"


# ----------------------v------ COUNTDOWN MECHANISM ------------------------------- #

def update_timer_text(seconds):
    m = math.floor(seconds / 60)
    s = seconds % 60

    mm = str(m)
    ss = str(s)

    if len(mm) < 2:
        mm = "0" + mm

    if len(ss) < 2:
        ss = "0" + ss

    global timer_text
    timer_text = f"{mm}:{ss}"


def refresh_screen():
    my_canvas.itemconfig(canvas_timer, text=timer_text)
    global mode, modes
    if mode == modes["work"]:
        my_label.config(text=label_text, fg=REDISH)
    elif mode == modes["rest_short"]:
        my_label.config(text=label_text, fg=GREENER)
        my_check_label.config(text=checks)
    elif mode == modes["rest_long"]:
        my_label.config(text=label_text, fg=GREENEST)
        my_check_label.config(text=checks)


def update_successful_countdown():
    global successful_countdown
    successful_countdown += 1
    if successful_countdown >= 8:
        successful_countdown = 0


def countdown(x):
    if x > 0:
        update_timer_text(x)
        refresh_screen()
        global my_timer_thread
        my_timer_thread = my_window.after(1000, countdown, x - 1)
    else:
        update_successful_countdown()
        refresh_screen()
        timer()


# ---------------------------- TIMER RESET ------------------------------- #

def reset():
    my_window.after_cancel(my_timer_thread)

    global successful_countdown, mode, checks, label_text, timer_text
    timer_text = "00:00"
    label_text = "Timer"
    checks = ""
    mode = None
    successful_countdown = 0
    my_label.config(text=label_text, background=YELLOW, foreground=GREEN, font=(FONT_NAME, 30, "bold"))
    my_canvas.itemconfig(canvas_timer, fill=GREEN, text=timer_text, font=(FONT_NAME, 30, "bold"))


# ---------------------------- UI SETUP ------------------------------- #
my_window = tkinter.Tk()
my_window.title("Pomodoro Timer")
my_window.config(bg=YELLOW, padx=50, pady=20)

my_label = tkinter.Label(text=label_text, background=YELLOW, foreground=GREEN, font=(FONT_NAME, 30, "bold"))
my_label.grid(row=0, column=1)

my_canvas = tkinter.Canvas(width=300, height=300, bg=YELLOW, highlightthickness=0)
photo = tkinter.PhotoImage(file="tomatoY.png")
my_canvas.create_image(150, 150, image=photo)
canvas_timer = my_canvas.create_text(150, 150, fill=GREEN, text=timer_text, font=(FONT_NAME, 30, "bold"))
my_canvas.grid(row=1, column=1)

my_start_button = tkinter.Button(text="Start", command=timer)
my_start_button.grid(row=2, column=0)

my_reset_button = tkinter.Button(text="Reset", command=reset)
my_reset_button.grid(row=2, column=2)

my_check_label = tkinter.Label(text=checks, background=YELLOW, foreground=REDISH)
my_check_label.grid(row=3, column=1)

my_window.mainloop()
