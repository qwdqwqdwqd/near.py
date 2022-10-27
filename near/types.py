from typing import Any, Literal, NewType, TypedDict

RPCEndpoint = NewType("RPCEndpoint", str)
YoctoNEAR = NewType("YoctoNEAR", int)


class RPCErrorCause(TypedDict):
    info: Any
    name: str


class RPCError(TypedDict):
    name: str
    cause: RPCErrorCause
    code: int
    data: str
    message: str


class RPCResponse(TypedDict, total=False):
    error: RPCError
    id: Literal["dontcare"]
    jsonrpc: Literal["2.0"]
    result: Any


class RPC:
    gas_price = RPCEndpoint("gas_price")
    status = RPCEndpoint("status")
