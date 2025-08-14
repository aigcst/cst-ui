from dataclasses import dataclass, field
from typing import Any, Callable, Union

import flet as ft
import flet.canvas as cv


@dataclass
class SliderColors:
    active_bar_color: str
    inactive_bar_color: str

    @staticmethod
    def dark():
        return SliderColors(active_bar_color="#1f5eff", inactive_bar_color="#323741")

    @staticmethod
    def light():
        return SliderColors(active_bar_color="#1f5eff", inactive_bar_color="#e8ebf4")


@dataclass
class Slider(ft.Slider):
    scale: None | ft.ScaleValue = 0.9
    # offset: None | ft.OffsetValue = ft.Offset(x=-0.1, y=0)
    theme_mode: ft.ThemeMode = ft.ThemeMode.LIGHT

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.colors = (
            SliderColors.dark()
            if self.theme_mode == ft.ThemeMode.DARK
            else SliderColors.light()
        )
        self.active_color = self.colors.active_bar_color
        self.inactive_color = self.colors.inactive_bar_color

        self.thumb_color = ft.Colors.WHITE
        self.overlay_color = ft.Colors.with_opacity(0, ft.Colors.WHITE)
        return super().__post_init__(ref)


@dataclass
class RangeSlider(ft.RangeSlider):
    min: ft.Number = 0
    max: ft.Number = 1
    start_value: ft.Number = (max - min) * 1 / 5
    end_value: ft.Number = (max - min) * 3 / 5
    scale: None | ft.ScaleValue = 0.9
    # offset: None | ft.OffsetValue = ft.Offset(x=-0.1, y=0)
    theme_mode: ft.ThemeMode = ft.ThemeMode.LIGHT

    def __post_init__(self, ref: ft.Ref[Any] | None):
        if self.min is None:
            self.min, self.max = 0, 1
            self.start_value = (self.max - self.min) * 1 / 5
            self.end_value = (self.max - self.min) * 3 / 5

        self.colors = (
            SliderColors.dark()
            if self.theme_mode == ft.ThemeMode.DARK
            else SliderColors.light()
        )
        self.active_color = self.colors.active_bar_color
        self.inactive_color = self.colors.inactive_bar_color

        self.thumb_color = ft.Colors.WHITE
        self.overlay_color = ft.Colors.with_opacity(0, ft.Colors.WHITE)
        return super().__post_init__(ref)


