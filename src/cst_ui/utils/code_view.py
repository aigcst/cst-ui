import flet as ft

from cst_ui.display.text import Code
from cst_ui.layout.expander import Expander


class CodeView(ft.Column):
    def __init__(self, code_str, **kwargs):
        super().__init__(**kwargs)
        self.controls.append(eval(code_str))
        self.controls.append(
            Expander(title="查看代码", controls=[Code(code_str)], dense=True)
        )


def demo():
    code_str = """
ft.Text(value='test')
"""
    return ft.Column(controls=[CodeView(code_str)])


def main(page: ft.Page):
    page.add(demo())


if __name__ == "__main__":
    ft.app(main)
