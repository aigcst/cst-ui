from dataclasses import dataclass
from typing import Any

import flet as ft
from flet.controls.material.expansion_tile import Optional, StrOrControl


@dataclass
class Expander(ft.ExpansionTile):
    title: StrOrControl | ft.Container
    dense: Optional[bool] = None

    def __post_init__(self, ref: ft.Ref[Any] | None):
        if isinstance(self.title, str):
            self.title = ft.Container(ft.Text(self.title), on_hover=self.handle_hover)
        if isinstance(self.subtitle, str):
            self.subtitle = ft.Container(ft.Text(self.subtitle))
        else:
            self.subtitle = ft.Container(self.subtitle)
        if self.controls is not None:
            self.controls = [
                ft.Container(
                    ft.Column(
                        controls=self.controls,
                        spacing=0,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    expand=True,
                    alignment=ft.Alignment.TOP_LEFT,
                    padding=ft.padding.only(left=16),
                )
            ]
        self.affinity = ft.TileAffinity.PLATFORM
        self.bgcolor = ft.Colors.GREY_200
        self.collapsed_bgcolor = ft.Colors.GREY_200
        self.expanded_cross_axis_alignment = ft.CrossAxisAlignment.START
        return super().__post_init__(ref)

    def handle_hover(self, e):
        self.title: StrOrControl | ft.Container
        if isinstance(self.title, ft.Container):
            self.title.bgcolor = ft.Colors.GREY_400 if e.data else ft.Colors.GREY_200
        if self.subtitle is not None and isinstance(self.subtitle, ft.Container):
            self.subtitle.bgcolor = ft.Colors.GREY_400 if e.data else ft.Colors.GREY_200


def demo():
    return ft.Column(
        controls=[
            Expander(
                title="ExpansionTile 3",
                subtitle=ft.Text("Leading expansion arrow icon"),
                controls=[
                    ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                    ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                    ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ],
            ),
            Expander(
                title="ExpansionTile 3",
                controls=[
                    ft.Text("This is sub-tile number 3"),
                    ft.Text("This is sub-tile number 4"),
                    ft.Text("This is sub-tile number 5"),
                ],
            ),
            Expander(
                title="ExpansionTile 3",
                controls=[
                    ft.Text("This is sub-tile number 3"),
                    ft.Text("This is sub-tile number 4"),
                    ft.Text("This is sub-tile number 5"),
                ],
            ),
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