@dataclass
class VerticalSlider(ft.GestureDetector):
    value: Union[int, float] = 50
    min_val: Union[int, float] = 0
    max_val: Union[int, float] = 100
    label: str = "{value}%"
    round_to: int = 0
    inactive_track_border_radius: ft.BorderRadiusValue = field(
        default_factory=lambda: ft.BorderRadius.all(6)
    )
    # active_track_border_radius: Union[int, float, ft.BorderRadius] = (
    #     ft.BorderRadius.(0, 0, 6, 6),
    # )
    slider_height: Union[int, float] = 200
    slider_width: Union[int, float] = 60
    inactive_track_color: str = ft.Colors.GREY_500
    active_track_color: str = ft.Colors.GREY_900
    text_style: ft.TextStyle = field(
        default_factory=lambda: ft.TextStyle(
            weight=ft.FontWeight.BOLD, color=ft.Colors.ERROR
        )
    )

    on_change: Callable | None = None

    def __post_init__(self, ref: ft.Ref[Any] | None):
        # self.label = label if "{value}" in label else "{value}"
        self.base_color = self.inactive_track_color
        self.fill_color = self.active_track_color
        self.slider_height, self.slider_width = self.slider_height, self.slider_width

        self.on_pan_update = self.__handle_slider_drag
        self.on_hover = self.__change_mouse_cursor

        self._canvas = cv.Canvas(
            on_resize=self.__handle_canvas_resize,
            shapes=[
                cv.Rect(
                    x=0,
                    y=0,
                    height=self.slider_height,
                    # border_radius=self.base_border_radius,
                    paint=ft.Paint(color=self.base_color),
                    width=self.slider_width,
                ),
                cv.Rect(
                    x=0,
                    y=self.slider_height,
                    height=-self.__new_value_from_old(
                        self.value, self.min_val, self.max_val, 0, self.slider_height
                    ),
                    # border_radius=self.fill_border_radius,
                    paint=ft.Paint(color=self.fill_color),
                    width=self.slider_width,
                ),
                cv.Text(
                    x=self.slider_width / 2,
                    y=self.slider_height / 2,
                    text_align=ft.TextAlign.CENTER,
                    alignment=ft.Alignment.CENTER,
                    value=self.__get_label_from_value(self.value),
                    style=self.text_style,
                ),
            ],
        )

        self.content = ft.Container(
            content=self._canvas,
            height=self.slider_height,
            width=self.slider_width,
        )

        return super().__post_init__(ref)
        """
        Args:
            value: the value of the slider. Must lie between min_val and max_val
            min_val: the minimum value of the slider
            max_val: the maximum value of the slider
            label: the label of the slider. If set, "{value}" must be present and will be replaced by the slider's value
            round_to: the number of decimal places to round the slider's value to
            inactive_track_border_radius: the border radius of the slider's inactive track
            active_track_border_radius: the border radius of the slider's active track
            slider_height: the height of the slider
            slider_width: the width of the slider
            inactive_track_color: the color of the slider's inactive track
            active_track_color: the color of the slider's active track
            text_style: Set the style of the text that is displayed by default in the middle of the slider
            on_change: Callback function to be called when the value of the slider is changed
        """

    @property
    def canvas(self):
        return self._canvas

    @property
    def inactive_track_rect(self):
        return self._canvas.shapes[0]

    @property
    def active_track_rect(self):
        return self._canvas.shapes[1]

    @property
    def text(self):
        return self._canvas.shapes[2]

    def __handle_canvas_resize(self, e: cv.CanvasResizeEvent):
        """
        Called when the canvas is resized.
        It updates the slider's height and width to match that of the resized canvas.

        todo: make this function work as expected!
        """
        self.slider_height, self.slider_width = e.height, e.width
        # update canvas
        self._canvas.width = self.slider_width
        self._canvas.height = self.slider_height

        # update the text
        # e.control.shapes: list[cv.Rect, cv.Rect, cv.Text]
        e.control.shapes[2].x = self.slider_width / 2
        e.control.shapes[2].y = self.slider_height / 2

        # update base Rect
        e.control.shapes[0].height = self.slider_height

        # update fill Rect
        e.control.shapes[1].x = 0
        e.control.shapes[1].y = self.slider_height
        e.control.shapes[1].height = -self.__new_value_from_old(
            self.value, self.min_val, self.max_val, 0, -self.slider_height
        )
        e.control.shapes[1].width = self.slider_width
        self.update()

    def __handle_slider_drag(self, e: ft.DragUpdateEvent):
        """
        Called when the slider is being dragged. It updates the value of the slider displayed on the screen
        using the mouse click or move coordinates (only local_y here), and then calls update() to redraw everything.

        Args:
            e: Contains the local and global coordinates of mouse click or move/drag events
        """
        # the negative sign here plays an important role; without it, the slider's active track will go downwards
        # self.slider_height >= e.local_y >= 0   --> if True, then the user is between the boundaries of the slider
        # e.local_y >= self.slider_height --> if True, then the user is below the slider's lower boundary
        # (note: the more we go downwards, the greater the local_y)
        # else -self.slider_height  --> the user is above the slider's upper boundary, hence we make the slider full
        self.content.content.shapes[1].height = (
            -self.slider_height + e.local_position.y
            if self.slider_height >= e.local_position.y >= 0
            else 0
            if e.local_position.y >= self.slider_height
            else -self.slider_height
        )

        # translate the height of the slider to a value between the set min and max values
        self.value = self.__new_value_from_old(
            self.content.content.shapes[1].height,
            0,
            self.slider_height,
            self.min_val,
            self.max_val,
        )

        # set the slider's text
        self._canvas.shapes[2].text = self.__get_label_from_value(self.value)

        self.update()

        # pass the value of the slider to the on_change function, if set
        if self.on_change is not None:
            self.on_change(self.value)

    def __new_value_from_old(self, value, old_min, old_max, new_min, new_max):
        """
        Scales or converts a given value from an old range or scale to a new one.
        For example: if you have a number between 0-100 (old_min=0, old_max=100) but want
        it to be between 0-10 (new_min=0,new_max=10), you would call __new_value(50, 0 , 100 , 0 , 10).
        This would return 5 because 50% of 100 is 50 which is halfway between 10.

        Args:
            value: Value that is being converted (from the old range to the new one)
            old_min: Minimum value of the old range
            old_max: Maximum value of the old range
            new_min: Minimum value of the new range
            new_max: Maximum value of the new range

        Returns:
            A value that is scaled from the old range to the new range
        """
        new_val = round(
            abs(
                ((value - old_min) / (old_max - old_min)) * (new_max - new_min)
                + new_min
            ),
            self.round_to,
        )
        return int(new_val) if self.round_to == 0 else new_val

    def __get_label_from_value(self, value):
        """
        Takes a value and returns the label for that value.
        The label contains `{value}`. This function will replace {value} with str(value) and return that string.

        Args:
            value: the value used to build the label

        Returns:
            The label string built from the value of the slider
        """
        s = self.label.split("{value}")
        s.insert(1, str(value))
        return "".join(s)

    def __change_mouse_cursor(self, e: ft.HoverEvent):
        """Changes the mouse cursor when hovering on the slider."""
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        self.update()


