"""评级"""

from dataclasses import dataclass
from typing import Any, Callable

import flet as ft


@dataclass
class Rating(ft.Row):
    readonly: bool = False
    disabled: bool = False
    cancel: bool = False
    elements: int = 5
    rating: int | None = None
    on_change: Callable | None = None
    rating: int | None = None

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.rating = self.rating - 1 if self.rating is not None else self.rating
        self.on_change = self.on_change or (lambda x: None)
        self.row_elements: list[ft.IconButton] = []
        self.references: list[ft.Ref] = []

        self._add_cancel()
        self._add_elements()
        self.controls = self.row_elements  # type: ignore
        self.spacing = 0
        return super().__post_init__(ref)

    def _add_elements(self):
        for i in range(0, self.elements):
            element_ref = ft.Ref[ft.IconButton]()
            self.references.append(element_ref)
            is_selected = True if self.rating is not None and i <= self.rating else False
            self.row_elements.append(
                ft.IconButton(
                    icon=ft.Icons.STAR_BORDER,
                    ref=element_ref,
                    icon_color=ft.Colors.GREY,
                    selected_icon=ft.Icons.STAR,
                    selected_icon_color=ft.Colors.GREY if self.disabled else ft.Colors.BLUE,
                    data=i,
                    selected=is_selected,
                    disabled=self.disabled,
                    on_click=self._select,
                )
            )

    def _add_cancel(self):
        if self.cancel:
            self.row_elements.append(
                ft.IconButton(
                    icon=ft.Icons.CANCEL_OUTLINED,
                    icon_color=ft.Colors.RED,
                    on_click=self._reset,
                )
            )

    def _reset(self, e):
        if self.readonly:
            return
        for i in range(self.elements - 1, -1, -1):
            ref: ft.Ref[ft.IconButton] = self.references[i]
            ref.current.selected = False
            self.rating = None
        self.update()

    def _select(self, e):
        if self.readonly:
            return

        if self.rating is not None and e.control.data == self.rating:
            self._reset(e)
        else:
            for i in range(self.elements - 1, -1, -1):
                if e.control.data >= i:
                    ref: ft.Ref[ft.IconButton] = self.references[i]
                    ref.current.selected = True
                else:
                    ref: ft.Ref[ft.IconButton] = self.references[i]
                    ref.current.selected = False
            self.rating = e.control.data
        self._on_change(self.rating)
        self.update()

    def _on_change(self, e) -> None:
        if e is not None:
            self.on_change(e + 1)
        else:
            self.on_change(0)

    def did_mount(self):
        return super().did_mount()

    def will_unmount(self):
        return super().will_unmount()


def demo():
    def rating_cb(e):
        print(f"Rating: Callback {e}")
        # page.update()

    return ft.Column(
        controls=[
            ft.Text("Basic example"),
            Rating(),
            ft.Divider(),
            ft.Text("Cancel"),
            Rating(cancel=True),
            ft.Divider(),
            ft.Text("Readonly"),
            Rating(readonly=True, rating=3),
            ft.Divider(),
            ft.Text("Disabled"),
            Rating(rating=4, disabled=True),
            ft.Divider(),
            Rating(on_change=rating_cb),
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
