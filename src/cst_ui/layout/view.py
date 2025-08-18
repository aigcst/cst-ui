from dataclasses import dataclass, field

import flet as ft
from flet.controls.core.view import Optional, PaddingValue


@dataclass
class View(ft.View):
    padding: Optional[PaddingValue] = field(default_factory=lambda: ft.Padding.all(10))
    scroll: Optional[ft.ScrollMode] = ft.ScrollMode.ADAPTIVE


def demo():
    return View(controls=[ft.Text("View")])


def main(page: ft.Page):
    page.title = "tabs"
    page.views = [demo()]


if __name__ == "__main__":
    ft.run(main)