# # def main(page: ft.Page):
# #     page.title = "Vertical Slider Example"
# #     page.theme_mode = "light"
# #     page.horizontal_alignment = page.vertical_alignment = "center"
# #     page.window_width = 390
# #     page.window_height = 400


def demo():
    def handle_slider_change(value):
        print(f"VerticalSlider: SliderValue = {value}")

    vertical_slider = VerticalSlider(
        active_track_color=ft.Colors.RED, on_change=handle_slider_change
    )
    vs_1 = VerticalSlider(
        value=50,
        label="%{value}",
        slider_width=80,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=24),
        active_track_color=ft.Colors.PRIMARY,
        inactive_track_color=ft.Colors.PRIMARY_CONTAINER,
        on_change=lambda val: print(f"VerticalSlider: slider_1_value = {val}"),
    )
    # horizontal_slider.content.bgcolor = ft.Colors.AMBER
    return ft.Column(
        controls=[
            vertical_slider,
            vs_1,
            Slider(
                active_color=ft.Colors.RED, inactive_color=ft.Colors.GREY, height=300
            ),
        ]
    )


def main(page: ft.Page):
    page.add(demo())
    page.update()


if __name__ == "__main__":
    ft.run(main)


# def demo():
#     def handle_change_radio(e):
#         print("RangeSlider: ", e.control.value)

#     def handle_click(e):
#         print(
#             "RangeSlider",
#             v_checkbox.value is None,
#             v_switch.value,
#             v_radio.value,
#             v_slide.value,
#             v_rangeslide.value,
#         )

#     return ft.Column(
#         controls=[
#             v_checkbox := CheckBox(label="确认"),
#             v_switch := Switch(label="开关"),
#             v_radio := Radio(
#                 label="单选",
#                 options=["选项1", "选项2", "选项3"],
#                 on_change=handle_change_radio,
#                 radio_layout_type=LayoutType.vertical,
#             ),
#             v_slide := Slider("数量"),
#             v_rangeslide := RangeSlider("数量范围"),
#             ft.ElevatedButton("查看数据", on_click=handle_click),
#         ]
#     )


# def main(page: ft.Page):
#     page.title = "Test"
#     set_theme(page)

#     # page.theme_mode = "dark"
#     page.add(demo())
#     page.update()


# if __name__ == "__main__":
#     ft.run(main)
