from typing import (
    TYPE_CHECKING,
    Awaitable,
    Callable,
    Generic,
    ParamSpec,
    Type,
    TypeVar,
    cast,
    overload,
)

from near.types import RPCEndpoint

if TYPE_CHECKING:
    from near.main import AsyncNear, Near


R = TypeVar("R")
P = ParamSpec("P")


class Method(Generic[P, R]):
    def __init__(
        self,
        json_rpc_method: RPCEndpoint,
        result_key: str,
    ):
        self.json_rpc_method = json_rpc_method
        self.result_key = result_key

    @overload
    def __get__(
        self,
        obj: "Near",
        obj_type: Type["Near"],
    ) -> Callable[P, R]:
        ...

    @overload
    def __get__(
        self,
        obj: "AsyncNear",
        obj_type: Type["AsyncNear"],
    ) -> Callable[P, Awaitable[R]]:
        ...

    def __get__(
        self,
        obj: "Near | AsyncNear",
        obj_type: Type["Near"] | Type["AsyncNear"],
    ) -> Callable[P, R] | Callable[P, Awaitable[R]]:
        from near.main import AsyncNear, Near

        if isinstance(obj, Near):

            def caller(*args: P.args, **kwargs: P.kwargs) -> R:

                response = cast(Near, obj).provider.post(
                    self.json_rpc_method, params=[*args]
                )
                result = response["result"][self.result_key]
                return cast(R, result)

            return caller
        elif isinstance(obj, AsyncNear):

            async def async_caller(*args: P.args, **kwargs: P.kwargs) -> R:
                response = await cast(AsyncNear, obj).provider.post(
                    self.json_rpc_method, params=[*args]
                )
                result = response["result"][self.result_key]
                return cast(R, result)

            return async_caller
        else:
            raise ValueError("No way...")
