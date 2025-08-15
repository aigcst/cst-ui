"""参考 flet-contrib color-picker"""

import colorsys

import flet as ft


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0)
    )


def hex2rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def hex2hsv(value):
    rgb_color = hex2rgb(value)
    return colorsys.rgb_to_hsv(
        rgb_color[0] / 255, rgb_color[1] / 255, rgb_color[2] / 255
    )


SLIDER_WIDTH = 180
CIRCLE_SIZE = 16


class HueSlider(ft.GestureDetector):
    def __init__(self, on_change_hue, hue=1):
        super().__init__()
        self.__hue = hue
        self.__number_of_hues = 10
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_slider()
        self.on_change_hue = on_change_hue
        self.on_pan_start = self.drag_start
        self.on_pan_update = self.drag_update

    # hue
    @property
    def hue(self) -> float:
        return self.__hue

    @hue.setter
    def hue(self, value: float):
        if isinstance(value, float):
            self.__hue = value
            if value < 0 or value > 1:
                raise Exception("Hue value should be between 0 and 1")
        else:
            raise Exception("Hue value should be a float number")

    def _before_build_command(self):
        super()._before_build_command()
        # called every time on self.update()
        self.thumb.left = self.__hue * self.track.width
        self.thumb.bgcolor = rgb2hex(colorsys.hsv_to_rgb(self.__hue, 1, 1))

    def __update_selected_hue(self, x):
        self.__hue = max(0, min((x - CIRCLE_SIZE / 2) / self.track.width, 1))
        self.thumb.left = self.__hue * self.track.width
        self.thumb.bgcolor = rgb2hex(colorsys.hsv_to_rgb(self.__hue, 1, 1))

    def update_selected_hue(self, x):
        self.__update_selected_hue(x)
        self.thumb.update()
        self.on_change_hue()

    def drag_start(self, e: ft.DragStartEvent):
        self.update_selected_hue(x=e.local_position.x)

    def drag_update(self, e: ft.DragUpdateEvent):
        self.update_selected_hue(x=e.local_position.x)

    def generate_gradient_colors(self):
        colors = []
        for i in range(0, self.__number_of_hues + 1):
            color = rgb2hex(colorsys.hsv_to_rgb(i / self.__number_of_hues, 1, 1))
            colors.append(color)
        return colors

    def generate_slider(self):
        self.track = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=self.generate_gradient_colors(),
            ),
            width=SLIDER_WIDTH - CIRCLE_SIZE,
            height=CIRCLE_SIZE / 2,
            border_radius=5,
            top=CIRCLE_SIZE / 4,
            left=CIRCLE_SIZE / 2,
        )

        self.thumb = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )
        self.content: ft.Stack
        self.content.controls.append(self.track)
        self.content.controls.append(self.thumb)


COLOR_MATRIX_WIDTH = 340
CIRCLE_SIZE = 20


