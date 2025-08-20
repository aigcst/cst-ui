from dataclasses import dataclass
from enum import Enum
from typing import Any

import flet as ft


class DeltaType(Enum):
    normal = ft.Colors.BLACK
    good = ft.Colors.RED
    bad = ft.Colors.GREEN


@dataclass
class Metrics(ft.Container):
    label: str | ft.Text = ""
    value: int | str | ft.Text = ""
    delta_type: DeltaType = DeltaType.good
    delta: str = ""

    def __post_init__(self, ref: ft.Ref[Any] | None):
        if isinstance(self.label, str):
            self.label = ft.Text(
                value=self.label, theme_style=ft.TextThemeStyle.LABEL_SMALL
            )
        if (
            isinstance(self.value, str)
            or isinstance(self.value, int)
            or isinstance(self.value, float)
        ):
            self.value = ft.Text(
                value=self.value, theme_style=ft.TextThemeStyle.DISPLAY_SMALL
            )
        else:
            self.value = self.value
        icon = ft.Icons.ARROW_UPWARD
        if self.delta_type == DeltaType.good:
            icon = ft.Icons.ARROW_UPWARD
        elif self.delta_type == DeltaType.bad:
            icon = ft.Icons.ARROW_DOWNWARD
        self.v_delta = ft.Row(
            controls=[
                ft.Icon(name=icon, color=self.delta_type.value),
                ft.Text(
                    value=self.delta,
                    color=self.delta_type.value,
                ),
            ]
        )
        self.content = ft.Column(
            controls=[
                self.label,
                self.value,
                self.v_delta,
            ],
            spacing=0,
        )
        return super().__post_init__(ref)


def demo():
    return ft.Column(
        controls=[
            Metrics(
                label="数据量",
                value=100,
                delta="90%",
                delta_type=DeltaType.bad,
            )
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
