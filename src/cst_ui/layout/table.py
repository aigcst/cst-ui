"""
表格组件，具备：
1. 分页
2. 样式
3. 搜索
支持多种列类型：Text、Number、CheckBox、SelectBox、Datetime、Date、Time、List、Link、Image、Line、BarChart、Progress
"""

import copy
import random
from dataclasses import dataclass
from typing import Any

import flet as ft

import cst_ui as ui


@dataclass
class Table(ft.Column):
    """
    通用表格组件，支持分页、编号列、样式自定义等功能。
    """

    DEFAULT_ROW_PER_PAGE: int = 10  # 默认每页行数
    data_table: ft.DataTable | None = None  # 输入的 DataTable 对象
    rows_per_page: int = DEFAULT_ROW_PER_PAGE  # 每页显示的行数
    with_paged: bool = True  # 是否启用分页
    init_width: int | None = None  # 初始宽度
    with_number: bool = True  # 是否显示编号列

    def __post_init__(self, ref: ft.Ref[Any] | None):
        # 深拷贝输入的 DataTable，避免外部数据被修改
        self.input_data_table = copy.deepcopy(self.data_table)
        self.init_data_per_page_nums = self.rows_per_page
        self.current_page = 1

        # 分页控件的边距
        self.paged_padding_left = 20
        self.paged_padding_right = 20
        self.paged_padding_top = 10
        self.paged_padding_bottom = 10

        # 分页控件
        self.v_paging = ui.Paging(sum_data_nums=self.num_rows, on_change_page=self.set_page)

        # Flet DataTable 控件
        self.ft_data_table = ft.DataTable(
            columns=self.input_data_table.columns,
            rows=self.build_rows(),
            heading_row_color='#f4f4f4',
            sort_column_index=2,
            horizontal_lines=ft.BorderSide(1, '#EDEEF4'),
            border=ft.Border.all(1, '#eeeeee'),
            expand=self.expand,
            width=10000,
        )

        # 表格外层卡片
        self.v_row_table = ft.Card(
            ft.Container(
                content=self.ft_data_table,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, ft.Colors.GREY_400),
            ),
        )

        # 组装最终视图
        if self.with_paged:
            self.ui_view = ft.Card(
                content=ft.Container(
                    content=ft.Column([self.v_row_table, self.v_paging], scroll=ft.ScrollMode.AUTO),
                    padding=ft.Padding.only(
                        left=self.paged_padding_left,
                        right=self.paged_padding_right,
                        top=self.paged_padding_top,
                        bottom=self.paged_padding_bottom,
                    ),
                    bgcolor=ft.Colors.WHITE,
                ),
                elevation=2,
            )
        else:
            self.ui_view = self.v_row_table

        self.controls = [self.ui_view]
        super().__post_init__(ref)

    @property
    def data_per_page_nums(self) -> int:
        """每页数据条数（由分页控件决定）"""
        return self.v_paging.data_per_page_nums

    @property
    def num_rows(self) -> int:
        """表格总行数"""
        return len(self.input_data_table.rows)

    @property
    def num_pages(self) -> int:
        """总页数"""
        return self.v_paging.sum_page_nums

    @property
    def data_columns(self):
        """表格所有列"""
        return self.ft_data_table.columns

    @property
    def data_rows(self):
        """表格所有行"""
        return self.input_data_table.rows

    def update_data_table(self, data_table=None):
        """
        更新表格数据和列定义
        """
        if data_table is not None:
            self.input_data_table = data_table
        self.ft_data_table.columns = self.input_data_table.columns

        # 自动添加编号列
        if (
            self.with_number
            and len(self.ft_data_table.columns) >= 1
            and self.ft_data_table.columns[0].label.value != '编号'
        ):
            self.ft_data_table.columns.insert(0, ft.DataColumn(label=ft.Text('编号')))
        self.refresh_data()

    def set_page(self, page: str | int | None = None, delta: int = 0):
        """
        设置当前页码，支持直接指定页码或增量跳转
        """
        if page is not None:
            try:
                page_int = int(page)
                self.current_page = page_int if 1 <= page_int <= self.num_pages else 1
            except ValueError:
                self.current_page = 1
        elif delta:
            self.current_page += delta
        else:
            return
        self.refresh_data()

    def build_rows(self) -> list:
        """
        构建当前页的数据行
        """
        if self.with_paged:
            index_start = (self.current_page - 1) * self.data_per_page_nums
            index_end = self.current_page * self.data_per_page_nums
        else:
            index_start = 0
            index_end = -1

        rst_rows = []
        # 遍历当前页的数据行
        for idx, row in enumerate(self.input_data_table.rows[slice(index_start, index_end)]):
            # 自动补充编号列
            if self.with_number and (len(row.cells) < len(self.input_data_table.columns)):
                row.cells.insert(0, ft.DataCell(ft.Text(index_start + idx + 1)))
            # 设置悬浮颜色
            row.color = {ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ft.Colors.BLUE)}
            # 行选中事件（可自定义）
            row.on_select_changed = lambda e: e
            rst_rows.append(row)
        return rst_rows

    def refresh_data(self):
        """
        刷新表格数据和分页控件
        """
        self.ft_data_table.rows = self.build_rows()
        self.v_paging.update_sum_data_nums(value=self.num_rows)

    def did_mount(self):
        """
        组件挂载时自动刷新数据
        """
        self.update_data_table(self.input_data_table)


def demo():
    """
    表格控件演示
    """
    rows = []
    for i in range(200):
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text('John')),
                    ft.DataCell(ft.Text('Smith')),
                    ft.DataCell(ft.Text(str(random.random()))),
                ]
            )
        )
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text('First name')),
            ft.DataColumn(label=ft.Text('Last name')),
            ft.DataColumn(label=ft.Text('Age'), numeric=True),
        ],
        rows=rows,
    )
    print(f'Table: {len(data_table.rows)}')

    return ft.Column(controls=[Table(data_table=data_table, rows_per_page=10, with_paged=True)])


def main(page: ft.Page):
    page.title = 'Table'
    page.scroll = ft.ScrollMode.AUTO
    page.add(demo())


if __name__ == '__main__':
    ft.run(main)
