import asyncio
from pathlib import Path

import flet as ft

HTTP_SERVER_PORT = 88


class FileDownload(ft.TextButton):
    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path
        self.http_file_path = f"http://localhost:{HTTP_SERVER_PORT}/{self.file_path}"

        self.text = f"下载 {self.file_path.name}"
        self.on_click = self.handle_click_btn

    def did_mount(self):
        self.page.run_task(self.open_http_server)
        return super().did_mount()

    async def open_http_server(self):
        self.http_server_proc = await asyncio.create_subprocess_shell(
            f"python -m http.server {HTTP_SERVER_PORT}",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    def will_unmount(self):
        self.http_server_proc.kill()
        return super().will_unmount()

    def handle_click_btn(self, e):
        self.page.launch_url(self.http_file_path)
        self.page.update()


def demo():
    return ft.Column(controls=[FileDownload(Path(r"./pyproject.toml"))])


def main(page: ft.Page):
    page.title = "Test"
    # page.theme_mode = "dark"
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)
