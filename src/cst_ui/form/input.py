import math
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Optional

import flet as ft
from flet.controls.material.textfield import (
    KeyboardType,
)

from cst_ui.basic.form_base import DEFAULT_FORM_HEIGHT, FormField, LayoutType
from cst_ui.basic.theme import theme

# from cstos.basic.form_base import FormField

# horizontal 水平布局
# vertical 垂直布局

ICON_SIZE = 16


@dataclass
class InputColors:
    hovered_outer_textinput_border_color: str
    hovered_inner_textinput_border_color: str
    default_outer_textinput_border_color: str
    default_inner_textinput_border_color: str
    text_field_focused_background_color: str
    text_field_border_color: str
    text_field_background_color: str
    text_color: str
    cursor_color: str

    @staticmethod
    def dark():
        return InputColors(
            hovered_outer_textinput_border_color="#1B2C58",
            hovered_inner_textinput_border_color="#1e55e2",
            default_outer_textinput_border_color="#26376b",
            default_inner_textinput_border_color="#494D5F",
            text_field_focused_background_color="#323741",
            text_field_border_color="#2b2f3b",
            text_field_background_color="#292f3a",
            text_color="#ffffff",
            cursor_color="#ffffff",
        )

    @staticmethod
    def light():
        return InputColors(
            hovered_outer_textinput_border_color="#d5e0fb",
            hovered_inner_textinput_border_color="#5786ff",
            default_outer_textinput_border_color="#d3d8e7",
            default_inner_textinput_border_color="#d3d8e7",
            text_field_focused_background_color="#ffffff",
            text_field_border_color=ft.Colors.GREY_400,
            text_field_background_color="#ffffff",
            text_color="#000000",
            cursor_color="#000000",
        )


@dataclass
class Input(ft.TextField):
    value: int | float | Decimal | str = ""
    # value: Union[int, float, Decimal, str] = ""
    # value: str = ""
    theme_mode = ft.ThemeMode.LIGHT
    keyboard_type: KeyboardType = KeyboardType.TEXT

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.colors = InputColors.light()
        # if self.is_dir_path:
        #     self.v_file_picker = ft.FilePicker(on_result=self.get_directory_result)
        #     self.suffix = ft.IconButton(
        #         icon=ft.Icons.FOLDER_OPEN, icon_size=18, on_click=lambda _: self.v_file_picker.get_directory_path()
        #     )
        if self.prefix and not self.suffix:
            content_padding = ft.Padding.only(left=10, right=5)
        elif self.suffix and not self.prefix:
            content_padding = ft.Padding.only(left=5, right=10)
        elif self.prefix and self.suffix:
            content_padding = ft.Padding.symmetric(horizontal=10)
        else:
            content_padding = ft.Padding.all(10)
        self.cursor_width = 1
        self.cursor_color = self.cursor_color or theme.color.primary
        self.colors = (
            InputColors.dark()
            if self.theme_mode == ft.ThemeMode.DARK
            else InputColors.light()
        )
        # self.focused_border_width = self.focused_border_width or ft.Border.all(1)
        self.focused_border_color = self.focused_border_color or theme.color.primary
        self.focused_bgcolor = self.focused_bgcolor or ft.Colors.RED
        self.border_radius = self.border_radius or ft.BorderRadius.all(7)
        self.filled = True
        self.color = self.colors.text_color
        self.expand_loose = True
        self.fill_color = (
            self.bgcolor or self.fill_color or self.colors.text_field_background_color
        )
        self.selection_color = ft.Colors.GREY_400
        self.hover_color = ft.Colors.BLUE_50
        self.content_padding = self.content_padding or content_padding

        self.text_size = theme.font_size
        self.default_value = self.value

        self.height = DEFAULT_FORM_HEIGHT if self.height is None else self.height
        # self.border_radius = theme.border_radius.large
        self.border = ft.InputBorder.OUTLINE if self.border is None else self.border
        self.border_width = 1
        self.cursor_width = 1
        self.cursor_color = self.colors.cursor_color

        self.border_color = (
            self.colors.text_field_border_color
            if self.border_color is None
            else self.border_color
        )

        return super().__post_init__(ref)

    @property
    def path(self) -> Optional[Path]:
        if self.value is None or len(str(self.value).strip()) == 0:
            return None
        else:
            return Path(str(self.value).strip().strip('"').strip("'"))

    # validate的定义放在value的后面，不然智能提示时老在value前面
    def validate(self):
        pass

    # def get_directory_result(self, event: ft.FilePickerResultEvent):
    #     self.value = event.path if event.path else 'CANCELADO'
    #     self.rst_dir_path = Path(self.value)
    #     self.update()
    #     # self.error_style = ft.TextStyle(
    #     # size=12,
    #     # )
    #     # self.on_focus = self_on_focus

    #     if self.is_dir_path:
    #         self.page.overlay.append(self.v_file_picker)
    #     return super().did_mount()

    # def v_content_on_focus(self, e):
    #     # self.is_focused = not self.is_focused

    #     if self.is_panel_visible:
    #         self.border = ft.Border.all(2, self.colors.hovered_outer_textinput_border_color)
    #         # self.inner_container.border = ft.Border.all(2, self.colors.hovered_inner_textinput_border_color)

    #     else:
    #         self.border = ft.Border.all(
    #             4,
    #             ft.Colors.with_opacity(0, self.colors.default_outer_textinput_border_color),
    #         )
    #         # self.inner_container.border = ft.Border.all(2, self.colors.default_inner_textinput_border_color)

    #     self.update()
    #     # return super().on_focus()

    # def did_mount(self):
    #     self.colors = InputColors.dark() if self.page.theme_mode == ft.ThemeMode.DARK else InputColors.light()
    #     self.update()

    def form_reset(self):
        self.value = self.default_value
        self.update()

    def textbox_changed(self, e):
        self.value = e.control.value


