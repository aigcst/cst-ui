import re

import flet as ft

from cst_ui.basic.theme import theme


class LogContainer(ft.Container):
    """
    日志显示容器，支持不同类型日志高亮显示和自动滚动。
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 日志列表控件，自动滚动
        self.lv = ft.ListView(expand=1, spacing=2, padding=4, auto_scroll=True, height=200)
        # 支持文本选择
        self.content = ft.SelectionArea(content=self.lv)
        # 边框与圆角
        self.border = ft.Border.all(color=ft.Colors.GREY_400, width=1)
        self.margin = ft.margin.all(6)
        self.border_radius = 6

    def add(self, log_str: str):
        """
        添加日志内容，根据内容关键字自动高亮不同颜色。
        """
        log_str = str(log_str)
        log_color = ft.Colors.BLACK
        is_common = False

        # 根据关键字匹配日志类型，设置颜色
        if re.search(r'error', log_str, re.IGNORECASE):
            log_color = theme.color.error
        elif re.search(r'warning', log_str, re.IGNORECASE):
            log_color = theme.color.warning
        elif re.search(r'success', log_str, re.IGNORECASE):
            log_color = theme.color.success
        elif re.search(r'info', log_str, re.IGNORECASE):
            log_color = theme.color.primary
        else:
            is_common = True

        # 普通日志用 Markdown，特殊日志用 Text 并高亮
        if is_common:
            self.lv.controls.append(ft.Markdown(value=log_str))
        else:
            self.lv.controls.append(ft.Text(value=log_str, color=log_color))
        self.update()

    def clear(self):
        """
        清空日志内容。
        """
        self.lv.controls.clear()
        self.update()


def demo():
    """
    日志容器控件演示。
    """
    import time

    logger_container = LogContainer(bgcolor=ft.Colors.GREY_200, height=200)

    def test(_):
        # 添加不同类型日志
        logger_container.add(f'test{time.time()}')
        logger_container.add(
            """
qqer 
wqer     
dsasf


                             """
        )
        logger_container.add('error:test')
        logger_container.add('warning:test')
        logger_container.add('success:test')

    def test_clear(_):
        logger_container.clear()

    test_btn = ft.Button(content=ft.Text(value='测试日志'), on_click=test)
    clear_btn = ft.Button(content=ft.Text(value='清理日志'), on_click=test_clear)

    return ft.Column(controls=[test_btn, clear_btn, logger_container])


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == '__main__':
    ft.run(main)
