from dataclasses import dataclass

import flet as ft


@dataclass
class Switch(ft.CupertinoSwitch):
    active_color = "#1f5eff"
    track_color = ft.Colors.GREY
    offset = ft.Offset(x=-0.3, y=0)
    scale = 0.6


@dataclass
class ToggleColors:
    label_text_color: str
    default_outline_color: str
    selected_outline_color: str
    default_thumb_color: str
    selected_thumb_color: str
    selected_track_color: str
    default_track_color: str = ""  # Optional attribute not needed for the dark theme

    @staticmethod
    def dark():
        return ToggleColors(
            label_text_color="#515766",
            default_outline_color="#494D5F",
            selected_outline_color="#1f5eff",
            default_thumb_color="#7b849c",
            selected_thumb_color="#ffffff",
            selected_track_color="#1f5eff",
        )

    @staticmethod
    def light():
        return ToggleColors(
            label_text_color="#697492",
            default_outline_color="#c1c9df",
            selected_outline_color="#1f5eff",
            default_thumb_color="#7b849c",
            selected_thumb_color="#ffffff",
            selected_track_color="#1f5eff",
            default_track_color="#ffffff",
        )


class Toggle(ft.Switch):
    """参考 fletmint"""

    def __init__(
        self, on_change, value=True, label="toggle", theme=ft.ThemeMode.DARK, **kwargs
    ):
        super().__init__(**kwargs)
        self.label = label
        self.on_change = on_change
        self.value = value
        self.theme = theme
        self.apply_theme()

    def init_ui(self):
        self.label = f" {self.label}"
        self.label_style = ft.TextStyle(color=self.colors.label_text_color, size=15)
        self.value = self.value
        self.track_outline_color = {
            ft.ControlState.DEFAULT: self.colors.default_outline_color,
            ft.ControlState.SELECTED: self.colors.selected_outline_color,
        }
        self.thumb_color = {
            ft.ControlState.DEFAULT: self.colors.default_thumb_color,
            ft.ControlState.SELECTED: self.colors.selected_thumb_color,
        }

        self.track_color = {
            ft.ControlState.DEFAULT: self.colors.default_track_color,
            ft.ControlState.SELECTED: self.colors.selected_track_color,
        }
        self.overlay_color = ft.Colors.with_opacity(0, "white")
        self.on_change = self.on_change

    def apply_theme(self):
        self.colors = (
            ToggleColors.dark()
            if self.theme == ft.ThemeMode.DARK
            else ToggleColors.light()
        )
        self.change_theme(self.colors)
        self.init_ui()

    def change_theme(self, colors=None):
        # Dynamically update attributes based on what is available in ToggleColors
        for attr in vars(colors):
            if hasattr(self, attr):
                setattr(self, attr, getattr(colors, attr))

    def toggle_theme(self):
        self.theme = (
            ft.ThemeMode.LIGHT if self.theme == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        self.apply_theme()
        self.update()


def demo():
    def test(e):
        pass

    return ft.Column(
        controls=[
            Toggle(
                on_change=test,
            )
        ],
    )


def main(page: ft.Page):
    page.add(demo())


if __name__ == "__main__":
    ft.run(main)
