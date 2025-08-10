"""主题相关配置"""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

import flet as ft

# --- 2、字体 ---
FONT_DIR = Path(list(Path(__file__).parents)[1], "data/fonts").resolve()


class Font:
    name: str
    path: str

    def __init__(self, path: str):
        self.name = Path(path).stem
        self.path = path

    def __repr__(self):
        return f"{self.name}, {self.path}"


fonts = [Font(str(Path(FONT_DIR, "AlibabaPuHuiTi-3-55-Regular.otf"))), Font(str(Path(FONT_DIR, "Consolas.ttf")))]

FONTS = dict(zip([font.name for font in fonts], [font.path for font in fonts]))


# 1、颜色
@dataclass
class FeedbackStyle:
    icon: str
    color: str
    color_light: str
    color_accent: str
    # heavy: str
    # heavy_max: str


primary_color_style = FeedbackStyle(
    icon=ft.Icons.MESSAGE, color=ft.Colors.BLUE, color_light=ft.Colors.BLUE_300, color_accent=ft.Colors.BLUE_800
)
success_color_style = FeedbackStyle(
    icon=ft.Icons.DONE, color=ft.Colors.GREEN, color_light=ft.Colors.GREEN_300, color_accent=ft.Colors.GREEN_800
)
warning_color_style = FeedbackStyle(
    icon=ft.Icons.WARNING_ROUNDED,
    color=ft.Colors.AMBER,
    color_light=ft.Colors.AMBER_300,
    color_accent=ft.Colors.AMBER_800,
)
error_color_style = FeedbackStyle(
    icon=ft.Icons.CLOSE, color=ft.Colors.RED, color_light=ft.Colors.RED_300, color_accent=ft.Colors.RED_800
)
info_color_style = FeedbackStyle(
    icon=ft.Icons.CLOSE, color=ft.Colors.GREY, color_light=ft.Colors.GREY_300, color_accent=ft.Colors.GREY_800
)


@unique
class StyleType(Enum):
    DEFAULT = 0  # 默认灰色
    PRIMARY = 1  # 蓝色，#007bff
    INFO = 2  # 浅蓝色：#17a2b8
    SUCCESS = 3  # 绿色：#28a745
    WARNING = 4  # 黄色：#ffc107
    ERROR = 5  # 红色：#dc3545
    # SECONDARY   # 次要：#6c757d


# DEBUG
# CRITICAL
# 2、尺寸大小
# small_switch = create_custom_switch(0.5, "小号开关")
# normal_switch = create_custom_switch(0.8, "正常大小开关")
# large_switch = create_custom_switch(1.1, "大号开关")
# extra_large_switch = create_custom_switch(1.4, "特大号开关")
@dataclass
class BorderRadius:
    # https://fluent2.microsoft.design/shapes
    # Navigation bars, tab bars
    none: int = 0
    # Small badges
    small: int = 2
    # Buttons, dropdown
    medium: int = 4
    # Large buttons
    large: int = 8
    # Button sheets, popovers
    x_large: int = 12


class StrokeThickness(Enum):
    # https://fluent2.microsoft.design/shapes
    # web
    thin = 1
    thick = 2
    thicker = 3
    thickest = 4

    thin_mobile = 1
    thick_mobile = 2
    thicker_mobile = 4
    thickest_mobile = 6


# --- 列间距 ---
@dataclass
class Spacing:
    same_control: int = 8
    different_control: int = 12
    none = 0
    XXS = 2
    XS = 4
    SNudge = 6
    S = 8
    MNudge = 10
    M = 12
    L = 16
    XL = 20
    XXL = 24
    XXXL = 32


class LayoutType(Enum):
    # 表单的水平、竖直排布
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

    # xs
    # s
    # m
    # l


class SizeType(Enum):
    small = "small"
    medium = "medium"
    large = "large"
    x_large = "x_large"
    xx_large = "xx_large"
    xxx_large = "xxx_large"


@dataclass
class Color:
    """基于 UI 稿"""

    background = ft.Colors.GREY_400
    primary = primary_color_style.color
    info = info_color_style.color
    success = success_color_style.color
    warning = warning_color_style.color
    error = error_color_style.color


