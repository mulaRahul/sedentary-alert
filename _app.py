import os
import json
import platform
from os import path
from time import sleep


# assets
ASSETS = "assets"

SUN_VALLEY_THEME = path.join("SunValley",
                             "sun-valley.tcl")
APP_ICO = path.join(ASSETS, "app.ico")
COFFE_ICO = path.join(ASSETS, "coffe.ico")
DOLPHIN_WAV = path.join(ASSETS, "dolphin.wav")

# utils
def min_to_sec(min):
    return min * 60

# data
JSDATA: dict

def load_json() -> dict:
    with open('schedule.json') as dt:
        return json.load(dt)

def update_json(jsdata:dict):
    with open('schedule.json', "w") as jsfile:
        json.dump(
            jsdata, jsfile, indent=2
        )


# notifier
def _notify(
    msg,
    icon,
    title=None,
    soundfile=DOLPHIN_WAV,
):
    os_platform =  platform.system()
    if os_platform == 'Windows':
            import winsound
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            
            toaster.show_toast(
                title=title if title else "Notification",
                msg=msg,
                icon_path=icon,
                threaded=True,
            )
            if soundfile:
                winsound.PlaySound(
                    soundfile, winsound.SND_FILENAME
                )
            
    elif os_platform == 'Darwin': # mac
            from playsound import playsound
            
            title = title if title else "Notification"
            os.system("osascript -e 'display notification"
                      f' "{msg}" with title "{title}"\'')
            
            if soundfile:
               playsound(soundfile)


def sed_alert():
    dt = load_json()

    if dt["sedentary_alert"]:
        interval = min_to_sec(dt["interval"])
        sleep(interval)
        try:
            _notify(
                title="Sedentary Alert",
                msg=("Drink water, fix "
                    "your posture and keep "
                    "blinking your eyes!"),
                icon=COFFE_ICO,
            )
        except ImportError:
            print("Modules not found")
        
        sed_alert()