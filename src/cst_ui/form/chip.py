from dataclasses import dataclass
from typing import Optional

import flet as ft
from flet.controls.material.chip import (
    AnimationStyle,
    BorderSide,
    BoxConstraints,
    ClipBehavior,
    ColorValue,
    Control,
    ControlEventHandler,
    ControlStateValue,
    Number,
    OutlinedBorder,
    PaddingValue,
    StrOrControl,
    TextStyle,
    VisualDensity,
)

from cst_ui.basic.theme import theme


@dataclass
class Chip(ft.Chip):
    text: str = ""
    label: StrOrControl = ft.Text(value="")  # 添加默认值
    leading: Optional[Control] = None
    selected: bool = False
    selected_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    bgcolor: Optional[ColorValue] = None
    show_checkmark: bool = True
    check_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    shape: Optional[OutlinedBorder] = None
    padding: Optional[PaddingValue] = None
    delete_icon: Optional[Control] = None
    delete_icon_tooltip: Optional[str] = None
    delete_icon_color: Optional[ColorValue] = None
    disabled_color: Optional[ColorValue] = None
    label_padding: Optional[PaddingValue] = None
    label_text_style: Optional[TextStyle] = None
    selected_shadow_color: Optional[ColorValue] = None
    autofocus: bool = False
    surface_tint_color: Optional[ColorValue] = None
    color: Optional[ControlStateValue[ColorValue]] = None
    elevation_on_click: Optional[Number] = None
    clip_behavior: ClipBehavior = ClipBehavior.NONE
    visual_density: Optional[VisualDensity] = None
    border_side: Optional[BorderSide] = None
    leading_size_constraints: Optional[BoxConstraints] = None
    delete_icon_size_constraints: Optional[BoxConstraints] = None
    enable_animation_style: Optional[AnimationStyle] = None
    select_animation_style: Optional[AnimationStyle] = None
    leading_drawer_animation_style: Optional[AnimationStyle] = None
    delete_drawer_animation_style: Optional[AnimationStyle] = None
    on_click: Optional[ControlEventHandler["Chip"]] = None
    on_delete: Optional[ControlEventHandler["Chip"]] = None
    on_select: Optional[ControlEventHandler["Chip"]] = None
    on_focus: Optional[ControlEventHandler["Chip"]] = None
    on_blur: Optional[ControlEventHandler["Chip"]] = None

    # self.text = text
    # self.label: ft.Text

    def before_update(self):
        super().before_update()
        self.selected_color = theme.color.success
        # 改 label为text
        self.label = ft.Text(value=self.text)

        self.check_color = ft.Colors.WHITE
        if self.selected:
            self.label.color = ft.Colors.WHITE
        else:
            self.label.color = ft.Colors.BLACK


def demo(page: ft.Page):
    v_ft = ft.Chip(label="", selected=True)
    v_column = ft.Column(
        controls=[
            Chip(
                text="test",
                selected=True,
                on_select=lambda _: print("Chip: ", _),
            ),
            Chip(
                text="test delete",
                on_select=lambda _: None,  # 空操作
                delete_icon=ft.Icon(ft.Icons.CANCEL),
                delete_icon_color=ft.Colors.RED,
                delete_icon_tooltip="删除",
            ),
            v_ft,
        ]
    )
    return v_column


def main(page: ft.Page):
    page.add(demo(page=page))


if __name__ == "__main__":
    ft.run(main)