@dataclass
class NumberInput(Input):
    value: int | float | Decimal | str = 0
    min_value = -math.inf
    max_value = math.inf
    step = 0.01

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.width = self.width or 150
        self.text_align = self.text_align or ft.TextAlign.CENTER
        # self.value = self.value or 0
        if isinstance(self.value, int):
            self.step = 1
            # self.form_content_type = FormContentType.INT
        elif isinstance(self.value, float):
            self.step = 0.01
        else:
            raise ValueError("value must be int or float")

        self.height = 36
        # todo: attention: 图标较小时 数字上下会居中
        self.v_decrease = ft.Container(
            content=ft.Icon(name=ft.Icons.REMOVE, size=ICON_SIZE),
            border_radius=ft.BorderRadius(
                top_left=0, top_right=0, bottom_left=0, bottom_right=0
            ),
            on_click=self.handle_decrease_click,
            on_hover=self.handle_hover,
            height=self.height,
            width=30,
            alignment=ft.Alignment.CENTER,
        )
        self.v_increase_icon = ft.Icon(name=ft.Icons.ADD, size=ICON_SIZE)
        self.v_increase = ft.Container(
            content=self.v_increase_icon,
            border_radius=ft.BorderRadius(
                top_left=0, top_right=8, bottom_left=0, bottom_right=8
            ),
            on_click=self.handle_increase_click,
            on_hover=self.handle_hover,
            height=self.height,
            width=30,
            alignment=ft.Alignment.CENTER,
        )
        self.suffix = ft.Container(
            content=ft.Row(
                controls=[self.v_decrease, self.v_increase],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
                run_spacing=0,
            ),
            width=60,
            alignment=ft.Alignment.CENTER_RIGHT,
            height=self.height,
            offset=ft.Offset(x=0, y=0.05),
        )
        self.last_value = self.value
        self.content_padding = ft.Padding.only(left=5, right=0, top=0, bottom=10)
        self.text_vertical_align = ft.VerticalAlignment.START

        self.on_change = self._on_change
        return super().__post_init__(ref)

    def handle_hover(self, e):
        e.control.bgcolor = theme.color.primary if e.data == "true" else None
        e.control.content.color = ft.Colors.WHITE if e.data == "true" else None
        e.control.update()

    def _on_change(self, e):
        # if self.error_text is not None:
        #     self.height = 64
        # else:
        #     self.height = 36

        # try:
        #     # Convert the input to the specified numerical type
        #     if self.value.strip() != "":
        #         __value = float(self.value)
        # except ValueError:
        #     print("NumberInputValueError", self.value, self.last_value)
        #     self.value = self.last_value
        # else:
        #     self.last_value = self.value
        # self.update()
        return super().on_change

    def handle_decrease_click(self, e):
        self.value = Decimal(str(self.value)) - Decimal(str(self.step))
        self.update()

    def handle_increase_click(self, e):
        self.value = Decimal(str(self.value)) + Decimal(str(self.step))
        self.update()


