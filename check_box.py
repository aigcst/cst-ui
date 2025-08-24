from dataclasses import dataclass, field
from typing import Any, List

import flet as ft

from cst_ui.basic.theme import theme


@dataclass
class CheckBox(ft.CupertinoCheckbox):
    """
    单个复选框，继承自 Flet 的 CupertinoCheckbox，设置主题色和样式。
    """

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.check_color = ft.Colors.WHITE  # 勾选标记颜色
        self.active_color = theme.color.primary  # 选中时的填充色
        self.padding = ft.Padding.all(0)  # 去除内边距
        return super().__post_init__(ref)


@dataclass
class CheckBoxGroup(ft.Container):
    """
    多选框组，支持全选和单独选择。
    """

    options: List[str] = field(default_factory=list)  # 选项列表

    def __post_init__(self, ref: ft.Ref[Any] | None):
        self.selected_list = []  # 当前选中的选项
        # 全选复选框
        self.check_all = CheckBox(label='全选', on_change=self.change_all)
        # 组装所有复选框控件
        self.check_box_controls = [
            self.check_all,
            ft.Divider(),
        ]
        for option in self.options:
            self.check_box_controls.append(CheckBox(label=option, on_change=self.change_single))
        # 布局设置
        self.content = ft.Column(self.check_box_controls, spacing=0, alignment=ft.MainAxisAlignment.START)
        self.width = 300
        self.tight = True
        self.padding = ft.Padding.all(0)
        return super().__post_init__(ref)

    @property
    def value(self) -> List[str]:
        """获取当前选中的选项列表"""
        return self.selected_list

    def change_single(self, e):
        """
        单个复选框变更事件。
        勾选则加入 selected_list，取消则移除。
        同步全选框状态。
        """
        val = e.control.label
        if e.data:
            if val not in self.selected_list:
                self.selected_list.append(val)
        else:
            if val in self.selected_list:
                self.selected_list.remove(val)
        # 同步全选框状态
        self.check_all.value = len(self.selected_list) == len(self.options)

    def change_all(self, e):
        """
        全选复选框变更事件。
        勾选则所有选项都选中，取消则全部取消。
        """
        self.check_all.tristate = False  # 禁用三态
        val = self.check_all.value
        # 遍历所有子复选框，设置为全选或全不选
        for i in range(2, len(self.check_box_controls)):
            self.check_box_controls[i].value = val
        self.selected_list = self.options.copy() if val else []


def demo(page: ft.Page):
    """
    复选框控件演示。
    """

    def on_change(e):
        page.add(ft.Text(f'value changed to {v_check_box.value}'))

    def on_click(e):
        v_text.value = str(v_check_box_group.value)

    v_check_box = CheckBox(
        label='Text CheckBox',
        on_change=on_change,
        width=200,
    )
    v_text = ft.Text()
    v_check_box_group = CheckBoxGroup(options=['多选1', '多选2', '多选3', '多选4', '多选5'])

    return ft.Column(
        controls=[
            v_check_box,
            ft.ElevatedButton(ft.Text(value='获取值'), on_click=on_click),
            v_text,
            v_check_box_group,
        ]
    )


def main(page: ft.Page):
    page.add(demo(page=page))


if __name__ == '__main__':
    ft.run(main)
