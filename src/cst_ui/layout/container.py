from dataclasses import dataclass

import flet as ft


# TODO: 右键恢复原始状态
@dataclass
class Container(ft.InteractiveViewer):
    pan_enabled: bool = False
    scale_enabled: bool = False


def demo():
    with open(__file__, "r", encoding="utf-8") as f:
        file_text = f.read()
    aa = Container(content=ft.Text(file_text))
    print(aa.pan_enabled)
    return ft.Column(controls=[aa])


def main(page: ft.Page):
    page.add(demo())


if __name__ == "__main__":
    ft.run(main)
