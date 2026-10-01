from winotify import Notification, audio


def send_notification(title, message):

    toast = Notification(
        app_id="Task Manager",
        title=title,
        msg=message
    )

    toast.set_audio(
        audio.Default,
        loop=False
    )

    toast.show()

    print("Windows notification triggered")