class Theme:
    def __init__(self) -> None:
        # 1、颜色：色彩规范
        self.color: Color = Color()
        self.bgcolor: str = "#2e2f3e"

        # 2、尺寸：大小规范
        self.font_size = 14
        self.light_theme_text_color = ft.Colors.BLACK
        self.dark_theme_text_color = ft.Colors.WHITE
        # self.color: Color = dataclasses.field(default=Color)
        self.text_default_color: str = ft.Colors.BLACK
        self.text_active_color: str = "#353535"
        self.text_disabled_color: str = "#666"

        self.text_size = 16
        self.mask_background_color: str = "#666"

        self.border_radius = BorderRadius()
        # self.border=
        self.border_width = 1
        self.border_color = "#666"
        self.border_active_color = "#666"
        self.card_border_color = "#666"

        self.form_content_height = 40
        # 3、字体

        # 4、圆角

        # 5、阴影
        self.shadow = ft.BoxShadow(
            spread_radius=0.2,
            blur_radius=10,
            color=ft.Colors.GREY_300,
            offset=ft.Offset(0, 2.5),
            # blur_style=ft.ShadowBlurStyle.SOLID,
        )

        # 9、应用主题
        self.ft_theme = ft.Theme(
            # color_scheme_seed=self.color.primary,  # 用于算法推导主题颜色余下部分的种子颜色
            # color_scheme=ft.ColorScheme(    # 自定义从color_scheme_seed派生的material颜色方案
            # ),
            text_theme=ft.TextTheme(),  # 与卡片和画布颜色形成对比的文本样式
            primary_text_theme=ft.TextTheme(),  # 与主色调形成对比的文本主题
            scrollbar_theme=ft.ScrollbarTheme(
                thickness=4,
                radius=10,
                main_axis_margin=5,
                cross_axis_margin=-10,
                track_visibility=False,
                thumb_visibility=False,
                track_color={ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT},
                thumb_color={
                    ft.ControlState.HOVERED: ft.Colors.TRANSPARENT,
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                },
            ),
            font_family="AlibabaPuHuiTi-3-55-Regular",  # 所有UI元素的基准字体
            use_material3=True,  # use material 2: this setting is mainly for the app-bar's elevation
            # visual_density=ft.ThemeVisualDensity.ADAPTIVEPLATFORMDENSITY,
            page_transitions=ft.PageTransitionsTheme(  # Removing animation on route change.
                android=ft.PageTransitionTheme.NONE,
                ios=ft.PageTransitionTheme.NONE,
                macos=ft.PageTransitionTheme.NONE,
                windows=ft.PageTransitionTheme.NONE,
                linux=ft.PageTransitionTheme.NONE,
            ),
            radio_theme=ft.RadioTheme(fill_color=ft.Colors.RED),
        )

    def __getitem__(self, key: StyleType) -> FeedbackStyle:
        if key == StyleType.INFO:
            return info_color_style
        elif key == StyleType.SUCCESS:
            return success_color_style
        elif key == StyleType.WARNING:
            return warning_color_style
        elif key == StyleType.ERROR:
            return error_color_style
        elif key == StyleType.DEFAULT:
            return primary_color_style
        elif key == StyleType.PRIMARY:
            return primary_color_style
        else:
            return primary_color_style

    def set_theme(self, page: ft.Page, on_resize: Callable):
        # 设置字体
        page.fonts = FONTS
        # 设置主题
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = theme.ft_theme
        page.bgcolor = Color.background
        # page.vertical_alignment = ft.MainAxisAlignment.CENTER
        # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        page.scroll = ft.ScrollMode.AUTO
        page.spacing = 0
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        page.window.resizable = True  # 页面缩放
        # page.on_resize = lambda _: on_page_resize(_, on_resize)
        # page.window.full_screen = True
        # page.window_maximizable = False
        # page.window_always_on_top = True
        # 最大化
        page.window.maximizable = True
        page.window.maximized = True
        # page.window.center()
        # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # page.vertical_alignment = ft.MainAxisAlignment.START
        page.window.width = 800
        page.window.height = 300

    # def switch(self, theme_mode: ft.ThemeMode):
    #     self.page.client_storage.set("theme_mode", self.mode)
    #     self.page.theme_mode = self.mode[0]
    #     self.label = self.mode[1]
    #     self.page.update()


theme = Theme()
