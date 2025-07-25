from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Deque, Union

from flet import Page, View, KeyboardEvent

from .my_types import Msg, Redirect
from .my_types import (
    SecretKey,
    _decode_payload_async,
    encode_verified,
)
from .inheritance import KeyboardAdmin, ResizeAdmin, SessionStorageEdit

from .my_types import Job


class DataAdmin:
    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: str,
        secret_key: str,
        auto_logout: bool,
        page_on_keyboard: KeyboardEvent,
        page_on_resize: ResizeAdmin,
        login_async: bool = False,
        go: Callable[[str], None] | None = None,
    ) -> None:
        """程序层面数据管理

        Args:
            page (Page): flet提供的Page
            route_prefix (str): 路由前缀
            route_init (str): 初始路由
            route_login (str): 登录路由
            secret_key (str): 密钥
            auto_logout (bool): 是否自动退出登录
            page_on_keyboard (KeyboardAdmin): 该页面的按键
            page_on_resize (ResizeAdmin): 该页面resize的动作
            login_async (bool, optional): _description_. Defaults to False.
            go (Callable[[str], None], optional): _description_. Defaults to None.
        """
        self.__page: Page = page
        self.__url_params: Dict[str, Any] | None = None
        self.__view: View | None = None
        self.__route_prefix = route_prefix
        self.__route_init = route_init
        self.__route_login = route_login
        self.__share = SessionStorageEdit()
        self.__on_keyboard_event = page_on_keyboard
        self.__on_resize = page_on_resize
        self.__route: str | None = None
        self.__go = go
        self.__history_routes: deque[str] = deque()

        self.__secret_key: SecretKey = secret_key
        self.__auto_logout: bool = auto_logout
        self.__sleep: int = 1
        self._key_login: str | None = None
        self._login_done: bool = False
        self._login_async: bool = login_async

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, page: object):
        self.__page = page

    @property
    def history_routes(self):
        return self.__history_routes

    @history_routes.setter
    def history_routes(self, history_routes: Deque[str]):
        self.__history_routes = history_routes

    @property
    def url_params(self):
        return self.__url_params

    @url_params.setter
    def url_params(self, url_params: Dict[str, Any]):
        self.__url_params = url_params

    @property
    def view(self):
        return self.__view

    @view.setter
    def view(self, view: View):
        self.__view = view

    @property
    def route_prefix(self):
        return self.__route_prefix

    @route_prefix.setter
    def route_prefix(self, route_prefix: str):
        self.__route_prefix = route_prefix

    @property
    def route_init(self):
        return self.__route_init

    @route_init.setter
    def route_init(self, route_init: str):
        self.__route_init = route_init

    @property
    def route_login(self):
        return self.__route_login

    @route_login.setter
    def route_login(self, route_login: str):
        self.__route_login = route_login

    @property
    def share(self):
        return self.__share

    # events
    @property
    def on_keyboard_event(self) -> KeyboardEvent:
        return self.__on_keyboard_event

    @on_keyboard_event.setter
    def on_keyboard_event(self, on_keyboard_event: KeyboardEvent):
        self.__on_keyboard_event = on_keyboard_event

    @property
    def on_resize(self):
        return self.__on_resize

    @on_resize.setter
    def on_resize(self, on_resize: object):
        self.__on_resize = on_resize

    @property
    def key_login(self):
        return self._key_login

    @property
    def auto_logout(self):
        return self.__auto_logout

    @property
    def secret_key(self):
        return self.__secret_key

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, route: str):
        self.__route = route

    """--------- login authentication : asynchronously | synchronously -------"""

    def _login_done_evaluate(self):
        return self._login_done

    def _create_task_login_update(self, decode: Dict[str, Any]):
        """Updates the login status, in case it does not exist it creates a new task that checks the user's login status."""
        time_exp = datetime.fromtimestamp(float(decode.get("exp")), tz=timezone.utc)
        time_now = datetime.now(tz=timezone.utc)
        time_res = time_exp - time_now
        self._login_done = True
        Job(
            func=self.logout,
            key=self.key_login,
            every=time_res,
            page=self.page,
            login_done=self._login_done_evaluate,
            sleep_time=self.__sleep,
        ).start()

    def logout(self, key: str):
        """Closes the sessions of all browser tabs or the device used, which has been previously configured with the `login` method.

        ### Example:
        ```python
        import flet as ft
        import flet_app as fs

        @app.page('/Dashboard', title='Dashboard', protected_route=True)
        def dashboard(data:fs.DataAdmin)
            return ft.View(
                controls=[
                    ft.FilledButton('Logout', onclick=data.logout('key-login')),
            )
        ```
        """

        def execute(key: str):
            assert self.route_login is not None, "Adds a login path in the FletApp Class"
            if self.page.web:
                self.page.pubsub.send_all_on_topic(
                    self.page.client_ip + self.page.client_user_agent, Msg("logout", key)
                )
            else:
                self.page.run_task(self.page.client_storage.remove_async, key)
                self.page.go(self.route_login)

        return lambda _=None: execute(key)

    async def __logaut_init(self, topic, msg: Msg):
        if msg.method == "login":
            await self.page.client_storage.set_async(msg.key, msg.value.get("value"))
            if self.page.route == self.route_login:
                self.page.go(msg.value.get("next_route"))

        elif msg.method == "logout":
            self._login_done = False
            await self.page.client_storage.remove_async(msg.key)
            self.page.go(self.route_login)

        elif msg.method == "updateLogin":
            self._login_done = msg.value

        elif msg.method == "updateLoginSessions":
            self._login_done = msg.value
            self._create_task_login_update(
                decode=await _decode_payload_async(
                    page=self.page,
                    key_login=self.key_login,
                    secret_key=(
                        self.secret_key.secret if self.secret_key.secret is not None else self.secret_key.pem_key.public
                    ),
                    algorithms=self.secret_key.algorithm,
                )
            )
        else:
            raise ValueError("Method not implemented in logout_init method.")

    def _create_login(self):
        """Create the connection between sessions."""
        if self.page.web:
            self.page.pubsub.subscribe_topic(self.page.client_ip + self.page.client_user_agent, self.__logaut_init)

    def _create_tasks(self, time_expiry: timedelta, key: str, sleep: int) -> None:
        """Creates the logout task when logging in."""
        if time_expiry is not None:
            Job(
                func=self.logout,
                key=key,
                every=time_expiry,
                page=self.page,
                login_done=self._login_done_evaluate,
                sleep_time=sleep,
            ).start()

    def login(
        self,
        key: str,
        value: Union[Dict[str, Any], Any],
        next_route: str,
        time_expiry: timedelta = None,
        sleep: int = 1,
    ):
        """Registering in the client's storage the key and value in all browser sessions.

        ### Parameters to use:

        * `key` : It is the identifier to store the value in the client storage.
        * `value` : Recommend to use a dict if you use JWT.
        * `next_route` : Redirect to next route after creating login.
        * `time_expiry` : Time to expire the session, use the `timedelta` class  to configure. (Optional)
        * `sleep` : Time to do login checks, default is 1s. (Optional)
        """
        if time_expiry:
            assert isinstance(value, Dict), "Use a dict in login method values or don't use time_expiry."
            assert (
                self.__secret_key is not None
            ), "Set the secret_key in the FletApp class parameter or don't use time_expiry."

        if self.__secret_key:
            evaluate_secret_key(self)
            self._key_login = key
            self.__sleep = sleep
            value = encode_verified(self.secret_key, value, time_expiry)
            self._login_done = True

            if self.__auto_logout:
                self._create_tasks(time_expiry, key, sleep)

        self.page.run_task(self.page.client_storage.set_async, key, value).result()

        if self.page.web:
            self.page.pubsub.send_others_on_topic(
                self.page.client_ip + self.page.client_user_agent,
                Msg("login", key, {"value": value, "next_route": next_route}),
            )
        self.__go(next_route)

    """ Page go  """

    def go(self, route: str):
        """To change the application path, it is important for better validation to avoid using `page.go()`."""
        return lambda _=None: self.__go(route)

    def redirect(self, route: str):
        """Useful if you do not want to access a route that has already been sent."""
        return Redirect(route)

    def go_back(self):
        """Go back to the previous route."""
        return lambda _=None: (
            (self.history_routes.pop(), self.__go(self.history_routes.pop()))
            if len(self.history_routes) > 1
            else (print("-> I can't go back! There is no route history."), None)
        )


def evaluate_secret_key(data: DataAdmin):
    assert (
        data.secret_key.secret is None
        and data.secret_key.algorithm == "RS256"
        or data.secret_key.pem_key is None
        and data.secret_key.algorithm == "HS256"
    ), "The algorithm is not set correctly in the 'secret_key' parameter of the 'FletApp' class."
