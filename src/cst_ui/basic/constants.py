'''常量和类型定义'''

# 考虑TypedDict做自定义参数
from enum import Enum


class RUN_MODE(Enum):
    DEV = 'dev'
    TEST = 'test'
    RELEASE = 'release'
