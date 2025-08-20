from dataclasses import dataclass, field
from typing import Any

import flet as ft
from flet.controls.material.dropdownm2 import Option

from cst_ui.basic.theme import theme

ICON_SIZE = 18
TEXT_SIZE = 14
PADDING = 10
INPUT_HEIGHT = 36


@dataclass
class DropDownColors:
    container_background_color: str
    container_border_color: str
    selected_control_background_color: str
    selected_control_text_color: str
    unselected_control_text_color: str
    dropdown_starter_icon_color: str

    @staticmethod
    def dark():
        return DropDownColors(
            container_background_color="#323741",
            container_border_color="#3d424d",
            selected_control_background_color="#2a2e35",
            selected_control_text_color=ft.Colors.with_opacity(0.9, "white"),
            unselected_control_text_color="#959cae",
            dropdown_starter_icon_color="#ffffff",
        )

    @staticmethod
    def light():
        return DropDownColors(
            container_background_color="#ffffff",
            container_border_color="#d9deec",
            selected_control_background_color="#e9efff",
            selected_control_text_color="#5182ff",
            unselected_control_text_color="#646f8e",
            dropdown_starter_icon_color="#7e879e",
        )


@dataclass
class SelectOption(Option):
    text: str = ""  # 不可为None

    def __post_init__(self, ref: ft.Ref[Any] | None):
        # self.selected = True
        # if self.selected:
        self.content = ft.Container(
            content=ft.Row(controls=[ft.Text(value=self.text)]),
            # bgcolor=ft.Colors.RED,
            margin=0,
            height=36,
            expand=True,
        )
        self.key = self.key or self.text
        return super().__post_init__(ref)


@dataclass
class SelectBox(ft.DropdownM2):
    option_list: list = field(default_factory=list)
    theme_mode: ft.ThemeMode = ft.ThemeMode.LIGHT
    options: list[SelectOption] = field(default_factory=list)

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.height = INPUT_HEIGHT
        # if self.options is None:
        # self.options = []
        for idx, _ in enumerate(self.option_list):
            if isinstance(self.option_list[idx], str):
                self.options.append(SelectOption(key=_, text=_))
            else:
                self.options.append(_)

        self.text_style = ft.TextStyle(size=TEXT_SIZE, color=ft.Colors.BLACK)
        self.content_padding = ft.padding.only(left=PADDING)

        self.colors = (
            DropDownColors.dark()
            if self.theme_mode == ft.ThemeMode.DARK
            else DropDownColors.light()
        )
        self.border_color = ft.Colors.GREY_400
        self.bgcolor = ft.Colors.WHITE
        self.border_width = 1
        self.border_radius = 6
        self.focused_border_color = theme.color.primary
        self.select_icon_enabled_color = ft.Colors.GREY_500
        self.padding = ft.padding.all(0)
        self.options_fill_horizontally = True

        self.content_padding = ft.padding.all(0)
        self.dense = True
        self.filled = True
        self.max_menu_height = 1000
        self.item_height = 48
        self.animate_size = 5000

        self.padding = ft.padding.only(left=20)
        self.focused_border_color = ft.Colors.RED
        return super().__post_init__(ref)


def demo():
    return ft.Column(
        controls=[
            SelectBox(
                # label="选择",
                option_list=["zhang", "li", "chen", "aa", "bb", "cc"],
            ),
            # ft.DropdownM2(
            #     options=[
            #         ft.dropdown.Option("zhang"),
            #         ft.dropdown.Option("li"),
            #         ft.dropdown.Option("chen"),
            #     ],
            #     height=20,
            # ),
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
