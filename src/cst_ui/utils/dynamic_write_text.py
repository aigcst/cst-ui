"""动态写值的 Text"""

import time

import flet as ft


class DynamicWriteText(ft.Text):
    def __init__(self, value: str):
        super().__init__()
        self.text = value
        self.no_wrap = False
        self.value = "\n"

    def run(self, e=None):
        for i in range(len(self.text)):
            self.value = self.value[:-1] + self.text[i] + "_"
            time.sleep(0.1)
            self.update()
            print("dddd")

    # def did_mount(self):
    #     # self.run()
    #     super().did_mount()


def demo():
    test_text = """
    测试文字测试文字测试文字测试文字测试文字测试文字
    测试文字测试文字测试文字测试文字测试文字测试文字
    测试文字测试文字测试文字测试文字测试文字测试文字
    """
    dynamic_text = DynamicWriteText(test_text)
    return ft.Column(
        controls=[
            dynamic_text,
            ft.ElevatedButton(
                content=ft.Text(value="开始写入"), on_click=dynamic_text.run
            ),
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
