from dataclasses import dataclass
from typing import Any, Optional

import flet as ft

from cst_ui.basic.theme import theme


@dataclass
class Tabs(ft.Tabs):
    label_color = theme.color.primary
    indicator_color = theme.color.primary
    unselected_label_color = '#777777'


@dataclass
class Tab(ft.Tab):
    text: str | ft.Control = ''

    def __post_init__(self, ref: ft.Ref[Any] | None):
        if isinstance(self.text, str):
            self.tab_content = ft.Column(
                controls=[ft.Text(value=self.text, text_align=ft.TextAlign.CENTER)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        return super().__post_init__(ref)

    def handle_content_hover(self, e: ft.HoverEvent):
        e.control.bgcolor = ft.Colors.RED
        e.control.update()

    @property
    def content(self) -> Optional[ft.Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[ft.Control]):
        if getattr(value, 'padding', None) is None:
            self.__content = ft.Container(value, padding=ft.padding.all(10))
        else:
            self.__content = value


def demo():
    return ft.TabBar(
        tabs=[
            ft.Tab(
                label='123',
                # content=ft.Container(content=ft.Text('tab_content 123')),
            ),
            ft.Tab(
                label='345',
                # content=ft.Container(
                #     content=Tabs(
                #         tabs=[
                #             Tab(text='123', content=ft.Text('tab_content 123')),
                #             Tab(text='345', content=ft.Text('tab_content 345')),
                #         ],
                #     ),
                # ),
            ),
        ]
    )


def main(page: ft.Page):
    page.title = 'tabs'
    page.add(demo())

    # tab_origin = ft.Tabs(
    #     tabs=[
    #         ft.Tab("123", ft.Container(ft.Text("123"))),
    #         ft.Tab("345", ft.Container(ft.Text("345"))),
    #     ]
    # )
    # page.add(tab_origin)


if __name__ == '__main__':
    ft.run(main)
