VERSION = "0.0.3"
# __flet_version__ = '0.0.3'
__author__ = "aigcst"
__email__ = "aigcst@outlook.com"
__url__ = "https://github.com/aigcst/cst-ui"
from flet import *

from .basic.app import (
    AddPageAdmin,
    App,
    AppKey,
    DataAdmin,
    EncryptAlgorithm,
    Job,
    KeyboardAdmin,
    PageAdmin,
    PemKey,
    Redirect,
    ResizeAdmin,
    ResponsiveControl,
    SecretKey,
    auto_routing,
    decode,
    decode_async,
    encode_HS256,
    encode_RS256,
    page,
)
from .basic.config import cfg
from .form.button import Button
from .layout.view import View


def main() -> None:
    print("Hello from cst_ui!")


if __name__ == "__main__":
    main()
