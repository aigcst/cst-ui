from dataclasses import dataclass
from typing import Any, Callable, Optional

import flet as ft

import cst_ui as ui
from cst_ui.basic.theme import StyleType, theme
from cst_ui.form.input import Input

# 常量定义
ICON_WIDTH = 28
ICON_HEIGHT = 28
ICON_DEFAULT_COLOR = theme.color.primary
ICON_HOVER_COLOR = theme.color.primary_light


def get_center_page_list(current_page: int, sum_page_nums: int) -> list:
    """
    根据当前页码和总页数生成分页按钮的页码列表。
    - 页数少于等于6时，全部显示。
    - 页数较多时，显示部分页码和省略号。
    """
    if sum_page_nums <= 6:
        return list(range(1, sum_page_nums + 1))
    if current_page < 5:
        return list(range(1, 6)) + [-1, sum_page_nums]
    if sum_page_nums - 5 < current_page <= sum_page_nums:
        return [1, -1] + list(range(sum_page_nums - 4, sum_page_nums + 1))
    return [1, -1] + list(range(current_page - 2, current_page + 3)) + [-1, sum_page_nums]


@dataclass
class Paging(ft.Row):
    """
    分页控件，支持页码跳转、每页条数切换等功能。
    """

    sum_data_nums: int = 0  # 总数据条数
    on_change_page: Optional[Callable[[int], None]] = None  # 页码变更回调
    data_per_page_nums: int = 10  # 每页数据条数
    current_page: int = 1  # 当前页码
    data_unit: str = '条'  # 数据单位

    def __post_init__(self, ref: Optional[ft.Ref[Any]] = None):
        # 总数显示
        self.v_count = ft.Text(value=f'共 {self.sum_data_nums} {self.data_unit}')
        # 页码按钮行
        self.v_now_page = ft.Row(controls=self.get_center_page_button_list())
        # 跳转输入框
        self.v_goto_page = Input(
            on_submit=self.handle_goto_page_submit,
            width=40,
            height=32,
            text_align=ft.TextAlign.CENTER,
            content_padding=0,
        )
        # 每页条数选择框
        self.v_num_of_row_changer_field = ui.SelectBox(
            options=[ui.SelectOption(text=str(_), key=_) for _ in [5, 10, 15, 20, 30, 40, 50]],
            value=str(self.data_per_page_nums),
            width=48,
            height=ICON_HEIGHT,
            on_change=self.handle_change_data_per_page_nums,
        )
        # 组装控件
        self.controls = [
            self.v_count,
            ft.Row(
                controls=[
                    self.v_now_page,
                    ft.Text('跳至'),
                    self.v_goto_page,
                    ft.Text('页'),
                ],
                spacing=6,
            ),
            ft.Row(
                controls=[
                    ft.Text('每页'),
                    self.v_num_of_row_changer_field,
                    ft.Text(self.data_unit),
                ]
            ),
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        super().__post_init__(ref)

    @property
    def sum_page_nums(self) -> int:
        """计算总页数"""
        num_page, num_page_over = divmod(self.sum_data_nums, self.data_per_page_nums)
        return num_page + (1 if num_page_over else 0)

    def handle_change_data_per_page_nums(self, e):
        """每页条数变更事件"""
        self.data_per_page_nums = int(e.control.value)
        self.current_page = 1  # 切换每页条数时回到首页
        self.refresh_page_buttons()
        if self.on_change_page:
            self.on_change_page(self.current_page)

    def handle_update(self):
        """刷新总数和页码按钮"""
        self.v_count.value = f'共 {self.sum_data_nums} {self.data_unit}'
        self.refresh_page_buttons()

    def update_sum_data_nums(self, value: int):
        """外部调用：更新总数据条数"""
        self.sum_data_nums = value
        self.handle_update()

    def handle_goto_page_submit(self, e):
        """跳转页码输入框提交事件"""
        try:
            page = int(e.control.value)
            if 1 <= page <= self.sum_page_nums:
                self.current_page = page
                if self.on_change_page:
                    self.on_change_page(self.current_page)
                self.refresh_page_buttons()
        except Exception:
            pass  # 非法输入忽略

    def get_center_page_button_list(self) -> list:
        """生成页码按钮列表"""
        rst_control_list = []

        # 上一页按钮
        prev_page_btn = ft.IconButton(
            ft.Icons.KEYBOARD_ARROW_LEFT,
            on_click=self.click_update_page,
            tooltip='上一页',
            data=self.current_page - 1,
            width=ICON_WIDTH,
            height=ICON_HEIGHT,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: theme[StyleType.PRIMARY].color,
                    ft.ControlState.HOVERED: theme[StyleType.PRIMARY].color,
                },
                side={ft.ControlState.HOVERED: ft.BorderSide(1, theme[StyleType.PRIMARY].color_light)},
                shape=ft.RoundedRectangleBorder(radius=theme.border_radius.medium),
                padding=0,
            ),
            disabled=self.current_page <= 1,
            icon_color=ft.Colors.GREY if self.current_page <= 1 else None,
        )
        rst_control_list.append(prev_page_btn)

        # 中间页码按钮
        for _page in get_center_page_list(self.current_page, self.sum_page_nums):
            if _page == -1:
                rst_control_list.append(ft.Text('...'))
            elif _page == self.current_page:
                # 当前页高亮
                rst_control_list.append(
                    ft.TextButton(
                        content=ft.Text(str(_page), color=ft.Colors.WHITE),
                        on_click=self.click_update_page,
                        tooltip=f'第 {_page} 页',
                        data=_page,
                        width=ICON_WIDTH,
                        height=ICON_HEIGHT,
                        style=ft.ButtonStyle(
                            bgcolor=theme.color.primary,
                            color={ft.ControlState.HOVERED: theme.color.primary},
                            shape=ft.RoundedRectangleBorder(radius=theme.border_radius.medium),
                            padding=0,
                        ),
                    )
                )
            else:
                # 普通页码
                rst_control_list.append(
                    ft.TextButton(
                        content=ft.Text(str(_page)),
                        on_click=self.click_update_page,
                        tooltip=f'第 {_page} 页',
                        data=_page,
                        width=ICON_WIDTH,
                        height=ICON_HEIGHT,
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                ft.ControlState.HOVERED: theme.color.primary,
                            },
                            side={ft.ControlState.HOVERED: ft.BorderSide(1, theme[StyleType.PRIMARY].color_light)},
                            shape=ft.RoundedRectangleBorder(radius=theme.border_radius.medium),
                            padding=0,
                        ),
                    )
                )

        # 下一页按钮
        next_page_btn = ft.IconButton(
            ft.Icons.KEYBOARD_ARROW_RIGHT,
            icon_size=20,
            on_click=self.click_update_page,
            tooltip='下一页',
            data=self.current_page + 1,
            width=ICON_WIDTH,
            height=ICON_HEIGHT,
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: theme[StyleType.PRIMARY].color,
                    ft.ControlState.HOVERED: theme[StyleType.PRIMARY].color,
                },
                side={ft.ControlState.HOVERED: ft.BorderSide(1, theme[StyleType.PRIMARY].color_light)},
                shape=ft.RoundedRectangleBorder(radius=theme.border_radius.medium),
                padding=0,
            ),
            disabled=self.current_page >= self.sum_page_nums,
            icon_color=ft.Colors.GREY if self.current_page >= self.sum_page_nums else None,
        )
        rst_control_list.append(next_page_btn)
        return rst_control_list

    def refresh_page_buttons(self):
        """刷新页码按钮行"""
        self.v_now_page.controls = self.get_center_page_button_list()

    def click_update_page(self, e):
        """点击页码或前后页按钮事件"""
        page = int(e.control.data)
        if 1 <= page <= self.sum_page_nums:
            self.current_page = page
            if self.on_change_page:
                self.on_change_page(self.current_page)
            self.refresh_page_buttons()


def handle_test(data=0):
    print(data)


def demo():
    """分页控件演示"""
    return ft.Column(
        controls=[
            Paging(
                sum_data_nums=1000,
                on_change_page=handle_test,
            ),
        ]
    )


def main(page: ft.Page):
    page.title = 'Paging'
    page.scroll = ft.ScrollMode.AUTO
    page.add(demo())


if __name__ == '__main__':
    ft.run(main)
