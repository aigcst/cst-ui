from dataclasses import dataclass
from typing import Any

import flet as ft
from flet.controls.material.segmented_button import Control, Optional

from cst_ui.basic.theme import theme


@dataclass
class Segment(ft.Segment):
    def __post_init__(self, ref: ft.Ref[Any] | None):
        if self.label is None:
            self.label = ft.Text(value=self.value)
        return super().__post_init__(ref)


@dataclass
class SegmentedButton(ft.SegmentedButton):
    segments: list[Segment] | None = None
    option_list: list | None = None
    selected_icon: Optional[Control] = ft.Icon(
        name=ft.Icons.CHECK, color=ft.Colors.WHITE
    )
    allow_multiple_selection: bool = True
    allow_empty_selection: bool = True

    def __post_init__(self, ref: ft.Ref[Any] | None):
        if self.option_list is not None:
            self.segments = [Segment(_) for _ in self.option_list]
        # self.view_width = len(text_list) * btn_width + 2
        self.style = ft.ButtonStyle(
            color={
                ft.ControlState.SELECTED: ft.Colors.WHITE,
            },
            bgcolor={
                # ft.ControlState.HOVERED: ft.Colors.RED,
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                ft.ControlState.SELECTED: theme.color.primary,
            },
            shape={
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=6),
                ft.ControlState.SELECTED: ft.RoundedRectangleBorder(radius=6),
            },
        )
        return super().__post_init__(ref)

    # # selected
    # @property
    # def selected(self) -> Optional[Set]:
    #     s = self.v_content._get_attr("selected")
    #     return set(json.loads(s)) if s else s

    # @selected.setter
    # def selected(self, value: Optional[Set]):
    #     self.v_content._set_attr(
    #         "selected",
    #         (
    #             json.dumps(list(value), separators=(",", ":"))
    #             if value is not None
    #             else None
    #         ),
    #     )


def demo():
    tmp_seg_button = SegmentedButton(
        # selected={"1", "4"},
        allow_multiple_selection=True,
        selected=["333"],
        allow_empty_selection=True,
        option_list=["1122", "2333", "3444", "344e44", "555455"],
    )
    print(tmp_seg_button.allow_multiple_selection)
    print(tmp_seg_button.allow_empty_selection)
    return ft.Column(
        controls=[
            # SegmentedButton(
            #     # label="test",
            #     # selected={"1", "4"},
            #     # allow_multiple_selection=True,
            #     selected={"1"},
            #     allow_empty_selection=True,
            #     option_list=["1", "2", "3", "4"],
            # ),
            tmp_seg_button,
        ]
    )


def main(page: ft.Page):
    page.title = "Test MyControl"
    page.add(demo())


if __name__ == "__main__":
    ft.run(main)
