import os
import json
import platform
from os import path
from time import sleep


# assets
ASSETS = "assets"

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


# Using if instead of match so that it 
# works on python versions below 3.10
os_platform =  platform.system()
if os_platform == 'Windows':    

    def _notify(
        msg,
        icon=COFFE_ICO,
        title=None,
        soundfile=DOLPHIN_WAV,
    ):

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
    
    def _notify(
        msg,
        title=None,
        soundfile=DOLPHIN_WAV,
    ):
        from playsound import playsound
        
        title = title if title else "Notification"
        # command: osascript -e 'display notification "message" with "title"'
        # the script is with-in single quotes and
        # message & title within double quotes
        os.system(f"""osascript -e 'display notification "{msg}" with title "{title}"'""")
        
        if soundfile:
            playsound(soundfile)


def sed_alert():
    dt = load_json()

    if dt["sedentary_alert"]:
        interval = min_to_sec(dt["interval"])
        sleep(interval)

        _notify(
                title="Sedentary Alert",
                msg=("Drink water, fix "
                    "your posture and keep "
                    "blinking your eyes!")
            )
        
        sed_alert()