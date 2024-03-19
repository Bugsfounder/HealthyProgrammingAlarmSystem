import tkinter as tk
from tkinter import messagebox
from plyer import notification
import threading
import time
import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

Gst.init(None)


class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Break Alarm App")
        self.root.geometry("600x700")
        self.root.minsize(400, 400)
        self.root.maxsize(500, 610)

        self.label1 = tk.Label(root, text="Enter Total Work Time (hrs):")
        self.label1.pack()

        self.work_time = tk.Entry(root)
        self.work_time.pack()

        self.label2 = tk.Label(root, text="Enter Break Interval (minutes):")
        self.label2.pack()

        self.break_interval = tk.Entry(root)
        self.break_interval.pack()

        self.label3 = tk.Label(root, text="Enter Break Duration (minutes):")
        self.label3.pack()

        self.break_duration = tk.Entry(root)
        self.break_duration.pack()

        self.set_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack()

    def play_mp3(file_path):
        playbin = Gst.ElementFactory.make("playbin", "player")
        playbin.props.uri = f"./alarm_sounds/{file_path}"
        playbin.set_state(Gst.State.PLAYING)

        # Wait until playback is finished or interrupted
        bus = playbin.get_bus()
        bus.timed_pop_filtered(
            Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS
        )

        playbin.set_state(Gst.State.NULL)

    def show_notification(self, title, message):
        self.play_mp3("break.mp3")
        notification.notify(title=title, message=message, timeout=10)

    def start_alarm(self):
        total_work_time = float(self.work_time.get()) * 3600
        break_interval = float(self.break_interval.get()) * 60
        break_duration = float(self.break_duration.get()) * 60

        start_time = time.time()
        end_time = start_time + total_work_time

        while time.time() < end_time:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                break

            if remaining_time % break_interval < break_duration:
                self.show_notification(
                    "Take a Break",
                    f"Time to take a {break_duration/60:.1f}-minute break!",
                )
                time.sleep(break_duration)
                self.show_notification("Resume Work", "Time to resume work!")
            else:
                time.sleep(60)  # Check every minute

        self.show_notification(
            "Work Completed",
            "Your work session of {} hours is completed!".format(
                float(self.work_time.get())
            ),
        )
        self.root.destroy()

    def set_alarm(self):
        self.set_button["state"] = "disabled"
        alarm_thread = threading.Thread(target=self.start_alarm)
        alarm_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
