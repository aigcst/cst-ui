import calendar
import locale as loc
from datetime import datetime, timedelta

# 需要修改
from enum import Enum

import flet as ft


class SelectionType(Enum):
    SINGLE = 0
    MULTIPLE = 1
    RANGE = 2

    @staticmethod
    def from_value(value):
        return SelectionType(value)


class DatePicker(ft.Stack):
    @property
    def selected_data(self):
        return self.selected

    PREV_MONTH = "PM"
    NEXT_MONTH = "NM"
    PREV_YEAR = "PY"
    NEXT_YEAR = "NY"

    PREV_HOUR = "PH"
    NEXT_HOUR = "NH"
    PREV_MINUTE = "PMIN"
    NEXT_MINUTE = "NMIN"

    EMPTY = ""
    WHITE_SPACE = " "

    DELTA_MONTH_WEEK = 5
    DELTA_YEAR_WEEK = 52
    DELTA_HOUR = 1
    DELTA_MINUTE = 1

    WEEKEND_DAYS = [5, 6]

    CELL_SIZE = 32
    LAYOUT_WIDTH = 340
    LAYOUT_MIN_HEIGHT = 280
    LAYOUT_MAX_HEIGHT = 320
    LAYOUT_DT_MIN_HEIGHT = 320
    LAYOUT_DT_MAX_HEIGHT = 360

    def __init__(
        self,
        hour_minute: bool = False,
        selected_date=None,
        selection_type=SelectionType.SINGLE,
        disable_to: datetime = None,
        disable_from: datetime = None,
        holidays=None,
        hide_prev_next_month_days: bool = False,
        first_weekday: int = 0,
        show_three_months: bool = False,
        locale: str = None,
    ):
        super().__init__()
        self.selected = selected_date if selected_date else []
        self.selection_type = (
            selection_type
            if not type(int)
            else SelectionType.from_value(selection_type)
        )
        self.hour_minute = hour_minute
        self.disable_to = disable_to
        self.disable_from = disable_from
        self.holidays = holidays
        self.hide_prev_next_month_days = hide_prev_next_month_days
        self.first_weekday = first_weekday
        self.show_three_months = show_three_months
        if locale:
            loc.setlocale(loc.LC_ALL, locale)

        self.now = datetime.now()
        self.yy = self.now.year
        self.mm = self.now.month
        self.dd = self.now.day
        self.hour = self.now.hour
        self.minute = self.now.minute
        self.cal = calendar.Calendar(first_weekday)

    def _get_current_month(self, year, month):
        return self.cal.monthdatescalendar(year, month)

    def _create_calendar(self, year, month, hour, minute, hide_ymhm=False):
        week_rows_controls = []
        week_rows_days_controls = []
        today = datetime.now()

        days = self._get_current_month(year, month)

        ym = self._year_month_selectors(year, month, hide_ymhm)
        week_rows_controls.append(ft.Column([ym], alignment=ft.MainAxisAlignment.START))

        labels = ft.Row(self._row_labels(), spacing=18)
        week_rows_controls.append(
            ft.Column([labels], alignment=ft.MainAxisAlignment.START)
        )

        weeks_rows_num = len(self._get_current_month(year, month))

        for w in range(0, weeks_rows_num):
            row = []

            for d in days[w]:
                d = (
                    datetime(d.year, d.month, d.day, self.hour, self.minute)
                    if self.hour_minute
                    else datetime(d.year, d.month, d.day)
                )

                month = d.month
                is_main_month = True if month == self.mm else False

                if self.hide_prev_next_month_days and not is_main_month:
                    row.append(
                        ft.Text(
                            "",
                            width=self.CELL_SIZE,
                            height=self.CELL_SIZE,
                        )
                    )
                    continue

                dt_weekday = d.weekday()
                day = d.day
                is_weekend = False
                is_holiday = False

                is_day_disabled = False

                if self.disable_from and self._trunc_datetime(d) > self._trunc_datetime(
                    self.disable_from
                ):
                    is_day_disabled = True

                if self.disable_to and self._trunc_datetime(d) < self._trunc_datetime(
                    self.disable_to
                ):
                    is_day_disabled = True

                text_color = None
                border_side = None
                bg = None
                # week end bg color
                if dt_weekday in self.WEEKEND_DAYS:
                    text_color = ft.Colors.RED_500
                    is_weekend = True
                # holidays
                if self.holidays and d in self.holidays:
                    text_color = ft.Colors.RED_500
                    is_holiday = True

                # current day bg
                if (
                    is_main_month
                    and day == self.dd
                    and self.dd == today.day
                    and self.mm == today.month
                    and self.yy == today.year
                ):
                    border_side = ft.BorderSide(2, ft.Colors.BLUE)
                elif (is_weekend or is_holiday) and (
                    not is_main_month or is_day_disabled
                ):
                    text_color = ft.Colors.RED_200
                    bg = None
                elif not is_main_month and is_day_disabled:
                    text_color = ft.Colors.BLACK38
                    bg = None
                elif not is_main_month:
                    text_color = ft.Colors.BLUE_200
                    bg = None
                else:
                    bg = None

                # selected days
                selected_numbers = len(self.selected)
                if self.selection_type != SelectionType.RANGE:
                    if selected_numbers > 0 and d in self.selected:
                        bg = ft.Colors.BLUE_400
                        text_color = ft.Colors.WHITE
                else:
                    if (
                        selected_numbers > 0
                        and selected_numbers < 3
                        and d in self.selected
                    ):
                        bg = ft.Colors.BLUE_400
                        text_color = ft.Colors.WHITE

                if self.selection_type == SelectionType.RANGE and selected_numbers > 1:
                    if d > self.selected[0] and d < self.selected[-1]:
                        bg = ft.Colors.BLUE_300
                        text_color = ft.Colors.WHITE

                row.append(
                    ft.TextButton(
                        text=str(day),
                        data=d,
                        width=self.CELL_SIZE,
                        height=self.CELL_SIZE,
                        disabled=is_day_disabled,
                        style=ft.ButtonStyle(
                            color=text_color,
                            bgcolor=bg,
                            padding=0,
                            shape={
                                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                    radius=1
                                ),
                            },
                            side=border_side,
                        ),
                        on_click=self._select_date,
                    )
                )

            week_rows_days_controls.append(ft.Row(row, spacing=18))

        week_rows_controls.append(
            ft.Column(
                week_rows_days_controls, alignment=ft.MainAxisAlignment.START, spacing=0
            )
        )

        if self.hour_minute and not hide_ymhm:
            hm = self._hour_minute_selector(hour, minute)
            week_rows_controls.append(
                ft.Row([hm], alignment=ft.MainAxisAlignment.CENTER)
            )

        return week_rows_controls

    def _year_month_selectors(self, year, month, hide_ymhm=False):
        prev_year = (
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS,
                data=self.PREV_YEAR,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else ft.Text(
                self.EMPTY,
                height=self.CELL_SIZE,
            )
        )
        next_year = (
            ft.IconButton(
                icon=ft.Icons.ARROW_FORWARD_IOS,
                data=self.NEXT_YEAR,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else ft.Text(self.EMPTY)
        )
        prev_month = (
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS,
                data=self.PREV_MONTH,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else ft.Text(self.EMPTY)
        )
        next_month = (
            ft.IconButton(
                icon=ft.Icons.ARROW_FORWARD_IOS,
                data=self.NEXT_MONTH,
                on_click=self._adjust_calendar,
            )
            if not hide_ymhm
            else ft.Text(self.EMPTY)
        )
        ym = ft.Row(
            [
                ft.Row(
                    [
                        prev_year,
                        ft.Text(year),
                        next_year,
                    ],
                    spacing=0,
                ),
                ft.Row(
                    [
                        prev_month,
                        ft.Text(
                            calendar.month_name[month], text_align=ft.alignment.center
                        ),
                        next_month,
                    ],
                    spacing=0,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return ym

    def _row_labels(self):
        label_row = []
        days_label = calendar.weekheader(2).split(self.WHITE_SPACE)
        for i in range(0, self.first_weekday):
            days_label.append(days_label.pop(0))
        for _ in days_label:
            label_row.append(
                ft.TextButton(
                    text=_,
                    width=self.CELL_SIZE,
                    height=self.CELL_SIZE,
                    disabled=True,
                    style=ft.ButtonStyle(
                        padding=0,
                        color=ft.Colors.GREY_500,
                        # bgcolor=ft.Colors.GREY_300,
                        shape={
                            ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                radius=1
                            ),
                        },
                    ),
                )
            )

        return label_row

    def _hour_minute_selector(self, hour, minute):
        hm = ft.Row(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            data=self.PREV_HOUR,
                            on_click=self._adjust_hh_min,
                        ),
                        ft.Text(hour),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            data=self.NEXT_HOUR,
                            on_click=self._adjust_hh_min,
                        ),
                    ]
                ),
                ft.Text(":"),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            data=self.PREV_MINUTE,
                            on_click=self._adjust_hh_min,
                        ),
                        ft.Text(minute),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            data=self.NEXT_MINUTE,
                            on_click=self._adjust_hh_min,
                        ),
                    ]
                ),
            ],
            spacing=48,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

        return hm

    def build(self):
        rows = self._create_layout(self.yy, self.mm, self.hour, self.minute)

        cal_height = self._calculate_heigth(self.yy, self.mm)

        self.cal_container = ft.Container(
            content=ft.Row(rows),
            bgcolor=ft.Colors.WHITE,
            padding=12,
            height=self._cal_height(cal_height),
        )
        return self.cal_container

    def _calculate_heigth(self, year, month):
        if self.show_three_months:
            prev, next = self._prev_next_month(year, month)
            cal_height = max(
                len(self._get_current_month(year, month)),
                len(self._get_current_month(prev.year, prev.month)),
                len(self._get_current_month(next.year, next.month)),
            )
        else:
            cal_height = len(self._get_current_month(year, month))
        return cal_height

    def _create_layout(self, year, month, hour, minute):
        rows = []
        prev, next = self._prev_next_month(year, month)

        if self.show_three_months:
            week_rows_controls_prev = self._create_calendar(
                prev.year, prev.month, hour, minute, True
            )
            rows.append(
                ft.Column(week_rows_controls_prev, width=self.LAYOUT_WIDTH, spacing=10)
            )
            rows.append(ft.VerticalDivider())

        week_rows_controls = self._create_calendar(year, month, hour, minute)
        rows.append(ft.Column(week_rows_controls, width=self.LAYOUT_WIDTH, spacing=10))

        if self.show_three_months:
            rows.append(ft.VerticalDivider())
            week_rows_controls_next = self._create_calendar(
                next.year, next.month, hour, minute, True
            )
            rows.append(
                ft.Column(week_rows_controls_next, width=self.LAYOUT_WIDTH, spacing=10)
            )

        return rows

    def _prev_next_month(self, year, month):
        delta = timedelta(weeks=self.DELTA_MONTH_WEEK)
        current = datetime(year, month, 15)
        prev = current - delta
        next = current + delta
        return prev, next

    def _select_date(self, e: ft.ControlEvent):
        result: datetime = e.control.data

        if self.selection_type == SelectionType.RANGE:
            if len(self.selected) == 2:
                self.selected = []

            if len(self.selected) > 0:
                if self.selected[0] == result:
                    self.selected = []
                else:
                    if result > self.selected[0]:
                        if len(self.selected) == 1:
                            self.selected.append(result)
                        else:
                            return
                    else:
                        return
            else:
                self.selected.append(result)
        elif self.selection_type == SelectionType.MULTIPLE:
            if len(self.selected) > 0 and result in self.selected:
                self.selected.remove(result)
            else:
                if self.hour_minute:
                    result = datetime(
                        result.year, result.month, result.day, self.hour, self.minute
                    )
                self.selected.append(result)
        else:
            if len(self.selected) == 1 and result in self.selected:
                self.selected.remove(result)
            else:
                self.selected = []
                if self.hour_minute:
                    result = datetime(
                        result.year, result.month, result.day, self.hour, self.minute
                    )
                self.selected.append(result)

        self._update_calendar()

    def _adjust_calendar(self, e: ft.ControlEvent):
        if e.control.data == self.PREV_MONTH or e.control.data == self.NEXT_MONTH:
            delta = timedelta(weeks=self.DELTA_MONTH_WEEK)
        if e.control.data == self.PREV_YEAR or e.control.data == self.NEXT_YEAR:
            delta = timedelta(weeks=self.DELTA_YEAR_WEEK)

        if e.control.data == self.PREV_MONTH or e.control.data == self.PREV_YEAR:
            self.now = self.now - delta
        if e.control.data == self.NEXT_MONTH or e.control.data == self.NEXT_YEAR:
            self.now = self.now + delta

        self.mm = self.now.month
        self.yy = self.now.year
        self._update_calendar()

    def _adjust_hh_min(self, e: ft.ControlEvent):
        if e.control.data == self.PREV_HOUR or e.control.data == self.NEXT_HOUR:
            delta = timedelta(hours=self.DELTA_HOUR)
        if e.control.data == self.PREV_MINUTE or e.control.data == self.NEXT_MINUTE:
            delta = timedelta(minutes=self.DELTA_MINUTE)

        if e.control.data == self.PREV_HOUR or e.control.data == self.PREV_MINUTE:
            self.now = self.now - delta
        if e.control.data == self.NEXT_HOUR or e.control.data == self.NEXT_MINUTE:
            self.now = self.now + delta

        self.hour = self.now.hour
        self.minute = self.now.minute
        self._update_calendar()

    def _update_calendar(self):
        self.cal_container.content = ft.Row(
            self._create_layout(self.yy, self.mm, self.hour, self.minute)
        )
        cal_height = self._calculate_heigth(self.yy, self.mm)
        self.cal_container.height = self._cal_height(cal_height)
        self.update()

    def _cal_height(self, weeks_number):
        if self.hour_minute:
            return (
                self.LAYOUT_DT_MIN_HEIGHT
                if weeks_number == 5
                else self.LAYOUT_DT_MAX_HEIGHT
            )
        else:
            return (
                self.LAYOUT_MIN_HEIGHT if weeks_number == 5 else self.LAYOUT_MAX_HEIGHT
            )

    def _trunc_datetime(self, date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)


