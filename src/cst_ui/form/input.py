import math
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Optional, Union

import flet as ft
from flet.controls.material.textfield import (
    AutofillHint,
    Brightness,
    ClipBehavior,
    ColorValue,
    ControlEventHandler,
    InputFilter,
    KeyboardType,
    MouseCursor,
    Number,
    PaddingValue,
    StrutStyle,
    TextAlign,
    TextCapitalization,
    TextField,
)

# from jui.basic.form_base import FormField

# horizontal 水平布局
# vertical 垂直布局

ICON_SIZE = 16

from cst_ui.basic.form_base import DEFAULT_FORM_HEIGHT, FormField, LayoutType
from cst_ui.basic.theme import theme


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
    """
    A text field lets the user enter text, either with hardware keyboard or with an
    onscreen keyboard.
    """

    value: int | float | Decimal | str = ""
    # value: Union[int, float, Decimal, str] = ""
    # value: str = ""
    """
    Current value of the TextField.
    """
    theme_mode = ft.ThemeMode.LIGHT
    keyboard_type: KeyboardType = KeyboardType.TEXT
    """
    The type of keyboard to use for editing the text. The property value is
    [`KeyboardType`][flet.KeyboardType] and defaults
    to `KeyboardType.TEXT`.
    """

    multiline: bool = False
    """
    `True` if TextField can contain multiple lines of text.
    """

    min_lines: Optional[int] = None
    """
    The minimum number of lines to occupy when the content spans fewer lines.

    This affects the height of the field itself and does not limit the number of lines
    that can be entered into the field.

    Defaults to `1`.
    """

    max_lines: Optional[int] = None
    """
    The maximum number of lines to show at one time, wrapping if necessary.

    This affects the height of the field itself and does not limit the number of lines
    that can be entered into the field.

    If this is `1` (the default), the text will not wrap, but will scroll horizontally
    instead.
    """

    max_length: Optional[int] = None
    """
    Limits a maximum number of characters that can be entered into TextField.
    """

    password: bool = False
    """
    Whether to hide the text being edited.

    Defaults to `False`.
    """

    can_reveal_password: bool = False
    """
    Displays a toggle icon button that allows revealing the entered password. Is shown
    if both `password` and `can_reveal_password` are `True`.

    The icon is displayed in the same location as `suffix` and in case both
    `can_reveal_password`/`password` and `suffix` are provided, then the `suffix` is
    not shown.
    """

    read_only: bool = False
    """
    Whether the text can be changed.

    When this is set to `True`, the text cannot be modified by any shortcut or keyboard
    operation. The text is still selectable.

    Defaults to `False`.
    """

    shift_enter: bool = False
    """
    Changes the behavior of `Enter` button in `multiline` TextField to be chat-like,
    i.e. new line can be added with `Shift`+`Enter` and pressing just `Enter` fires
    `on_submit` event.
    """

    text_align: Optional[TextAlign] = None
    """
    How the text should be aligned horizontally.

    Defaults to `TextAlign.LEFT`.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    capitalization: Optional[TextCapitalization] = None
    """
    Enables automatic on-the-fly capitalization of entered text.

    Defaults to `TextCapitalization.NONE`.
    """

    autocorrect: bool = True
    """
    Whether to enable autocorrection.

    Defaults to `True`.
    """

    enable_suggestions: bool = True
    """
    Whether to show input suggestions as the user types.

    This flag only affects Android. On iOS, suggestions are tied directly to
    `autocorrect`, so that suggestions are only shown when `autocorrect` is `True`.
    On Android autocorrection and suggestion are controlled separately.

    Defaults to `True`.
    """

    smart_dashes_type: bool = True
    """
    Whether to allow the platform to automatically format dashes.

    This flag only affects iOS versions 11 and above. As an example of what this does,
    two consecutive hyphen characters will be automatically replaced with one en dash,
    and three consecutive hyphens will become one em dash.

    Defaults to `True`.
    """

    smart_quotes_type: bool = True
    """
    Whether to allow the platform to automatically format quotes.

    This flag only affects iOS. As an example of what this does, a standard vertical
    double quote character will be automatically replaced by a left or right double
    quote depending on its position in a word.

    Defaults to `True`.
    """

    show_cursor: bool = True
    """
    Whether the field's cursor is to be shown.

    Defaults to `True`.
    """

    cursor_color: Optional[ColorValue] = None
    """
    The color of TextField cursor.
    """

    cursor_error_color: Optional[ColorValue] = None
    """
    TBD
    """

    cursor_width: Number = 2.0
    """
    Sets cursor width.
    """

    cursor_height: Optional[Number] = None
    """
    Sets cursor height.
    """

    cursor_radius: Optional[Number] = None
    """
    Sets cursor radius.
    """

    selection_color: Optional[ColorValue] = None
    """
    The color of TextField selection.
    """

    input_filter: Optional[InputFilter] = None
    """
    Provides as-you-type filtering/validation.

    Similar to the `on_change` callback, the input filters are not applied when the
    content of the field is changed programmatically.
    """

    obscuring_character: str = "•"
    """
    TBD
    """

    enable_interactive_selection: bool = True
    """
    TBD
    """

    enable_ime_personalized_learning: bool = True
    """
    TBD
    """

    can_request_focus: bool = True
    """
    TBD
    """

    ignore_pointers: bool = False
    """
    TBD
    """

    enable_stylus_handwriting: bool = True
    """
    TBD
    """

    animate_cursor_opacity: Optional[bool] = None
    """
    TBD
    """

    always_call_on_tap: bool = False
    """
    TBD
    """

    scroll_padding: PaddingValue = 20
    """
    TBD
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    TBD
    """

    keyboard_brightness: Optional[Brightness] = None
    """
    TBD
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    TBD
    """

    strut_style: Optional[StrutStyle] = None
    """
    TBD
    """

    autofill_hints: Optional[Union[AutofillHint, list[AutofillHint]]] = None
    """
    Helps the autofill service identify the type of this text input.

    More information [here](https://api.flutter.dev/flutter/material/TextField/autofillHints.html).
    """

    on_change: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when the typed input for the TextField has changed.
    """

    on_click: Optional[ControlEventHandler["TextField"]] = None
    """
    TBD
    """

    on_submit: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when user presses ENTER while focus is on TextField.
    """

    on_focus: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["TextField"]] = None
    """
    Called when the control has lost focus.
    """

    on_tap_outside: Optional[ControlEventHandler["TextField"]] = None
    """
    TBD
    """

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

    # def did_mount(self):
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
        print("--------", self.value)
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
        self.content_padding = ft.padding.only(left=5, right=0, top=0, bottom=10)
        self.text_vertical_align = ft.VerticalAlignment.START

        self.on_change = self._on_change
        return super().__post_init__(ref)

    # def __init__(
    #     self,
    #     label: Optional[str] = None,
    #     label_width: Optional[int] = None,
    #     is_required=False,
    #     layout_type=LayoutType.horizontal,
    #     theme_mode=ft.ThemeMode.LIGHT,
    #     wrap=False,
    #     **kwargs: Unpack[TextFieldTypedDict],
    # ):
    #     self.form_content_type = FormContentType.FLOAT

    #     self.v_content.height = 36

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
    # number_input_2 := NumberInput("身高", value=180.00),
    # number_input_3 := NumberInput("身高"),
    # number_input_4 := NumberInput("体重", value=140),
    # ft.Button("查看数据", on_click=print_data),
    return ft.Column(
        controls=[
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
