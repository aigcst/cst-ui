import flet as ft


class FileField:
    """
    文件字段基类，提供文件相关属性。
    """

    def __init__(self):
        self.is_file_field = True
        self.file_changed = False
        self.value = None


class FilePickerImage(ft.Stack, FileField):
    """
    图片选择控件，支持图片预览与文件选择。
    """

    def __init__(self):
        ft.Stack.__init__(self)
        FileField.__init__(self)

        # 图片控件，初始为默认图片
        self.image = ft.Image(
            width=150,
            height=150,
            border_radius=10,
            fit=ft.BoxFit.COVER,
            src='data/images/lenna.png',
        )

        # 容器，包含图片和标题
        self.content = ft.Container(
            height=200,
            width=150,
            content=ft.Column([ft.Text('dish image'), self.image]),
            on_click=self.image_click,
            alignment=ft.Alignment.CENTER,
        )

        # 文件选择器
        self.file_picker = ft.FilePicker(on_upload=self.image_picked)

    def did_mount(self):
        """
        组件挂载时，将文件选择器注册到页面服务。
        """
        if hasattr(self, 'page') and self.page:
            self.page.services.append(self.file_picker)

    def image_picked(self, e):
        """
        文件选择回调，更新图片显示。
        """
        if not e.files:
            return
        file = e.files[0]
        self.value = file.path
        self.file_changed = True
        self.update()

    def update(self):
        """
        更新图片显示。
        """
        if self.value:
            self.image.src = self.value
            self.image.update()
        ft.Stack.update(self)  # 调用父类 update

    async def image_click(self, _):
        """
        点击图片时触发文件选择。
        """
        await self.file_picker.pick_files_async(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
        )

    def build(self):
        """
        返回控件内容。
        """
        return self.content


def demo():
    """
    图片选择控件演示。
    """
    return ft.Column(controls=[FilePickerImage()])


def main(page: ft.Page):
    page.title = '图片选择'
    page.scroll = ft.ScrollMode.AUTO
    page.add(demo())


if __name__ == '__main__':
    ft.run(main)
