import asyncio
import time
from typing import Optional

import flet as ft

# class Text(ft.Text):
#     style_type: str = "default"

#     def before_update(self):
#         super().before_update()
#         self.theme_style = self.theme_style or ft.TextThemeStyle.BODY_MEDIUM


class HeaderBase(ft.Column):
    def __init__(
        self, value: str = "占位", with_divider: bool = False, divider_thickness=1, divider_height=1, **kwargs
    ):
        super().__init__(**kwargs)
        self.v_text = ft.Text(value)
        if with_divider:
            # if hasattr(ft.Colors, self.divider.upper()):
            #     divider_color = self.divider
            # else:
            #     divider_color = theme.color.divider
            self.divider_color = ft.Colors.BLACK
            self.v_divider = ft.Divider(thickness=divider_thickness, height=divider_height, color=self.divider_color)
            self.controls = [self.v_text, self.v_divider]
            self.spacing = 0
            self.alignment = ft.MainAxisAlignment.CENTER
            self.run_spacing = 0
        else:
            self.controls = [self.v_text]
        # self.height = 100
        self.padding = 0
        self.alignment = ft.MainAxisAlignment.START


class Title(HeaderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_text.theme_style = self.v_text.theme_style or ft.TextThemeStyle.DISPLAY_MEDIUM
        self.v_text.weight = self.v_text.weight or ft.FontWeight.BOLD


class SubTitle(HeaderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_text.theme_style = self.v_text.theme_style or ft.TextThemeStyle.DISPLAY_SMALL
        self.v_text.weight = self.v_text.weight or ft.FontWeight.BOLD
        # self.horizontal_alignment=ft.


class Header_1(HeaderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_text.theme_style = self.v_text.theme_style or ft.TextThemeStyle.HEADLINE_LARGE
        self.v_text.weight = self.v_text.weight or ft.FontWeight.W_600


class Header_2(HeaderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_text.theme_style = self.v_text.theme_style or ft.TextThemeStyle.HEADLINE_MEDIUM
        self.v_text.weight = self.v_text.weight or ft.FontWeight.W_500


class Header_3(HeaderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_text.theme_style = self.v_text.theme_style or ft.TextThemeStyle.HEADLINE_SMALL
        self.v_text.weight = self.v_text.weight or ft.FontWeight.W_500


class Header_4(HeaderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_text.theme_style = self.v_text.theme_style or ft.TextThemeStyle.TITLE_LARGE
        self.v_text.weight = self.v_text.weight or ft.FontWeight.W_500


class Header_5(HeaderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.v_text.theme_style = self.v_text.theme_style or ft.TextThemeStyle.TITLE_MEDIUM
        self.v_text.weight = self.v_text.weight or ft.FontWeight.W_500


class Quote(ft.Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bgcolor = ft.Colors.GREY


class Link(ft.Text):
    def __init__(self, link: str | None = None, **kwargs):
        super().__init__(**kwargs)


class Caption(ft.Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bgcolor = ft.Colors.GREY


Header = Header_1
SubHeader = Header_2
MARKDOWN_STYLE = ft.MarkdownStyleSheet(
    code_text_style=ft.TextStyle(font_family="Consolas"),
    h1_text_style=ft.TextStyle(size=36, weight=ft.FontWeight.BOLD),
    h2_text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD),
    h3_text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
    h4_text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
    h5_text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
)


class Markdown(ft.Markdown):
    def __init__(self, value: str = "", **kwargs):
        super().__init__(value=value, **kwargs)
        self.selectable = True
        self.extension_set = ft.MarkdownExtensionSet.GITHUB_WEB
        self.code_theme = ft.MarkdownCodeTheme.MONOKAI
        # BUG: 需要一个空的配置值，不然关键词会是黑色，看不清
        self.code_style_sheet = MARKDOWN_STYLE


class Json(ft.Markdown):
    # todo：树状展示，可复制
    def __init__(self, value, language="python", *args, **kwargs):
        super().__init__(*args, **kwargs)


class Code(ft.Row):
    def __init__(self, value, language="python"):
        #
        self.value = f"""```{language}
{value}
```"""
        self.language = language
        self._hovered: bool | None = None

        self.copy_box = ft.Container(
            width=28,
            height=28,
            border=ft.Border.all(1, "transparent"),
            right=1,
            top=1,
            border_radius=7,
            scale=ft.Scale(1),
            animate=ft.Animation(400, ft.AnimationCurve.EASE),
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                name=ft.Icons.COPY,
                size=14,
                color=ft.Colors.WHITE54,
                opacity=0,
                animate_opacity=ft.Animation(420, ft.AnimationCurve.EASE),
            ),
            on_click=lambda e: self.get_copy_box_content(e),
        )

        super().__init__()

        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [
            ft.Container(
                expand=True,
                padding=8,
                border_radius=8,
                # bgcolor=ft.Colors.GREY_200,
                on_hover=lambda e: self.show_copy_box(e),
                content=ft.Stack(controls=[Markdown(value=self.value), self.copy_box]),
            )
        ]

    def get_copy_box_content(self, e):
        # self.value = self.value.replace("`", "")
        # self.value = self.value.replace(self.language, "")
        tmp_value = "\n".join(self.value.splitlines()[1:-1])
        e.page.clipboard.set(tmp_value)

        # e.page.set_clipboard(tmp_value)

        while self._hovered:
            self.copy_box.disabled = True
            self.copy_box.update()

            self.copy_box.content.opacity = 0
            self.copy_box.content.name = ft.Icons.CHECK
            self.copy_box.update()

            # await asyncio.sleep(0.25)
            time.sleep(0.25)

            self.copy_box.content.opacity = 1
            self.copy_box.content.color = "teal"
            self.copy_box.update()
            time.sleep(1)
            # await asyncio.sleep(1)

            self.copy_box.content.opacity = 0
            self.copy_box.content.name = ft.Icons.COPY
            self.copy_box.content.color = ft.Colors.WHITE54
            self.copy_box.update()

            self.copy_box.disabled = False
            self.copy_box.update()

            break

        if self._hovered:
            self.copy_box.content.opacity = 1

        else:
            self.copy_box.content.opacity = 0

        self.copy_box.content.update()

    def show_copy_box(self, e):
        if e.data == True:
            self.copy_box.border = ft.Border.all(0.95, "white10")
            self.copy_box.content.opacity = 1
            self._hovered = True

        else:
            self.copy_box.content.opacity = 0
            self.copy_box.border = ft.Border.all(0.95, "transparent")
            self._hovered = False

        self.copy_box.update()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 370
    page.window.always_on_top = True
    page.scroll = ft.ScrollMode.ALWAYS
    markdown_str = """
# Markdown Example
Markdown allows you to easily include formatted text, images, and even formatted Dart code in your app.

name: `chen`
## Titles

Setext-style

This is an H1
=============

This is an H2
-------------

Atx-style

# This is an H1

## This is an H2

###### This is an H6

Select the valid headers:

- [x] # hello
- [ ] #hello

## Links

[inline-style](https://www.google.com)

## Images

![Image from Flet assets](/images/bus.jpg)

![Test image](https://picsum.photos/200/300)

## Tables

|Syntax                                 |Result                               |
|---------------------------------------|-------------------------------------|
|`*italic 1*`                           |*italic 1*                           |
|`_italic 2_`                           | _italic 2_                          |
|`**bold 1**`                           |**bold 1**                           |
|`__bold 2__`                           |__bold 2__                           |
|`This is a ~~strikethrough~~`          |This is a ~~strikethrough~~          |
|`***italic bold 1***`                  |***italic bold 1***                  |
|`___italic bold 2___`                  |___italic bold 2___                  |
|`***~~italic bold strikethrough 1~~***`|***~~italic bold strikethrough 1~~***|
|`~~***italic bold strikethrough 2***~~`|~~***italic bold strikethrough 2***~~|

## Styling

Style text as _italic_, __bold__, ~~strikethrough~~, or `inline code`.

- Use bulleted lists
- To better clarify
- Your points

## Code blocks

Formatted Dart code looks really pretty too:

```C++
void main() {
  runApp(MaterialApp(
    home: Scaffold(
      body: ft.Markdown(data: markdownData),
    ),
  ));
}
```
"""
    page.add(
        ft.Text(value="测试文本"),
        ft.Text(value="test", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        Title(value="dqwer", with_divider=True),
        Title(value="Title"),
        Header(value="Header", with_divider=True),
        SubHeader(value="SubHeader"),
        Header_1(value="标题1-Header_1"),
        # Header_2(value='标题2-Header_2', bgcolor=ft.Colors.RED),
        Header_3(value="标题3-Header_3"),
        Header_4(value="标题4-Header_4"),
        Header_5(value="标题5-Header_5"),
        ft.Text(value="Text"),
        # Text(value='primary text', style_type=StyleType.PRIMARY),
        # Text(value='info text', style_type=StyleType.INFO),
        # Text(value='success text', style_type=StyleType.SUCCESS),
        # Text(value='warning text', style_type=StyleType.WARNING),
        # Text(value='error text', style_type=StyleType.ERROR),
        ft.Text("DISPLAY_LARGE", theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
        ft.Text("DISPLAY_MEDIUM", theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM),
        ft.Text("DISPLAY_SMALL", theme_style=ft.TextThemeStyle.DISPLAY_SMALL),
        ft.Text("HEADLINE_LARGE", theme_style=ft.TextThemeStyle.HEADLINE_LARGE),
        ft.Text("HEADLINE_MEDIUM", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        ft.Text("HEADLINE_SMALL", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
        ft.Text("TITLE_LARGE", theme_style=ft.TextThemeStyle.TITLE_LARGE),
        ft.Text("TITLE_MEDIUM", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
        ft.Text("TITLE_SMALL", theme_style=ft.TextThemeStyle.TITLE_SMALL),
        ft.Text("LABEL_LARGE", theme_style=ft.TextThemeStyle.LABEL_LARGE),
        ft.Text("LABEL_MEDIUM", theme_style=ft.TextThemeStyle.LABEL_MEDIUM),
        ft.Text("LABEL_SMALL", theme_style=ft.TextThemeStyle.LABEL_SMALL),
        ft.Text("BODY_LARGE", theme_style=ft.TextThemeStyle.BODY_LARGE),
        ft.Text("BODY_MEDIUM", theme_style=ft.TextThemeStyle.BODY_MEDIUM),
        ft.Text("BODY_SMALL", theme_style=ft.TextThemeStyle.BODY_SMALL),
        Code(
            value="""
for i in range(100):
    print(i)
"""
        ),
        Code(
            value="""
{
"foo": "bar",
"baz": "boz",
"stuff": [
"stuff 1",
"stuff 2",
]
}
""",
            language="json",
        ),
        Markdown(
            markdown_str
            # on_tap_link=lambda e: page.launch_url(e.data),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
