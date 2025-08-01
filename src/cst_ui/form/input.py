import flet as ft
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypedDict, Unpack, Union
from cst_ui.basic.theme import theme, LayoutType
from cst_ui.basic.form_base import FormField, FormValueType, FormLabel, DEFAULT_FORM_HEIGHT


from flet.controls.material.textfield import (
    KeyboardType,
    TextAlign,
    TextCapitalization,
    OptionalColorValue,
    Number,
    OptionalNumber,
    InputFilter,
    PaddingValue,
    ClipBehavior,
    Brightness,
    MouseCursor,
    StrutStyle,
    AutofillHint,
    OptionalControlEventHandler,
    TextField,
)


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


class Input(FormField):
    def __init__(
        self,
        value: str = '',
        # 自带参数，提到前面
        label: Optional[str] = None,
        label_width: Optional[int] = None,
        is_required=False,
        layout_type=LayoutType.HORIZONTAL,
        theme_mode=ft.ThemeMode.LIGHT,
        wrap=False,
        form_value_type=FormValueType.STR,
        is_file_path=False,
        is_dir_path=False,
        # START: ft.TextField
        keyboard_type: KeyboardType = KeyboardType.TEXT,
        multiline: bool = False,
        min_lines: Optional[int] = None,
        max_lines: Optional[int] = None,
        max_length: Optional[int] = None,
        password: bool = False,
        can_reveal_password: bool = False,
        read_only: bool = False,
        shift_enter: bool = False,
        text_align: Optional[TextAlign] = None,
        autofocus: bool = False,
        capitalization: Optional[TextCapitalization] = None,
        autocorrect: bool = True,
        enable_suggestions: bool = True,
        smart_dashes_type: bool = True,
        smart_quotes_type: bool = True,
        show_cursor: bool = True,
        cursor_color: OptionalColorValue = None,
        cursor_error_color: OptionalColorValue = None,
        cursor_width: Number = 2.0,
        cursor_height: OptionalNumber = None,
        cursor_radius: OptionalNumber = None,
        selection_color: OptionalColorValue = None,
        input_filter: Optional[InputFilter] = None,
        obscuring_character: str = "•",
        enable_interactive_selection: bool = True,
        enable_ime_personalized_learning: bool = True,
        can_request_focus: bool = True,
        ignore_pointers: bool = False,
        enable_stylus_handwriting: bool = True,
        animate_cursor_opacity: Optional[bool] = None,
        always_call_on_tap: bool = False,
        scroll_padding: PaddingValue = 20,
        clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE,
        keyboard_brightness: Optional[Brightness] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        strut_style: Optional[StrutStyle] = None,
        autofill_hints: Optional[Union[AutofillHint, list[AutofillHint]]] = None,
        on_change: OptionalControlEventHandler["TextField"] = None,
        on_click: OptionalControlEventHandler["TextField"] = None,
        on_submit: OptionalControlEventHandler["TextField"] = None,
        on_focus: OptionalControlEventHandler["TextField"] = None,
        on_blur: OptionalControlEventHandler["TextField"] = None,
        on_tap_outside: OptionalControlEventHandler["TextField"] = None,
        **kwargs,
    ):

        super().__init__(
            label=label,
            label_width=label_width,
            is_required=is_required,
            layout_type=layout_type,
            theme_mode=theme_mode,
            wrap=wrap,
            form_value_type=form_value_type,
            **kwargs,
        )
        self.v_content = ft.TextField(
            keyboard_type=keyboard_type,
            multiline=multiline,
            min_lines=min_lines,
            max_lines=max_lines,
            max_length=max_length,
            password=password,
            can_reveal_password=can_reveal_password,
            read_only=read_only,
            shift_enter=shift_enter,
            text_align=text_align,
            autofocus=autofocus,
            capitalization=capitalization,
            autocorrect=autocorrect,
            enable_suggestions=enable_suggestions,
            smart_dashes_type=smart_dashes_type,
            smart_quotes_type=smart_quotes_type,
            show_cursor=show_cursor,
            cursor_color=cursor_color,
            cursor_error_color=cursor_error_color,
            cursor_width=cursor_width,
            cursor_height=cursor_height,
            cursor_radius=cursor_radius,
            selection_color=selection_color,
            input_filter=input_filter,
            obscuring_character=obscuring_character,
            enable_interactive_selection=enable_interactive_selection,
            enable_ime_personalized_learning=enable_ime_personalized_learning,
            can_request_focus=can_request_focus,
            ignore_pointers=ignore_pointers,
            enable_stylus_handwriting=enable_stylus_handwriting,
            animate_cursor_opacity=animate_cursor_opacity,
            always_call_on_tap=always_call_on_tap,
            scroll_padding=scroll_padding,
            clip_behavior=clip_behavior,
            keyboard_brightness=keyboard_brightness,
            mouse_cursor=mouse_cursor,
            strut_style=strut_style,
            autofill_hints=autofill_hints,
            on_change=on_change,
            on_click=on_click,
            on_submit=on_submit,
            on_focus=on_focus,
            on_blur=on_blur,
            on_tap_outside=on_tap_outside,
            **kwargs,
        )
        self.set_content(self.v_content)
        self.colors = InputColors.light()
        self.is_dir_path = is_dir_path
        # if self.is_dir_path:
        #     self.v_file_picker = ft.FilePicker(on_result=self.get_directory_result)
        #     self.v_content.suffix = ft.IconButton(
        #         icon=ft.Icons.FOLDER_OPEN, icon_size=18, on_click=lambda _: self.v_file_picker.get_directory_path()
        #     )
        if self.v_content.prefix and not self.v_content.suffix:
            content_padding = ft.padding.only(left=10, right=5)
        elif self.v_content.suffix and not self.v_content.prefix:
            content_padding = ft.padding.only(left=5, right=10)
        elif self.v_content.prefix and self.v_content.suffix:
            content_padding = ft.padding.symmetric(horizontal=10)
        else:
            content_padding = ft.padding.all(10)
        self.v_content.cursor_width = 1
        self.v_content.cursor_color = self.v_content.cursor_color or theme.color.primary
        self.colors = InputColors.dark() if theme_mode == ft.ThemeMode.DARK else InputColors.light()
        # self.v_content.focused_border_width = self.v_content.focused_border_width or ft.border.all(1)
        self.v_content.focused_border_color = self.v_content.focused_border_color or theme.color.primary
        self.v_content.focused_bgcolor = self.v_content.focused_bgcolor or ft.Colors.RED
        self.v_content.border_radius = self.v_content.border_radius or ft.border_radius.all(7)
        self.v_content.filled = True
        self.v_content.color = self.colors.text_color
        self.v_content.expand_loose = True
        self.v_content.fill_color = (
            self.v_content.bgcolor or self.v_content.fill_color or self.colors.text_field_background_color
        )
        self.v_content.selection_color = ft.Colors.GREY_400
        self.v_content.hover_color = ft.Colors.BLUE_50
        self.v_content.content_padding = self.v_content.content_padding or content_padding

        self.v_content.text_size = theme.font_size
        self.value = value
        self.default_value = self.value

        self.v_content.height = DEFAULT_FORM_HEIGHT if self.v_content.height is None else self.v_content.height
        # self.v_content.border_radius = theme.border_radius.large
        self.v_content.border = ft.InputBorder.OUTLINE if self.v_content.border is None else self.v_content.border
        self.v_content.border_width = 1
        self.v_content.cursor_width = 1
        self.v_content.cursor_color = self.colors.cursor_color

        self.v_content.border_color = (
            self.colors.text_field_border_color if self.v_content.border_color is None else self.v_content.border_color
        )

    @property
    def path(self) -> Optional[Path]:
        if self.value is None or len(self.value.strip()) == 0:
            return None
        else:
            return Path(self.value.strip().strip('"').strip("'"))

    # value
    @property
    def value(self) -> Optional[str]:
        return self.v_content.value

    @value.setter
    def value(self, value: Optional[str]):
        if value is not None:
            self.v_content.value = value

    # validate的定义放在value的后面，不然智能提示时老在value前面
    def validate(self):
        pass

    # def get_directory_result(self, event: ft.FilePickerResultEvent):
    #     self.v_content.value = event.path if event.path else 'CANCELADO'
    #     self.rst_dir_path = Path(self.v_content.value)
    #     self.v_content.update()
    #     # self.v_content.error_style = ft.TextStyle(
    #     # size=12,
    #     # )
    #     # self.v_content.on_focus = self.v_content_on_focus

    # def did_mount(self):
    #     if self.is_dir_path:
    #         self.page.overlay.append(self.v_file_picker)
    #     return super().did_mount()

    # def v_content_on_focus(self, e):
    #     # self.v_content.is_focused = not self.v_content.is_focused

    #     if self.v_content.is_panel_visible:
    #         self.v_content.border = ft.border.all(2, self.colors.hovered_outer_textinput_border_color)
    #         # self.inner_container.border = ft.border.all(2, self.colors.hovered_inner_textinput_border_color)

    #     else:
    #         self.v_content.border = ft.border.all(
    #             4,
    #             ft.Colors.with_opacity(0, self.colors.default_outer_textinput_border_color),
    #         )
    #         # self.inner_container.border = ft.border.all(2, self.colors.default_inner_textinput_border_color)

    #     self.v_content.update()
    #     # return super().on_focus()

    def paragraph(self):
        return

    # def did_mount(self):
    #     self.colors = InputColors.dark() if self.page.theme_mode == ft.ThemeMode.DARK else InputColors.light()
    #     self.update()

    def save(self):
        pass

    def form_reset(self):
        self.value = self.default_value
        self.update()

    def textbox_changed(self, e):
        self.value = e.control.value

    # on_click
    # @property
    # def on_click(self):
    #     return self.v_content.on_click

    # @on_click.setter
    # def on_click(self, handler):
    #     self.v_content: ft.TextField
    #     self.v_content.on_click = handler


