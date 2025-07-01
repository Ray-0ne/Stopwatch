import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.core.audio import SoundLoader

class CountdownApp(BoxLayout):
    def __init__(self, **kwargs):
        super(CountdownApp, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Hour Spinner
        self.hour_spinner = Spinner(
            text='0',
            values=[str(i) for i in range(24)],
            size_hint=(None, None),
            size=(100, 44)
        )
        self.add_widget(self.hour_spinner)

        # Minute Spinner
        self.minute_spinner = Spinner(
            text='0',
            values=[str(i) for i in range(60)],
            size_hint=(None, None),
            size=(100, 44)
        )
        self.add_widget(self.minute_spinner)

        self.start_button = Button(text="Start")
        self.start_button.bind(on_press=self.toggle_start_pause)
        self.add_widget(self.start_button)

        self.reset_button = Button(text="Reset")
        self.reset_button.bind(on_press=self.reset_timer)
        self.add_widget(self.reset_button)

        self.time_label = Label(text="Time left: 00:00:00", halign='center')
        self.add_widget(self.time_label)

        self.progress_bar = ProgressBar(max=1)
        self.add_widget(self.progress_bar)

        self.total_seconds = 0
        self.remaining_seconds = 0
        self.is_running = False
        self.alarm_sound = SoundLoader.load('alarm.wav')

    def toggle_start_pause(self, instance):
        if not self.is_running:
            self.total_seconds = (
                int(self.hour_spinner.text) * 3600 +
                int(self.minute_spinner.text) * 60
            )
            if self.total_seconds == 0:
                return
            self.remaining_seconds = self.total_seconds
            self.is_running = True
            self.start_button.text = "Pause"
            Clock.schedule_interval(self.update_countdown, 1)
        else:
            self.is_running = False
            self.start_button.text = "Resume"
            Clock.unschedule(self.update_countdown)

    def reset_timer(self, instance):
        self.is_running = False
        self.remaining_seconds = 0
        self.start_button.text = "Start"
        self.progress_bar.value = 0
        self.time_label.text = "Time left: 00:00:00"
        Clock.unschedule(self.update_countdown)

    def update_countdown(self, dt):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
        else:
            self.is_running = False
            self.play_alarm()
            self.progress_bar.value = 1
            self.start_button.text = "Start"
            self.remaining_seconds = 0
            self.show_notification()
            Clock.unschedule(self.update_countdown)

    def play_alarm(self):
        if self.alarm_sound:
            self.alarm_sound.play()

    def update_display(self):
        time_str = f"{self.remaining_seconds // 3600:02}:{(self.remaining_seconds % 3600) // 60:02}:{self.remaining_seconds % 60:02}"
        self.time_label.text = f"Time left: {time_str}"
        if self.total_seconds > 0:
            progress = 1 - (self.remaining_seconds / self.total_seconds)
            self.progress_bar.value = progress

    def show_notification(self):
        from kivy.uix.popup import Popup
        popup = Popup(title="Time's Up!", content=Label(text="The countdown has finished!"), size_hint=(0.6, 0.4))
        popup.open()

class CountdownAppMain(App):
    def build(self):
        return CountdownApp()

if __name__ == '__main__':
    CountdownAppMain().run()
