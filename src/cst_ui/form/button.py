"""按钮"""

from enum import Enum
from typing import Optional

import flet as ft

from cst_ui.basic.theme import StyleType, theme


class ButtonSizeType(Enum):
    small = 30
    medium = 36
    large = 42


class ButtonShapeType(Enum):
    # 直角
    rect = "rect"
    # 圆弧（默认）
    circle = "circle"
    # 半圆
    round = "round"


class Button(ft.Button):
    def __init__(
        self,
        text: Optional[str] = None,
        style_type: StyleType = StyleType.DEFAULT,
        size_type: ButtonSizeType = ButtonSizeType.medium,
        shape_type: ButtonShapeType = ButtonShapeType.round,
        plain=False,  # 中心是否镂空
        **kwargs,
    ):
        # kwargs.setdefault('icon_color', ft.Colors.WHITE)
        super().__init__(**kwargs)
        self.text = text
        self.update_content()

        self.style_type = style_type
        self.shape_type = shape_type
        self.size_type = size_type
        self.plain = plain
        self.height = size_type.value

        self.height = size_type.value
        # self.content = ft.Text(value=text)
        self.style = ft.ButtonStyle(
            color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
            },
            bgcolor={
                ft.ControlState.DEFAULT: theme[self.style_type].color,
                ft.ControlState.HOVERED: theme[self.style_type].color_light,
                ft.ControlState.DISABLED: ft.Colors.GREY_300,
                ft.ControlState.PRESSED: theme[self.style_type].color_accent,
            },
            # 点击样式
            overlay_color={
                ft.ControlState.DEFAULT: theme[self.style_type].color,
                ft.ControlState.HOVERED: theme[self.style_type].color_light,
                ft.ControlState.DISABLED: ft.Colors.GREY_300,
                ft.ControlState.PRESSED: theme[self.style_type].color_accent,
                # ft.ControlState.PRESSED: theme[self.style_type].color_light,
                # ft.ControlState.PRESSED: ft.Colors.RED,
            },
            shadow_color={
                ft.ControlState.DEFAULT: theme[self.style_type].color,
                ft.ControlState.HOVERED: theme[self.style_type].color_light,
                ft.ControlState.DISABLED: ft.Colors.GREY_300,
                ft.ControlState.PRESSED: theme[self.style_type].color_accent,
                # ft.ControlState.PRESSED: theme[self.style_type].color_light,
                # ft.ControlState.PRESSED: ft.Colors.RED,
            },
            surface_tint_color=None,
            elevation={
                ft.ControlState.DEFAULT: 0,
                ft.ControlState.PRESSED: 0,
                ft.ControlState.HOVERED: 0,
            },
            # animation_duration=500,
            # padding=ft.padding.only(left=2, right=2),
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(1, theme[self.style_type].color),
                ft.ControlState.HOVERED: ft.BorderSide(
                    1, theme[self.style_type].color_light
                ),
                ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.GREY),
                ft.ControlState.PRESSED: ft.BorderSide(
                    1, theme[self.style_type].color_accent
                ),
            },
        )
        if self.plain:
            self.style.bgcolor = {
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                # ft.ControlState.PRESSED: theme[self.style_type].color_light_max,
            }
            # 点击样式
            self.style.overlay_color = {
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                # ft.ControlState.PRESSED: theme[self.style_type].color_light_max,
                # ft.ControlState.PRESSED: theme[self.style_type].color_light,
                # ft.ControlState.PRESSED: ft.Colors.RED,
            }
            self.style.side = {
                ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREY),
                ft.ControlState.HOVERED: ft.BorderSide(
                    1, theme[self.style_type].color_light
                ),
                ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.GREY),
                ft.ControlState.PRESSED: ft.BorderSide(
                    2, theme[self.style_type].color_accent
                ),
            }
            self.style.color = {
                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                ft.ControlState.HOVERED: theme[self.style_type].color,
                ft.ControlState.PRESSED: ft.Colors.WHITE,
            }

        if self.shape_type == ButtonShapeType.rect:
            self.style.shape = ft.ContinuousRectangleBorder()
        elif self.shape_type == ButtonShapeType.round:
            self.style.shape = ft.RoundedRectangleBorder(
                radius=theme.border_radius.large
            )
        elif self.shape_type == ButtonShapeType.circle:
            self.style.shape = ft.StadiumBorder()

        if self.disabled:
            self.style.bgcolor = ft.Colors.GREY_300

    def update_content(self):
        # 组件逻辑：更新时获取 content
        if self.content is None and self.text is not None:
            self.content = ft.Text(self.text)

    def set_disabled(self, disabled: bool):
        self.disabled = disabled
        if disabled:
            pass
            # self.bgcolor = ButtonColors.button_disabled_background_color
            # self.color = ButtonColors.button_disabled_content_color
            # self.on_click = None
        else:
            pass
            # self.bgcolor = ButtonColors.button_backgound_color
            # self.color = ButtonColors.button_content_color
            # self.on_click = self.on_click
        self.update_content()