def get_ui_view():
    def text_submit(e):
        if e.control.value != '1':
            e.control.error_text = '不是1'
        else:
            e.control.error_text = None
        e.control.update()

    return ft.Column(
        controls=[
            Input(
                label='帐号',
                # is_required=True,
                label_width=200,
            ),
            Input(
                # '密码',
                value='123456',
                password=True,
                can_reveal_password=True,
                is_required=False,
                label_width=200,
            ),
            Input(
                '手机号',
                is_required=True,
                layout_type=LayoutType.VERTICAL,
                label_width=200,
                keyboard_type=ft.KeyboardType.PHONE,
            ),
            Input(value='默认值'),
            Input(on_submit=text_submit),
            # Input(value="121233", prefix_icon=ft.Icons.DATASET),
            Input(is_dir_path=True),
            Input(value="345", disabled=True),
            # Input(value="123", fill_color=ft.Colors.RED, disabled=True),
            # Input(fill_color=ft.Colors.RED),
            Input(label='多行文本', label_width=200, value="345", multiline=True),
            # , multiline=True, height=300, width=500),
            # NumberInput(label='', value=10),
            Input(label='test', value="345", height=200, multiline=True),
        ]
    )


def main(page: ft.Page):
    page.title = "Test"
    page.scroll = ft.ScrollMode.ALWAYS
    # page.theme_mode = "dark"
    page.add(get_ui_view())
    page.update()


if __name__ == '__main__':
    ft.app(target=main)