from datetime import datetime


class Example(ft.Column):
    def __init__(self):
        super().__init__()

        self.datepicker = None
        self.holidays = [
            datetime(2023, 4, 25),
            datetime(2023, 5, 1),
            datetime(2023, 6, 2),
        ]
        self.locales = ["en_US", "fr_FR", "it_IT", "es_ES", "zh_CN"]
        self.selected_locale = None

        self.locales_opts = []
        for _ in self.locales:
            self.locales_opts.append(ft.dropdown.Option(_))

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Date picker"),
            actions=[
                ft.TextButton("关闭", on_click=self.cancel_dlg),
                ft.TextButton("确认", on_click=self.confirm_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=5,
            content_padding=0,
        )

        self.tf = ft.TextField(
            label="选择日期",
            dense=True,
            hint_text="yyyy-mm-ddThh:mm:ss",
            width=260,
            height=40,
        )
        self.cal_ico = ft.TextButton(
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.open_dlg_modal,
            height=40,
            width=40,
            right=0,
            style=ft.ButtonStyle(
                padding=ft.Padding(4, 0, 0, 0),
                shape={
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=1),
                },
            ),
        )

        self.st = ft.Stack(
            [
                self.tf,
                self.cal_ico,
            ]
        )

        self.cg = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Text("Selction Type"),
                    ft.Radio(
                        value=SelectionType.SINGLE.value,
                        label=SelectionType.SINGLE.name,
                    ),
                    ft.Radio(
                        value=SelectionType.RANGE.value, label=SelectionType.RANGE.name
                    ),
                    ft.Radio(
                        value=SelectionType.MULTIPLE.value,
                        label=SelectionType.MULTIPLE.name,
                    ),
                ]
            ),
            value=SelectionType.SINGLE.value,
        )
        self.c1 = ft.Switch(label="With hours and minutes", value=False)
        self.tf1 = ft.TextField(
            label="Disable days until date",
            dense=True,
            hint_text="yyyy-mm-dd hh:mm:ss",
            width=260,
            height=40,
        )
        self.tf2 = ft.TextField(
            label="Disable days from date",
            dense=True,
            hint_text="yyyy-mm-dd hh:mm:ss",
            width=260,
            height=40,
        )
        self.c2 = ft.Switch(
            label="Hide previous and next month days from current", value=False
        )
        self.c3 = ft.Switch(label="Shows three months", value=False)

        self.dd = ft.Dropdown(
            label="Locale",
            width=200,
            options=self.locales_opts,
            dense=True,
            on_change=self.set_locale,
        )

        self.from_to_text = ft.Text(visible=False)

        self.controls = [
            ft.Text("Datepicker options", size=24),
            ft.Divider(),
            self.cg,
            self.c1,
            self.c2,
            self.c3,
            ft.Row(
                [
                    self.tf1,
                    self.tf2,
                ]
            ),
            self.dd,
            ft.Divider(),
            self.st,
            self.from_to_text,
        ]

    def confirm_dlg(self, e):
        if int(self.cg.value) == SelectionType.SINGLE.value:
            self.tf.value = (
                self.datepicker.selected_data[0]
                if len(self.datepicker.selected_data) > 0
                else None
            )
        elif (
            int(self.cg.value) == SelectionType.MULTIPLE.value
            and len(self.datepicker.selected_data) > 0
        ):
            self.from_to_text.value = (
                f"{[d.isoformat() for d in self.datepicker.selected_data]}"
            )
            self.from_to_text.visible = True
        elif (
            int(self.cg.value) == SelectionType.RANGE.value
            and len(self.datepicker.selected_data) > 0
        ):
            self.from_to_text.value = f"From: {self.datepicker.selected_data[0]} To: {self.datepicker.selected_data[1]}"
            self.from_to_text.visible = True
        self.dlg_modal.open = False
        self.update()
        self.page.update()

    def cancel_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def open_dlg_modal(self, e):
        self.datepicker = DatePicker(
            hour_minute=self.c1.value,
            selected_date=[self.tf.value] if self.tf.value else None,
            selection_type=int(self.cg.value),
            disable_to=self._to_datetime(self.tf1.value),
            disable_from=self._to_datetime(self.tf2.value),
            hide_prev_next_month_days=self.c2.value,
            holidays=self.holidays,
            show_three_months=self.c3.value,
            locale=self.selected_locale,
        )
        self.dlg_modal.content = self.datepicker
        self.page.open(self.dlg_modal)

    def _to_datetime(self, date_str=None):
        if date_str:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        else:
            return None

    def set_locale(self, e):
        self.selected_locale = self.dd.value if self.dd.value else None


def demo():
    return ft.Column(controls=[Example()])


def main(page: ft.Page):
    page.add(demo())


if __name__ == "__main__":
    ft.run(main)
