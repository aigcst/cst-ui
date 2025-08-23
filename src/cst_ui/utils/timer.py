"""基于 flet_timer-master，集成 interval-timer模块"""

import asyncio
import threading
import traceback
from dataclasses import dataclass
from datetime import datetime
from time import perf_counter, sleep
from typing import Optional

import flet as ft


@dataclass
class Interval:
    index: int
    period: float
    _time_ready: float

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(index={self.index}, time={self.time:.03f}, lag={self.lag:.03f})'

    @property
    def time(self) -> float:
        """
        The start time of the interval, in seconds since the iterator object was created.
        """
        return self.index * self.period

    @property
    def end_time(self):
        """
        The end time of the interval, in seconds since the iterator object was created.
        """
        return self.time + self.period

    @property
    def buffer(self) -> float:
        """
        The length of time before the interval start time that the interval was requested. The minimum buffer is zero.
        """
        if self.time < self._time_ready:
            return 0
        return self.time - self._time_ready

    @property
    def lag(self) -> float:
        """
        The length of time after the interval start time that the interval was requested. The minimum lag is zero.

        If the lag is non-zero, then the code executed within the previous interval took longer than the interval
        period, which is generally undesirable.
        """
        if self._time_ready < self.time:
            return 0
        return self._time_ready - self.time


class IntervalTimer:
    # Affects timer precision, but also prevents high CPU usage
    CPU_SLEEP_S = 0.0001

    def _time(self) -> float:
        """
        Get the time relative to the interval timer starting, in seconds.
        """
        time_abs = perf_counter()

        # Set time 0 on first interval creation
        if self._time_zero is None:
            self._time_zero = time_abs

        return time_abs - self._time_zero

    def __init__(self, period: float, start: int = 0, stop: Optional[int] = None):
        """
        An interval timer iterator that synchronises iterations to within specific time intervals.

        The time taken for code execution within each iteration will not affect the interval timing, provided that the
        execution time is not longer than the interval period. The caller can check if this is the case by checking the
        `missed` attribute on the returned `Interval` instance.

        :param period: The interval period, in seconds.
        :param start: The number of iterations to delay starting by.
        :param stop: The number of iterations to automatically stop after.
        """
        self._period: float = period
        self._index: int = start
        self._stop: int = stop
        self._time_zero: Optional[int] = None

    def __iter__(self) -> 'IntervalTimer':
        return self

    async def __next__(self) -> Interval:
        if self._stop == self._index:
            raise StopIteration()

        interval = Interval(self._index, self._period, self._time())
        self._index += 1

        # Block the iteration until the interval begins
        while self._time() < interval.time:
            await asyncio.sleep(self.CPU_SLEEP_S)

        return interval


class Timer(ft.Container):
    def __init__(self, name='Timer', interval_s=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.interval_s = interval_s
        self.active = False
        self.th = threading.Thread(target=self.tick, daemon=True)
        self.padding = 0
        self.margin = 0
        self.content = ft.Text(value='None')

    def did_mount(self):
        self.start()
        self.th.start()

    def _refresh(self):
        self.content.value = datetime.now().strftime('%H:%M:%S')
        # self.update()

    def start(self):
        self.active = True

    def stop(self):
        self.active = False

    def tick(self):
        for _ in IntervalTimer(self.interval_s):
            if not self.active:
                break
            try:
                self._refresh()
            except Exception:
                print(f'Timer: {traceback.format_exc()}')

    def will_unmount(self):
        self.stop()
        super().will_unmount()


def demo():
    return ft.Column(controls=[Timer(name='timer', interval_s=1)])


def main(page: ft.Page):
    page.title = 'Timer'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(demo())

    page.update()


if __name__ == '__main__':
    ft.run(main)
