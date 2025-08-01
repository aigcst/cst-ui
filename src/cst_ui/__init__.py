VERSION = '0.0.3'
# __flet_version__ = '0.0.3'
__author__ = 'aigcst'
__email__ = 'aigcst@outlook.com'
__url__ = 'https://github.com/aigcst/cst-ui'
from .basic.app import (
    App,
    page,
    DataAdmin,
    AddPageAdmin,
    PageAdmin,
    Redirect,
    EncryptAlgorithm,
    PemKey,
    SecretKey,
    encode_HS256,
    encode_RS256,
    Job,
    KeyboardAdmin,
    ResizeAdmin,
    ResponsiveControl,
    AppKey,
    decode,
    decode_async,
    auto_routing,
)
from .basic.config import cfg
from .form.button import Button


from .layout.view import View


def main() -> None:
    print("Hello from cst_ui!")


if __name__ == "__main__":
    main()
