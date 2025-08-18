from dataclasses import dataclass
from typing import Any, Callable

import flet as ft

from cst_ui.basic.theme import StyleType, theme


@dataclass
class WindowCloseConfirm(ft.AlertDialog):
    """程序关闭时弹出框"""

    def __init__(self, page: ft.Page):
        super().__init__()
        page.window.prevent_close = True
        page.window.on_event = self.window_event
        self.modal = True
        self.title = ft.Text("确认")
        self.content = ft.Text("是否确认关闭程序?")
        self.actions = [
            ft.ElevatedButton(ft.Text(value="是"), on_click=self.yes_click),
            ft.OutlinedButton(ft.Text(value="否"), on_click=self.no_click),
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def window_event(self, e):
        if e.data == "close":
            e.page.open(self)
            e.page.update()

    def yes_click(self, e):
        # page.window.destroy()
        e.page.close(self)
        e.page.window.prevent_close = False
        e.page.window.close()
        # e.page.window.destroy()

    def no_click(self, e):
        self.open = False
        self.update()


@dataclass
class AlertDialog(ft.AlertDialog):
    title: ft.Control | None = None
    msg: str | None = None
    on_yes_click: Callable | None = None
    on_no_click: Callable | None = None
    style_type: StyleType = StyleType.DEFAULT

    def __post_init__(self, ref: ft.Ref[Any] | None):
        border_radius_value = theme.border_radius.medium
        if isinstance(self.title, str):
            title = ft.Container(
                ft.Row(
                    [
                        ft.Text(self.title, weight=ft.FontWeight.W_500),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color="#777777",
                            icon_size=20,
                            tooltip="关闭",
                            on_click=self.__on_no_click,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=ft.Colors.with_opacity(0.5, theme[self.style_type].color_light),
                padding=ft.padding.only(left=16, top=4, bottom=4),
                border_radius=ft.BorderRadius(
                    top_left=border_radius_value,
                    top_right=border_radius_value,
                    bottom_left=0,
                    bottom_right=0,
                ),
            )

        self.title_padding = 0
        self.content_padding = 0
        self.actions_padding = 0
        self.inset_padding = 0
        self.alert_dialog_type = self.style_type
        print(f"AlertDialog: {self.content}")
        if self.content is None:
            if self.style_type is not None and self.msg is not None:
                self.content = ft.Container(
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.IconButton(
                                    width=30,
                                    height=30,
                                    icon_size=20,
                                    icon=theme[self.style_type].icon,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                        },
                                        padding=0,
                                    ),
                                    # color=ft.Colors.WHITE,
                                ),
                                border_radius=ft.border_radius.all(1000),
                                bgcolor=theme[self.style_type].color,
                            ),
                            ft.Text(value=self.msg),
                        ],
                        wrap=True,
                    ),
                )
            else:
                self.content = ft.Container(
                    ft.Row(controls=[ft.Text(self.msg)], wrap=True),
                )
            self.content.padding = ft.padding.only(
                left=16,
                top=8,
                bottom=8,
            )
            # self.content.bgcolor = ft.Colors.with_opacity(0.90, "white")
            self.content.bgcolor = ft.Colors.WHITE

        if self.actions is None or self.actions == []:
            self.actions = []
            if self.on_no_click is not None:
                self.actions.append(
                    ft.ElevatedButton(
                        content=ft.Text("取消"), on_click=self.__on_no_click
                    )
                )
            if self.on_yes_click is not None:
                self.actions.append(
                    ft.ElevatedButton(
                        content=ft.Text("确认"), on_click=self.__on_yes_click
                    )
                )

            self.actions_alignment = ft.MainAxisAlignment.END
            self.content.border_radius = ft.BorderRadius(
                top_left=0,
                top_right=0,
                bottom_left=border_radius_value,
                bottom_right=border_radius_value,
            )

        if self.on_yes_click is not None:
            self.actions.append(
                ft.ElevatedButton(
                    content=ft.Text("确认"),
                    height=32,
                    on_click=self.__on_yes_click,
                    # style_type=StyleType.PRIMARY,
                )
            )
        if self.on_no_click is not None:
            self.actions.append(
                ft.ElevatedButton(
                    content=ft.Text("取消"),
                    height=32,
                    on_click=self.__on_no_click,
                    # style_type=StyleType.DEFAULT,
                )
            )

        self.actions_alignment = ft.MainAxisAlignment.END
        self.shape = ft.RoundedRectangleBorder(radius=border_radius_value)
        return super().__post_init__(ref)

    def __on_yes_click(self, e):
        if self.on_yes_click is not None:
            self.on_yes_click(e)
        self.open = False
        e.page.update()

    def __on_no_click(self, e):
        if self.on_no_click is not None:
            self.on_no_click(e)
        self.open = False
        e.page.update()

    def show(self, page: ft.Page):
        if isinstance(self.title, str):
            self.title = ft.Text(self.title)
        page.overlay.append(self)
        self.open = True
        page.update()

    def close(self, page: ft.Page):
        self.open = False
        page.update()


