'''表单基本组件'''

import flet as ft
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypedDict, Unpack, Union
from cst_ui.basic.theme import theme, LayoutType


class FormValueType(Enum):
    INT = 'INT'
    FLOAT = 'FLOAT'
    STR = 'STR'
    PATH = 'PATH'
    BOOL = 'BOOL'


class FormFieldTypedDict(TypedDict):
    label: Optional[str]
    label_width: Optional[int]
    is_required: bool
    layout_type: LayoutType
    theme_mode: ft.ThemeMode
    wrap: bool
    form_value_type: FormValueType


DEFAULT_FORM_HEIGHT = 36


class FormLabel(ft.Row):
    def __init__(self, label_value, is_required=False, **kwargs):
        super().__init__(**kwargs)

        self.is_required = is_required
        if label_value is None:
            self.v_label = ft.Text(value='')
        else:
            self.v_label = ft.Text(value=f'{label_value}：')
        self.spacing = 0
        self.alignment = ft.MainAxisAlignment.END
        if self.is_required:
            self.controls = [ft.Text(value='*', color=ft.Colors.RED), self.v_label]
        else:
            self.controls = [self.v_label]
        self.height = DEFAULT_FORM_HEIGHT


class FormField(ft.Container):
    def __init__(
        self,
        label: Optional[str],
        label_width: Optional[int] = 0,
        is_required: bool = False,
        layout_type: LayoutType = LayoutType.HORIZONTAL,
        theme_mode: ft.ThemeMode = ft.ThemeMode.SYSTEM,
        wrap: bool = False,
        form_value_type: FormValueType = FormValueType.STR,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.label = label
        self.label_width = label_width
        self.is_required = is_required
        self.layout_type = layout_type
        self.theme_mode = theme_mode
        self.wrap = wrap
        self.form_value_type = form_value_type

        # self.padding = 0
        # self.margin = 0
        self.alignment = ft.Alignment.TOP_LEFT
        self.v_content = ft.Text('占位内容')

    def set_content(self, v_contnet):
        self.v_label = FormLabel(label_value=self.label, is_required=self.is_required, width=self.label_width)
        if self.layout_type == LayoutType.HORIZONTAL:
            self.v_label.alignment = ft.MainAxisAlignment.END

            self.content = ft.Row(
                controls=[
                    self.v_label,
                    self.v_content,
                ],
                # 当不适合单行时，新增行
                # wrap=self.wrap,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        elif self.layout_type == LayoutType.VERTICAL:
            self.v_label.alignment = ft.MainAxisAlignment.START
            self.content = ft.Column(
                controls=[
                    self.v_label,
                    self.v_content,
                ],
                # 当不适合单行时，新增行
                wrap=self.wrap,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )

    @property
    def value(self) -> Union[int, float, Path, str, bool, None]:
        tmp_value = self.v_content.__dict__.get("value", None)
        if hasattr(self.v_content, 'form_value_type') and tmp_value is not None:
            if self.form_value_type == FormValueType.INT:
                return int(tmp_value)
            elif self.form_value_type == FormValueType.FLOAT:
                return float(tmp_value)
            elif self.form_value_type == FormValueType.PATH:
                return Path(tmp_value)
            elif self.form_value_type == FormValueType.STR:
                return str(tmp_value)
            elif self.form_value_type == FormValueType.BOOL:
                return bool(tmp_value)
            else:
                return tmp_value
        else:
            return tmp_value

    @value.setter
    def value(self, value):
        self.v_content.value = value
