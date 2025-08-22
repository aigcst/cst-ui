from dataclasses import dataclass, field
from typing import Any, Callable, List

import flet as ft


@dataclass
class SearchBar(ft.SearchBar):
    options: List[str] = field(default_factory=list)
    on_click: Callable | None = None

    def __post_init__(self, ref: ft.Ref[Any] | None):
        for _ in self.options:
            self.controls.append(ft.ListTile(title=ft.Text(_), on_click=self.on_click, data=_))
        return super().__post_init__(ref)


def demo():
    return ft.Column(
        controls=[
            SearchBar(),
        ]
    )


def main(page: ft.Page):
    page.title = 'Paging'
    page.scroll = ft.ScrollMode.AUTO
    page.add(demo())


if __name__ == '__main__':
    ft.run(main)
