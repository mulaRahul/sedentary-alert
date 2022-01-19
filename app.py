import threading
from tkinter import Tk, ttk, \
    StringVar, IntVar

from _app import *

# load app data
JSDATA = load_json()

# root window
App = Tk()
App.title("Sedentary Alert")
App.iconbitmap(APP_ICO)
App.resizable(False, False)

# Sedentry Frame
frame = ttk.Frame(App, padding=10)
frame.grid(row=0, column=0, padx=10, pady=10)

sedentary_alert = IntVar()
interval_period = StringVar()

sedentary_alert.set(1 if JSDATA["sedentary_alert"]
                   else 0)


def toggle_sed_alert():
    JSDATA["sedentry_alert"] = bool(
        sedentary_alert.get()
    )
    update_json(JSDATA)

    if JSDATA["sedentry_alert"] and \
       not SED_THREAD.is_alive():

        init_sed_thread()
        SED_THREAD.start()


sed_check = ttk.Checkbutton(
    frame, variable=sedentary_alert, 
    text="Sedentry Alert", 
    command=toggle_sed_alert
)
sed_check.grid(row=0, column=0, 
               columnspan=2, pady=5)

sed_lbl = ttk.Label(sed_frame, text="Interval")
sed_lbl.grid(row=1, column=0, pady=5)


def interval_change(interval):
    JSDATA["interval"] = int(interval.split()[0])
    update_json(JSDATA)


interval_opt = ["2 min", "5 min", "10 min", 
                "15 min", "30 min", "45 min"]

interval_dropdown = ttk.OptionMenu(
    frame, interval_period, "Select",
    *interval_opt, command=interval_change
)
interval_dropdown.grid(row=1, column=1, padx=(10, 0))

interval_period.set(f'{JSDATA["interval"]} min')


# threading
def init_sed_thread():
    global SED_THREAD
    SED_THREAD = threading.Thread(
        target=sed_alert, daemon=True, 
    )


init_sed_thread()

if JSDATA["sedentary_alert"]:
    SED_THREAD.start()

App.mainloop()