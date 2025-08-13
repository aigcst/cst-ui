import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import flet as ft
from flet.controls.core.image import (
    BlendMode,
    BorderRadiusValue,
    BoxFit,
    ColorValue,
    Control,
    FilterQuality,
    ImageRepeat,
)

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"


def img_loader(src: str, width, height: int, border_radius: int = 0) -> ft.Control:
    return ft.Stack(
        controls=[
            ft.Container(
                width=width,
                height=height,
                bgcolor="#e7ebf4",
                border_radius=border_radius,
            ),
            ft.Image(
                src=src,
                width=width,
                height=height,
                fit=ft.BoxFit.COVER,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=border_radius,
            ),
        ],
        width=width,
        height=height,
    )


class ImageAlertDialog(ft.AlertDialog):
    def __init__(self, image: "Image", **kwargs):
        super().__init__(**kwargs)
        self.title = image.src
        self.content = ft.InteractiveViewer(content=image.content)
        self.content.height = 600
        self.content.width = 800


@dataclass
class Image(ft.Container):
    src: None | str | Path = None
    src_base64: Optional[str] = None
    src_bytes: Optional[bytes] = None
    error_content: Optional[Control] = ft.Text("Loading...")
    repeat: ImageRepeat = ImageRepeat.NO_REPEAT
    fit: Optional[BoxFit] = ft.BoxFit.CONTAIN
    border_radius: Optional[BorderRadiusValue] = None
    # field(default=ft.BorderRadius.all(8))
    color: Optional[ColorValue] = None
    color_blend_mode: Optional[BlendMode] = None
    gapless_playback: bool = False
    semantics_label: Optional[str] = None
    exclude_from_semantics: bool = False
    """
    Whether to exclude this image from semantics.
    """

    filter_quality: FilterQuality = FilterQuality.MEDIUM
    """
    The rendering quality of the image.
    """

    cache_width: Optional[int] = None
    """
    The size at which the image should be decoded.

    The image will, however, be rendered to the constraints of the layout regardless
    of this parameter.
    """

    cache_height: Optional[int] = None
    """
    The size at which the image should be decoded.

    The image will, however, be rendered to the constraints of the layout regardless
    of this parameter.
    """

    anti_alias: bool = False
    tooltip: str = str(src)
    scale = 1
    """
    Whether to paint the image with anti-aliasing.

    Anti-aliasing alleviates the sawtooth artifact when the image is rotated.
    """
    width: Optional[ft.Number] = 200
    height: Optional[ft.Number] = 200

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.content = ft.Image(
            # src=self.img_path.absolute().as_posix(),
            src=str(self.src),
            src_base64=self.src_base64,
            src_bytes=self.src_bytes,
            error_content=self.error_content,
            repeat=self.repeat,
            fit=self.fit,
            border_radius=self.border_radius,
            color=self.color,
            color_blend_mode=self.color_blend_mode,
            gapless_playback=self.gapless_playback,
            semantics_label=self.semantics_label,
            exclude_from_semantics=self.exclude_from_semantics,
            filter_quality=self.filter_quality,
            cache_width=self.cache_width,
            cache_height=self.cache_height,
            anti_alias=self.anti_alias,
        )
        self.padding = 0
        self.bgcolor = ft.Colors.GREY
        self.border_radius = ft.BorderRadius.all(5)
        self.alignment = ft.Alignment.CENTER
        self.scale = 1.0
        self.on_hover = self.img_hover
        # self.v_text = ft.Text(
        #     value=v_text_value, size=12, text_align=ft.TextAlign.CENTER, max_lines=2
        # )
        # self.v_img_page = ImageAlertDialog(self)
        # self.content = ft.Container(
        #     ft.Column(
        #         controls=[
        #             ft.Container(content=self.v_image, on_click=self.double_tap),
        #             self.v_text,
        #         ],
        #         spacing=2,
        #         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #     ),
        #     alignment=ft.Alignment.TOP_CENTER,
        #     # bgcolor=ft.Colors.GREY_100,
        # )
        return super().__post_init__(ref)

    def img_hover(self, e):
        self.scale = 1.1 if e.data else 1.0

    # def update_w_h(self, width, height):
    #     new_txt_size = width / 200 * self.v_text.size
    #     if 12 <= new_txt_size <= 16:
    #         self.v_text.size = width / 200 * self.v_text.size
    #     self.v_image.width = width
    #     self.v_image.height = height
    #     self.height = height
    #     self.width = width
    #     # self.v_stack_img.width = self.v_container.width = self.image.width = self.width = width
    #     # self.v_stack_img.height = self.v_container.height = self.image.height = self.height = height
    #     self.update()


def demo():
    #     file_path = file_path_list[0].resolve()
    return ft.Column(
        controls=[
            Image(src=str(Path(r"data\images\avatar.jpg"))),
        ]
    )


def main(page: ft.Page):
    page.window.width = 1080
    page.window.height = 1080
    page.add(demo())


if __name__ == "__main__":
    ft.run(main)
