import flet as ft


class Column(ft.ListView):
    def did_mount(self):
        for i in range(8000):
            self.controls.append(ft.Text(value="test"))
            yield
            self.update()
        return super().did_mount()


def demo(page: ft.Page):
    from cst_ui.display.text import Code

    with open(__file__, "r", encoding="utf-8") as f:
        file_text = f.read()
    return ft.Column(controls=[Code(file_text), Column()])


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE

    page.add(demo(page=page))


if __name__ == "__main__":
    ft.run(main)
