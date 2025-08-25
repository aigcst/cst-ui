from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List

import flet as ft


@dataclass
class Carousel(ft.Row):
    """
    图片轮播控件，支持动画切换、主图放大、描述显示等功能。
    """

    images_list: List[str] = field(default_factory=list)
    animations: ft.AnimationCurve = ft.AnimationCurve.LINEAR
    compact: bool = False
    descriptive: bool = False
    transform_factor: float = 1.0  # 图片缩放因子

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.number_of_items = len(self.images_list)
        self.current_image_index = 0
        self.animation_in = self.animations
        self.animation_out = self.animations
        self.controls = self.build_carousel()
        self.alignment = ft.MainAxisAlignment.CENTER
        super().__post_init__(ref)

    def update_image_view(self, index: int, main_image: bool = False):
        """
        构建指定索引的图片视图，支持主图放大和描述显示。
        """
        if self.number_of_items == 0:
            return ft.Container(ft.Text('无图片'), width=200, height=150)
        index = index % self.number_of_items  # 支持循环
        src = str(self.images_list[index])
        description = Path(src).name if self.descriptive and main_image else ''
        # 图片尺寸
        base_width, base_height = (500, 300) if main_image else (300, 200)
        width = base_width * self.transform_factor
        height = base_height * self.transform_factor

        image = ft.Container(
            ft.Image(src=src, fit=ft.BoxFit.FILL, border_radius=ft.border_radius.all(5)),
            margin=5,
        )
        container = ft.Container(image, width=width, height=height)

        if self.descriptive and main_image:
            return ft.Column(
                [container, ft.Text(description)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        return container

    def build_carousel(self):
        """
        构建轮播控件，包括图片和左右切换按钮。
        """

        def navigate(offset: int):
            """切换图片索引并刷新视图"""
            if self.number_of_items == 0:
                return
            self.current_image_index = (self.current_image_index + offset) % self.number_of_items
            if not self.compact:
                carousel_row.content.controls = [
                    self.update_image_view(self.current_image_index - 1),
                    self.update_image_view(self.current_image_index, main_image=True),
                    self.update_image_view(self.current_image_index + 1),
                ]
            else:
                carousel_row.content.controls = [self.update_image_view(self.current_image_index, main_image=True)]
            self.update()

        # 初始图片内容
        if not self.compact:
            carousel_content_row = [
                self.update_image_view(self.current_image_index - 1),
                self.update_image_view(self.current_image_index, main_image=True),
                self.update_image_view(self.current_image_index + 1),
            ]
        else:
            carousel_content_row = [self.update_image_view(self.current_image_index, main_image=True)]

        # 动画切换行
        carousel_row = ft.AnimatedSwitcher(
            ft.Row(
                carousel_content_row,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=500,
            reverse_duration=500,
            switch_in_curve=self.animation_in,
            switch_out_curve=self.animation_out,
        )

        # 左右切换按钮
        prev_button = ft.FloatingActionButton(
            icon=ft.Icons.NAVIGATE_BEFORE_ROUNDED,
            on_click=lambda _: navigate(-1),
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.CircleBorder(),
        )
        next_button = ft.FloatingActionButton(
            icon=ft.Icons.NAVIGATE_NEXT_ROUNDED,
            on_click=lambda _: navigate(1),
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.CircleBorder(),
        )

        return [prev_button, carousel_row, next_button]


@dataclass
class CarouselLine(ft.Container):
    """
    横向滚动图片条，支持左右按钮滚动。
    """

    images_list: List[str] = field(default_factory=list)

    def __post_init__(self, ref: ft.Ref[Any] | None):
        # 图片横向滚动行
        self.v_carousel = ft.Row(controls=[ft.Image(src=img) for img in self.images_list], scroll=ft.ScrollMode.HIDDEN)
        # 左右滚动按钮
        self.v_buttons = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD_ARROW_LEFT,
                    on_click=lambda e: self.v_carousel.scroll_to(
                        delta=-200, duration=300, curve=ft.AnimationCurve.DECELERATE
                    ),
                ),
                ft.IconButton(
                    icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                    on_click=lambda e: self.v_carousel.scroll_to(
                        delta=200, duration=300, curve=ft.AnimationCurve.DECELERATE
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
        )
        self.content = ft.Column(controls=[self.v_carousel, self.v_buttons])
        self.shadow = ft.BoxShadow(blur_radius=20, color=ft.Colors.GREY)
        super().__post_init__(ref)


def demo():
    """
    轮播控件演示。
    """
    img_dir = Path(r'data/images')
    img_file_list = []
    for i in range(10):
        for file in img_dir.iterdir():
            if file.suffix == '.jpg' or file.suffix == '.png':
                img_file_list.append(str(file))

    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    Carousel(
                        images_list=img_file_list,
                        animations=ft.AnimationCurve.EASE,
                    )
                ],
            ),
            CarouselLine(images_list=img_file_list),
        ]
    )


def main(page: ft.Page):
    page.title = '图片轮播演示'
    page.add(demo())
    page.update()


if __name__ == '__main__':
    ft.run(main)
