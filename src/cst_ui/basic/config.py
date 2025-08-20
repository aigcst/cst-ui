"""界面基本配置"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from .constants import RUN_MODE


def setup_filesize_logger(
    log_file: Path, name="cst_ui", run_mode: Optional[RUN_MODE] = None
) -> logging.Logger:
    """创建基于日志大小的日志器

    Arguments:
        log_file {rstr} -- 日志保存的文件

    Keyword Arguments:
        name {str} -- 日志器的名称 (default: {'cst_ui'})
        log_level {int} -- 日志器的级别 (default: {logging.DEBUG})

    Returns:
        logger -- 创建的日志器
    """
    # 创建logger
    my_logger = logging.getLogger(name)
    # 设置输出格式
    formatter = logging.Formatter(
        # 时间 文件名 文件行号 函数名 日志等级 输出的信息
        # fmt="[%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d:%(funcName)s]:%(levelname)s: %(message)s",
        fmt="%(asctime)s.%(msecs)03d | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if run_mode == RUN_MODE.DEV:
        # 开发模式增强日志，并设置日志器输出到print流
        log_level = logging.DEBUG
        print_stream = logging.StreamHandler()
        print_stream.setFormatter(formatter)
        my_logger.addHandler(print_stream)
    elif run_mode == RUN_MODE.TEST:
        # 测试模式输出重要日志日志，并设置日志器输出到print流
        log_level = logging.INFO
        print_stream = logging.StreamHandler()
        print_stream.setFormatter(formatter)
        my_logger.addHandler(print_stream)
    else:
        log_level = logging.INFO
    my_logger.setLevel(log_level)

    # 基于文件大小的handler
    filesize_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        mode="a",
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    filesize_handler.setFormatter(formatter)
    my_logger.addHandler(filesize_handler)

    return my_logger


class CFG:
    def __init__(self) -> None:
        # 项目根目录
        self.root_dir = Path(__file__).parents[2]
        self.run_mode = RUN_MODE.DEV
        # 输出文件夹：图像效果、日志等
        self.output_dir = Path(self.root_dir, "output")
        self.log_dir = Path(self.root_dir, "output", "log")
        self.log_dir.mkdir(exist_ok=True, parents=True)
        self.logger = setup_filesize_logger(
            log_file=Path(self.log_dir, "ui.log"), run_mode=self.run_mode
        )
        self.language = "zh_CN"
        # 简体中文	zh_CN
        # 繁体中文	zh_TW
        # 英语	en_US
        # 韩语	ko_KR
        # 日语	ja_JP
        # 俄语	ru_RU
        # 意大利语	it_IT
        # 阿拉伯语	ar_KW

    def __repr__(self):
        return f"""
- {self.output_dir=}
- {self.log_dir=}
"""

    def get(self, key_name):
        pass

    def set(self, key_name, value):
        pass


cfg = CFG()
if __name__ == "__main__":
    print(cfg)