def demo():
    def text_submit(e):
        if e.control.value != "1":
            e.control.error_text = "不是1"
        else:
            e.control.error_text = None
        e.control.update()

    a = Input()
    v_decrease = ft.Container(
        content=ft.Icon(name=ft.Icons.REMOVE),
        height=12,
        padding=0,
        margin=0,
    )
    v_increase = ft.Container(
        content=ft.Icon(name=ft.Icons.ADD, size=20),
        # margin=0,
    )
    # self.v_increase = ft.IconButton(
    #     icon=ft.Icons.ADD,
    #     style=self.icon_style,
    #     on_click=self.handle_increase_click,
    # )
    suffix = ft.Container(
        content=ft.Row(
            controls=[v_decrease, v_increase],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
            run_spacing=0,
        ),
        alignment=ft.Alignment.TOP_CENTER,
        width=80,
        padding=0,
        margin=0,
        # spacing=0,
        # run_spacing=0,
        height=10,
    )

    # def print_data(e):
    #     print(
    #         "NumberInput: ",
    #         number_input_1.value,
    #         number_input_2.value,
    #         number_input_3.value,
    #         number_input_4.value,
    #     )

    # FormField(
    #     label="带图标",
    #     form_content=,
    # ),
    # FormField(label="垂直布局", form_content=,
    # FormField(label="有默认值", form_content=,
    # FormField(
    #     label="不可选中", form_content=, layout_type=LayoutType.vertical
    # ),
    # FormField(
    # label="不可选中",
    #     form_content=,
    #     bgcolor=ft.Colors.RED,
    #     layout_type=LayoutType.vertical,
    #     on_change=_on_change,
    # ),
    # ]
    # )
    #     number_input_1 := NumberInput(
    #     "年龄",
    #     value=18,
    #     height=500,
    # ),
    number_input_2 = NumberInput(value=180.00)
    number_input_3 = NumberInput()
    number_input_4 = NumberInput(value=140)
    # ft.Button("查看数据", on_click=print_data),
    return ft.Column(
        controls=[
            FormField(label="身高", label_width=80, form_content=number_input_2),
            FormField(label="体重", label_width=80, form_content=number_input_4),
            NumberInput(
                # "年龄",
                value=18,
                height=500,
            ),
            FormField(label="帐号", label_width=80, form_content=Input()),
            FormField(
                label="密码",
                label_width=80,
                is_required=True,
                form_content=Input(
                    value="123456",
                    password=True,
                    can_reveal_password=True,
                ),
            ),
            FormField(
                label="帐号",
                label_width=80,
                form_content=Input(
                    "手机号",
                    keyboard_type=ft.KeyboardType.PHONE,
                ),
                is_required=True,
                layout_type=LayoutType.VERTICAL,
            ),
            FormField(
                label="帐号",
                label_width=80,
                form_content=Input(value="默认值"),
            ),
            FormField(
                label="帐号",
                label_width=80,
                form_content=Input(on_submit=text_submit),
            ),
            FormField(
                label="帐号",
                label_width=80,
                form_content=Input(),
            ),
            # is_dir_path=True
            FormField(
                label="帐号",
                label_width=80,
                form_content=Input(value="345", disabled=True),
            ),
            FormField(
                label="多行文本",
                label_width=80,
                form_content=Input(value="345", multiline=True),
            ),
            FormField(
                label="test",
                label_width=80,
                form_content=Input(value="345", height=200, multiline=True),
            ),
            FormField(
                label="test",
                label_width=80,
                form_content=Input(value="345", prefix_icon=ft.Icons.DATASET),
            ),
            FormField(
                label="test",
                label_width=80,
                form_content=Input(
                    value="345", fill_color=ft.Colors.RED, disabled=True
                ),
            ),
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
