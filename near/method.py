from typing import (
    TYPE_CHECKING,
    Awaitable,
    Callable,
    Generic,
    Type,
    TypeVar,
    cast,
    overload,
)

from near.types import ResultSchemaT, RPCEndpoint

if TYPE_CHECKING:
    from near.main import AsyncNear, Near


ResultT = TypeVar("ResultT")
ParamsT = TypeVar("ParamsT")


class Method(Generic[ParamsT, ResultT]):
    def __init__(
        self,
        base_method: RPCEndpoint,
        result_schema: Type[ResultSchemaT],
        result_formatter: Callable[[ResultSchemaT], ResultT],
    ):
        self.result_schema = result_schema
        self.base_method = base_method
        self.result_formatter = result_formatter

    @overload
    def __get__(
        self,
        obj: "Near",
        obj_type: Type["Near"],
    ) -> Callable[[ParamsT], ResultT]:
        ...

    @overload
    def __get__(
        self,
        obj: "AsyncNear",
        obj_type: Type["AsyncNear"],
    ) -> Callable[[ParamsT], Awaitable[ResultT]]:
        ...

    def __get__(
        self,
        obj: "Near | AsyncNear",
        obj_type: Type["Near"] | Type["AsyncNear"],
    ) -> Callable[[ParamsT], ResultT] | Callable[[ParamsT], Awaitable[ResultT]]:
        from near.main import AsyncNear, Near

        if isinstance(obj, Near):

            def caller(params: ParamsT) -> ResultT:
                response = cast(Near, obj).provider.call_rpc(
                    self.base_method, params, self.result_schema
                )
                return self.result_formatter(response)

            return caller
        elif isinstance(obj, AsyncNear):

            async def async_caller(params: ParamsT) -> ResultT:
                response = await cast(AsyncNear, obj).provider.call_rpc(
                    self.base_method, params, self.result_schema
                )
                return self.result_formatter(response)

            return async_caller
        else:
            raise ValueError("No way...")