class ColorPickerFletContrib(ft.Column):
    def __init__(self, color="#000000", width=COLOR_MATRIX_WIDTH):
        super().__init__()
        self.tight = True
        self.width = width
        self.__color = color
        self.hue_slider = HueSlider(
            on_change_hue=self.update_color_picker_on_hue_change,
            hue=hex2hsv(self.color)[0],
        )
        self.generate_color_map()
        self.generate_selected_color_view()

    # color
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    def before_update(self):
        super().before_update()
        # called every time on self.update()
        self.hue_slider.hue = hex2hsv(self.color)[0]
        self.update_circle_position()
        self.update_color_map()
        self.update_selected_color_view_values()

    def update_circle_position(self):
        hsv_color = hex2hsv(self.color)
        self.thumb.left = hsv_color[1] * self.color_map.width  # s * width
        self.thumb.top = (1 - hsv_color[2]) * self.color_map.height  # (1-v)*height

    def find_color(self, x, y):
        h = self.hue_slider.hue
        s = x / self.color_map.width
        v = (self.color_map.height - y) / self.color_map.height
        self.color = rgb2hex(colorsys.hsv_to_rgb(h, s, v))

    def generate_selected_color_view(self):
        rgb = hex2rgb(self.color)

        def on_hex_submit(e):
            self.color = e.control.value
            self.update()

        def __on_rgb_submit():
            rgb = (
                int(self.r.value) / 255,
                int(self.g.value) / 255,
                int(self.b.value) / 255,
            )
            self.color = rgb2hex(rgb)

        def on_rgb_submit(e):
            __on_rgb_submit()
            self.update()

        self.hex = ft.TextField(
            label="Hex",
            text_size=12,
            value=self.__color,
            height=40,
            width=90,
            on_submit=on_hex_submit,
            on_blur=on_hex_submit,
        )
        self.r = ft.TextField(
            label="R",
            height=40,
            width=55,
            value=rgb[0],
            text_size=12,
            on_submit=on_rgb_submit,
            on_blur=on_rgb_submit,
        )
        self.g = ft.TextField(
            label="G",
            height=40,
            width=55,
            value=rgb[1],
            text_size=12,
            on_submit=on_rgb_submit,
            on_blur=on_rgb_submit,
        )
        self.b = ft.TextField(
            label="B",
            height=40,
            width=55,
            value=rgb[2],
            text_size=12,
            on_submit=on_rgb_submit,
            on_blur=on_rgb_submit,
        )
        self.selected_color_view = ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Container(
                            width=30, height=30, border_radius=30, bgcolor=self.__color
                        ),
                        self.hue_slider,
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        self.hex,
                        self.r,
                        self.g,
                        self.b,
                    ],
                ),
            ],
        )

        self.controls.append(self.selected_color_view)

    def update_selected_color_view_values(self):
        rgb = hex2rgb(self.color)
        self.selected_color_view.controls[0].controls[
            0
        ].bgcolor = self.color  # Colored circle
        self.hex.value = self.__color  # Hex
        self.r.value = rgb[0]  # R
        self.g.value = rgb[1]  # G
        self.b.value = rgb[2]  # B
        self.thumb.bgcolor = self.color  # Color matrix circle

    def generate_color_map(self):
        def __move_circle(x, y):
            self.thumb.top = max(
                0,
                min(
                    y - CIRCLE_SIZE / 2,
                    self.color_map.height,
                ),
            )
            self.thumb.left = max(
                0,
                min(
                    x - CIRCLE_SIZE / 2,
                    self.color_map.width,
                ),
            )
            self.find_color(x=self.thumb.left, y=self.thumb.top)
            self.update_selected_color_view_values()

        def on_pan_update(e: ft.DragStartEvent):
            __move_circle(x=e.local_position.x, y=e.local_position.y)
            self.selected_color_view.update()
            self.thumb.update()

        self.color_map_container = ft.GestureDetector(
            content=ft.Stack(
                width=self.width,
                height=int(self.width * 3 / 5),
            ),
            on_pan_start=on_pan_update,
            on_pan_update=on_pan_update,
        )

        saturation_container = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=[ft.Colors.WHITE, ft.Colors.RED],
            ),
            width=self.color_map_container.content.width - CIRCLE_SIZE,
            height=self.color_map_container.content.height - CIRCLE_SIZE,
            border_radius=5,
        )

        self.color_map = ft.ShaderMask(
            top=CIRCLE_SIZE / 2,
            left=CIRCLE_SIZE / 2,
            content=saturation_container,
            blend_mode=ft.BlendMode.MULTIPLY,
            shader=ft.LinearGradient(
                begin=ft.Alignment.TOP_CENTER,
                end=ft.Alignment.BOTTOM_CENTER,
                colors=[ft.Colors.WHITE, ft.Colors.BLACK],
            ),
            border_radius=5,
            width=saturation_container.width,
            height=saturation_container.height,
        )

        self.thumb = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.color_map_container.content.controls.append(self.color_map)
        self.color_map_container.content.controls.append(self.thumb)
        self.controls.append(self.color_map_container)

    def update_color_map(self):
        h = self.hue_slider.hue
        s = hex2hsv(self.color)[1]
        v = hex2hsv(self.color)[2]
        container_gradient_colors = [
            rgb2hex(colorsys.hsv_to_rgb(h, 0, 1)),
            rgb2hex(colorsys.hsv_to_rgb(h, 1, 1)),
        ]

        self.color_map.content.gradient.colors = container_gradient_colors

        self.color = rgb2hex(colorsys.hsv_to_rgb(h, s, v))

    def update_color_picker_on_hue_change(self):
        self.update_color_map()
        self.update_selected_color_view_values()
        self.selected_color_view.update()
        self.color_map_container.update()


class ColorPicker(ft.Container):
    def __init__(
        self,
        color: str = ft.Colors.BLACK,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

        self.color_picker = ColorPickerFletContrib(color="#c8df6f", width=300)
        self.v_color_icon = ft.IconButton(
            icon=ft.Icons.BRUSH, on_click=self.open_color_picker, icon_color=color
        )
        self.v_color_dialog = ft.AlertDialog(
            content=self.color_picker,
            actions=[
                ft.TextButton("确认", on_click=self.change_color),
                ft.TextButton("取消", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self.change_color,
        )
        self.content = self.v_color_icon

    @property
    def color(self):
        return self.v_color_icon.icon_color

    def open_color_picker(self, e):
        e.page.open(self.v_color_dialog)

    def close_dialog(self, e):
        e.page.close(self.v_color_dialog)

    def change_color(self, e):
        self.v_color_icon.icon_color = self.color_picker.color
        e.page.close(self.v_color_dialog)
        self.v_color_icon.update()


def demo():
    return ft.Column(controls=[ColorPicker(color=ft.Colors.RED)])


def main(page: ft.Page):
    page.add(demo())


if __name__ == "__main__":
    ft.run(main)
