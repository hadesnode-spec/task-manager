import shutil
import subprocess
 
 
def send_notification(title, message):
 
    if shutil.which("notify-send") is None:
        print("notify-send not found. Install it with:")
        print("  sudo apt install libnotify-bin")
        return
 
    subprocess.run(
        [
            "notify-send",
            "--app-name=Task Manager",
            "--urgency=critical",
            title,
            message
        ],
        check=False
    )
 
    sound_file = "/usr/share/sounds/freedesktop/stereo/message.oga"
 
    if shutil.which("paplay"):
        subprocess.Popen(
            ["paplay", sound_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
 
    print("Linux notification triggered")
