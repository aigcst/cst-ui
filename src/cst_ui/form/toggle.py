"""基于 fletmint"""

from dataclasses import dataclass
from typing import Any, Callable

import flet as ft


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


@dataclass
class Toggle(ft.Switch):
    value: bool = True
    label: str = "toggle"
    theme: ft.ThemeMode = ft.ThemeMode.DARK

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.apply_theme()
        return super().__post_init__(ref)

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

    def apply_theme(self):
        self.colors = ToggleColors.dark() if self.theme == ft.ThemeMode.DARK else ToggleColors.light()
        self.change_theme(self.colors)
        self.init_ui()

    def change_theme(self, colors=None):
        # Dynamically update attributes based on what is available in ToggleColors
        for attr in vars(colors):
            if hasattr(self, attr):
                setattr(self, attr, getattr(colors, attr))

    def toggle_theme(self):
        self.theme = ft.ThemeMode.LIGHT if self.theme == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.apply_theme()
        self.update()


def demo(page):
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
    page.add(demo(page))


if __name__ == "__main__":
    ft.run(main)