def loading_dialogs(page: ft.Page, text: str) -> ft.AlertDialog:
    alertdialog = ft.AlertDialog(
        modal=False,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            value=f"{text}",
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            italic=True,
                            font_family="Verdana",
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ProgressRing(),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            height=180,
            width=130,
        ),
    )

    page.overlay.append(alertdialog)
    alertdialog.open = True
    page.update()

    return alertdialog


def show_alert_dialog(page: ft.Page, alert_dialog: ft.AlertDialog):
    alert_dialog.modal = True
    page.open(alert_dialog)


def demo():
    default_dialog = AlertDialog(
        title="常规弹窗",
        # actions_padding=10,
        content=ft.Container(
            ft.Text("测试表单内容"),
            height=400,
            width=400,
            padding=ft.padding.only(left=16, top=4, bottom=4),
        ),
        # on_yes_click=lambda _: print('yes'),
        # on_no_click=lambda _: print('no'),
    )
    primary_dialog = AlertDialog(
        title="primary 弹窗", msg="tessssst", style_type=StyleType.PRIMARY
    )
    success_dialog = AlertDialog(
        title="success 弹窗", msg="tessssst", style_type=StyleType.SUCCESS
    )
    warning_dialog = AlertDialog(
        title="warning 弹窗", msg="tessssst", style_type=StyleType.WARNING
    )
    error_dialog = AlertDialog(
        title="error 弹窗", msg="tessssst", style_type=StyleType.ERROR
    )
    info_dialog = AlertDialog(
        title="info 弹窗", msg="tessssst", style_type=StyleType.INFO
    )

    def test_click(e):
        default_dialog.show(e.page)

    def test_click2(e):
        primary_dialog.show(e.page)

    def test_click3(e):
        success_dialog.show(e.page)

    def test_click4(e):
        warning_dialog.show(e.page)

    def test_click5(e):
        error_dialog.show(e.page)

    def test_click6(e):
        info_dialog.show(e.page)

    default_button = ft.ElevatedButton(ft.Text(value="常规弹窗"), on_click=test_click)
    primary_button = ft.ElevatedButton(
        ft.Text(value="primary 弹窗"), on_click=test_click2
    )
    success_button = ft.ElevatedButton(
        ft.Text(value="success 弹窗"), on_click=test_click3
    )
    warning_button = ft.ElevatedButton(
        ft.Text(value="warning 弹窗"), on_click=test_click4
    )
    error_button = ft.ElevatedButton(ft.Text(value="error 弹窗"), on_click=test_click5)
    info_button = ft.ElevatedButton(ft.Text(value="info 弹窗"), on_click=test_click6)
    return ft.Column(
        controls=[
            default_button,
            primary_button,
            success_button,
            warning_button,
            error_button,
            info_button,
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.add(
        ft.IconButton(
            ft.Icons.DONE, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN
        )
    )
    page.add(ft.Icon(ft.Icons.DONE_OUTLINED))
    page.add(ft.Icon(ft.Icons.DONE_ROUNDED))
    page.add(ft.Icon(ft.Icons.DONE_SHARP))
    loading_dialogs(page, text="加载中")
    # 关闭前确认
    window_close = WindowCloseConfirm(page)
    page.add(window_close)


if __name__ == "__main__":
    ft.run(main)
