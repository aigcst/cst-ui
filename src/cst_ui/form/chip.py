from typing import Callable

import flet as ft

from cst_ui.basic.theme import theme


class Chip(ft.Chip):
    def __init__(self, text: str, **kwargs):
        kwargs.setdefault("label", ft.Text(value=""))
        super().__init__(**kwargs)
        self.label = ft.Text(value=text)

        self.selected_color = theme.color.success

        self.check_color = ft.Colors.WHITE

    def before_update(self):
        super().before_update()
        self.label: ft.Text
        if self.selected:
            self.label.color = ft.Colors.WHITE
        else:
            self.label.color = ft.Colors.BLACK


def get_ui_view():
    return ft.Column(
        controls=[
            Chip(text="test", on_select=lambda _: print("Chip: ", _)),
            Chip(
                text="test delete",
                on_select=lambda _: print("Chip: ", _),
                delete_icon=ft.Icon(ft.Icons.CANCEL),
                delete_icon_color=ft.Colors.RED,
                delete_icon_tooltip="删除",
            ),
        ]
    )


def main(page: ft.Page):
    page.title = "Test"
    page.add(get_ui_view())
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
