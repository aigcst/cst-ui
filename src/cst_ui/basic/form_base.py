"""表单基本组件"""

from enum import Enum
from pathlib import Path
from typing import Any, Optional, TypedDict, Union

import flet as ft

from cst_ui.basic.theme import LayoutType


class FormValueType(Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    STR = "STR"
    PATH = "PATH"
    BOOL = "BOOL"


class FormFieldTypedDict(TypedDict):
    label: Optional[str]
    label_width: Optional[int]
    is_required: bool
    layout_type: LayoutType
    theme_mode: ft.ThemeMode
    wrap: bool
    form_value_type: FormValueType


DEFAULT_FORM_HEIGHT = 36


class Label(ft.Text):
    def __init__(self, is_required=False, **kwargs):
        super().__init__(**kwargs)
        self.is_required = is_required
        if (
            self.value is not None
            and (not self.value.endswith(":"))
            and (not self.value.endswith("："))
        ):
            self.value = self.value + "："
        self.spacing = 0
        self.alignment = ft.MainAxisAlignment.END
        if self.is_required:
            self.spans = [
                ft.TextSpan(text="*", style=ft.TextStyle(color=ft.Colors.RED)),
                ft.TextSpan(self.value),
            ]
        else:
            self.spans = [ft.TextSpan(text=self.value)]
        # TODO: value 与 spans 同时存在时，都会显示
        self.value = ""

        # self.height = DEFAULT_FORM_HEIGHT


class FormField(ft.Container):
    def __init__(
        self,
        label: Optional[str],
        label_width: Optional[int] = 200,
        form_content: Any = ft.Text("占位内容"),
        is_required: bool = False,
        layout_type: LayoutType = LayoutType.HORIZONTAL,
        theme_mode: ft.ThemeMode = ft.ThemeMode.SYSTEM,
        wrap: bool = False,
        form_value_type: FormValueType = FormValueType.STR,
        **kwargs,
    ):
        self._form_content = form_content
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
        self.set_content(content=self._form_content)

    def set_content(self, content):
        self.v_label = Label(
            value=self.label, is_required=self.is_required, width=self.label_width
        )
        # self.v_label = ft.Text(spans=[ft.TextSpan(text=self.label)])
        if self.layout_type == LayoutType.HORIZONTAL:
            self.v_label.alignment = ft.MainAxisAlignment.END
            self.content = ft.Row(
                controls=[self.v_label, content],
                # 当不适合单行时，新增行
                # wrap=self.wrap,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        elif self.layout_type == LayoutType.VERTICAL:
            self.v_label.alignment = ft.MainAxisAlignment.START
            self.content = ft.Column(
                controls=[self.v_label, content],
                # 当不适合单行时，新增行
                wrap=self.wrap,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )

    @property
    def form_content(self):
        return self._form_content

    @form_content.setter
    def form_content(self, content):
        self.set_content(content=content)

    @property
    def value(self) -> Union[int, float, Path, str, bool, None]:
        tmp_value = self.content.__dict__.get("value", None)
        if hasattr(self.content, "form_value_type") and tmp_value is not None:
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
        self.form_content.value = value
