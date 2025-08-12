import flet as ft
import flet_audio


class Audio(ft.Container):
    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.audio_state = {
            "is_playing": False,
            "is_paused": False,
            "is_stopped": False,
            "duration": 0,
            "current_position": 0,
        }
        self.kwargs = kwargs
        self.setup_audio()
        self.build_audioplayer()

    def did_mount(self):
        self.page: ft.Page
        self.page.services.append(self.audio)
        # self.track_canvas.audio_duration = self.audio1.get_duration()
        # self.page.update()

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{int(mins):02}:{int(secs):02}"

    def update_total_time(self):
        self.total_time.value = self.format_time(self.audio_state["duration"])
        self.total_time.update()

    def update_duration(self, seconds):
        self.audio_state["current_position"] = seconds
        self.position_slider.value = (
            (seconds / self.audio_state["duration"]) * self.position_slider.max
            if self.audio_state["duration"] > 0
            else 0
        )
        self.position_slider.update()
        self.time_elapsed.value = self.format_time(seconds)
        self.time_elapsed.update()

    def on_slider_change(self, e):
        new_position = (e.control.value / 100) * self.audio_state["duration"]
        self.audio.position = new_position * 1000  # Set position in milliseconds
        self.update_duration(new_position)

    def seek(self, seconds):
        new_position = max(
            0,
            min(
                self.audio_state["duration"],
                self.audio_state["current_position"] + seconds,
            ),
        )  # Ensure within bounds
        self.audio.position = new_position * 1000  # Set position in milliseconds
        self.update_duration(new_position)

    def handle_play_or_pause(self, e):
        if self.audio_state["is_playing"]:
            self.audio.pause()
            self.audio_state["is_playing"] = False
            self.audio_state["is_paused"] = True
            new_icon = ft.Icon(name=ft.Icons.PLAY_ARROW_ROUNDED)
        # Check if the audio is paused
        elif self.audio_state["is_paused"]:
            self.audio.resume()
            self.audio_state["is_playing"] = True
            self.audio_state["is_paused"] = False
            new_icon = ft.Icon(name=ft.Icons.PAUSE_ROUNDED)
        # If the audio is neither playing nor paused (stopped or initial state)
        elif self.audio_state["is_stopped"]:
            self.audio_state["is_playing"] = False
            self.audio_state["is_paused"] = False
            self.audio_state["is_stopped"] = False
            new_icon = ft.Icon(name=ft.Icons.PLAY_ARROW_ROUNDED)
        else:
            self.audio.play()
            self.audio_state["is_playing"] = True
            self.audio_state["is_paused"] = False
            self.audio_state["is_stopped"] = False
            new_icon = ft.Icon(name=ft.Icons.PAUSE_ROUNDED)

        if self.play_button.content != new_icon:
            self.play_button.content = new_icon
            self.play_button.update()

    def setup_audio(self):
        self.audio = flet_audio.Audio(
            src=self.url,
            autoplay=False,
            volume=1,
            balance=0,
            on_loaded=lambda _: print("AudioPlayer: Audio Loaded"),
            on_duration_change=lambda e: (
                self.audio_state.update({"duration": int(e.duration) / 1000}),
                self.update_total_time(),
            ),
            on_position_change=lambda e: self.update_duration(int(e.position) / 1000),
            # on_state_change=lambda e: (
            #     print("AudioPlayer: State changed:", e.data),
            #     self.audio_state.update({"is_playing": e.data == "playing", "is_paused": e.data == "paused"}),
            # ),
            # on_seek_complete=lambda e: (
            #     self.audio_state.update({"is_stopped": True}),
            #     self.handle_play_or_pause(e),
            # ),
        )

    def build_audioplayer(self):
        self.time_elapsed = ft.Text("00:00")
        self.total_time = ft.Text("00:00")
        self.position_slider = ft.Slider(
            thumb_color=ft.Colors.with_opacity(0, "white"),
            overlay_color=ft.Colors.with_opacity(0, "white"),
            # secondary_track_value=ft.Colors.with_opacity(0, "white"),
            active_color="#1f5eff",
            inactive_color="#323741",
            max=100,
            on_change=self.on_slider_change,
        )
        self.play_button = ft.TextButton(
            on_click=self.handle_play_or_pause,
            content=ft.Icon(name=ft.Icons.PLAY_ARROW_ROUNDED),
            style=ft.ButtonStyle(
                color="#ffffff", bgcolor="#1f5eff", shape=ft.CircleBorder(), padding=15
            ),
        )
        self.content = ft.Row(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.REPLAY_10_ROUNDED,
                            icon_color="#ffffff,0.5",
                            on_click=lambda _: self.seek(-10),
                        ),
                        self.play_button,
                        ft.IconButton(
                            icon=ft.Icons.FORWARD_10_ROUNDED,
                            icon_color="#ffffff,0.5",
                            on_click=lambda _: self.seek(10),
                        ),
                    ],
                    spacing=0,
                ),
                self.position_slider,
                ft.Row([self.time_elapsed, ft.Text("/"), self.total_time], spacing=1),
            ],
            spacing=3,
        )
        self.width = 450
        self.padding = ft.Padding.symmetric(vertical=5, horizontal=15)
        self.bgcolor = "#323741"
        self.border = ft.Border.all(1, "#3d424d")
        self.border_radius = 14


def demo():
    return ft.Row(controls=[Audio(url=r"data\野蜂飞舞.mp3")])


def main(page: ft.Page):
    page.title = "Test"
    # page.theme_mode = "dark"
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
