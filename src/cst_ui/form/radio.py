from dataclasses import dataclass
from typing import Any

import flet as ft

from cst_ui.basic.theme import LayoutType, theme


@dataclass
class Radio(ft.RadioGroup):
    content: ft.Control | None = None
    options: list | None = None
    radio_layout_type: LayoutType = LayoutType.HORIZONTAL

    def __post_init__(self, ref: ft.Ref[Any] | None):
        if self.options is not None:
            for idx, _ in enumerate(self.options):
                if isinstance(_, str):
                    self.options[idx] = ft.Radio(
                        label=_,
                        value=_,
                        label_position=ft.LabelPosition.RIGHT,
                        # BUG: active_color的优先级比fill_color的低
                        # fill_color=ft.Colors.GREY_400,
                        active_color=theme.color.primary,
                    )
        if self.radio_layout_type == LayoutType.HORIZONTAL:
            self.content = ft.Row(controls=self.options)
        else:
            self.content = ft.Column(controls=self.options, spacing=2, run_spacing=10)

        return super().__post_init__(ref)


def demo():
    return ft.Column(
        controls=[
            Radio(options=["aa", "bb", "cc"]),
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
