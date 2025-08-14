from dataclasses import dataclass
from typing import Any

import flet as ft

from cst_ui.basic.theme import theme


@dataclass
class Card(ft.Card):
    elevation: ft.Number = 0

    def __post_init__(self, ref: ft.Ref[Any] | None):
        if self.content is not None:
            self.v_container = ft.Container(
                width=self.width,
                height=self.height,
                bgcolor=ft.Colors.WHITE,
                border_radius=theme.border_radius.x_large,
                on_hover=lambda e: self.on_card_hover(e),
                animate=ft.Animation(600, ft.AnimationCurve.EASE),
                border=ft.Border.all(2, ft.Colors.WHITE24),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                    controls=[self.content],
                ),
            )
            self.content = ft.Container(
                content=ft.Column(
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[self.v_container],
                )
            )
        return super().__post_init__(ref)

    def on_card_hover(self, e):
        if e.data:
            for __ in range(20):
                self.elevation = self.elevation + 1

            self.v_container.border = ft.Border.all(2, theme.color.primary)
            self.v_container.update()

        else:
            for __ in range(20):
                self.elevation = self.elevation - 1

            self.v_container.border = ft.Border.all(2, ft.Colors.WHITE24)
            self.v_container.update()


def demo():
    now_card = Card(
        content=ft.Container(
            content=ft.Column(controls=[ft.Text("text"), ft.Text("text")]),
            width=300,
            height=200,
        )
    )
    return ft.Column(controls=[now_card])


def main(page: ft.Page):
    page.bgcolor = ft.Colors.WHITE60
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