def main(page: ft.Page):
    def click_button(e):
        print("Button: Test: clicked button")

    page.window.width = 370
    page.window.always_on_top = True

    page.add(
        Button(content=ft.Text("test")),
        ft.Text("基本使用"),
        ft.Text("示例"),
        ft.Text("源码"),
        ft.Text("注意事项"),
        ft.Text("主按钮"),
        ft.Row(
            controls=[
                Button(text="color_button", style_type=StyleType.DEFAULT),
                Button(text="primary_button", style_type=StyleType.PRIMARY),
                Button(text="success_button", style_type=StyleType.SUCCESS),
                Button(text="info_button", style_type=StyleType.INFO),
                Button(text="warning_button", style_type=StyleType.WARNING),
                Button(text="error_button", style_type=StyleType.ERROR),
            ]
        ),
        ft.Text("次按钮，描边按钮，plain"),
        ft.Row(
            controls=[
                Button(text="color_button", style_type=StyleType.DEFAULT, plain=True),
                Button(text="primary_button", style_type=StyleType.PRIMARY, plain=True),
                Button(text="success_button", style_type=StyleType.SUCCESS, plain=True),
                Button(text="info_button", style_type=StyleType.INFO, plain=True),
                Button(text="warning_button", style_type=StyleType.WARNING, plain=True),
                Button(text="error_button", style_type=StyleType.ERROR, plain=True),
            ]
        ),
        ft.Text("rect-round-circle"),
        ft.Row(
            controls=[
                Button(
                    text="ButtonShapeType.rect",
                    style_type=StyleType.DEFAULT,
                    plain=True,
                    shape_type=ButtonShapeType.rect,
                ),
                Button(
                    text="ButtonShapeType.round",
                    style_type=StyleType.DEFAULT,
                    plain=True,
                    shape_type=ButtonShapeType.round,
                ),
                Button(
                    text="ButtonShapeType.circle",
                    style_type=StyleType.DEFAULT,
                    plain=True,
                    shape_type=ButtonShapeType.circle,
                ),
            ]
        ),
        ft.Text("disable"),
        ft.Row(
            controls=[
                Button(
                    text="color_button",
                    style_type=StyleType.DEFAULT,
                    plain=True,
                    disabled=True,
                ),
                Button(
                    text="primary_button",
                    style_type=StyleType.PRIMARY,
                    plain=True,
                    disabled=True,
                ),
                Button(
                    text="success_button",
                    style_type=StyleType.SUCCESS,
                    plain=True,
                    disabled=True,
                ),
                Button(
                    text="info_button",
                    style_type=StyleType.INFO,
                    plain=True,
                    disabled=True,
                ),
                Button(
                    text="warning_button",
                    style_type=StyleType.WARNING,
                    plain=True,
                    disabled=True,
                ),
                Button(
                    text="error_button",
                    style_type=StyleType.ERROR,
                    plain=True,
                    disabled=True,
                ),
            ]
        ),
        ft.Text("icon_button"),
        Button(text="icon_button", icon=ft.Icons.ADD),
    )


if __name__ == "__main__":
    ft.run(main)
