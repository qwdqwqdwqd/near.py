from collections import defaultdict
from typing import DefaultDict, Type

from near.types import RPCError as RPCErrorDict


class RPCError(IOError):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class BadResponseError(RPCError):
    ...


class RPCStandardError(RPCError):
    def __init__(self, error: RPCErrorDict) -> None:
        self.error = error

    def __str__(self) -> str:
        return f"{self.error.message}: {self.error.data}"


class HandlerError(RPCStandardError):
    ...


class RequestValidationError(RPCStandardError):
    ...


class UnknownBlockError(HandlerError):
    ...


class ParseError(RequestValidationError):
    ...


class InternalError(RPCStandardError):
    ...


class AccessKeyDoesNotExist(RPCError):
    ...


ERROR_MESSAGES_BIND = {
    "^access key .*? does not exist while viewing$": AccessKeyDoesNotExist
}


ERRORS_BIND: DefaultDict[str, Type[RPCStandardError]] = defaultdict(
    lambda: RPCStandardError,
    {
        "UNKNOWN_BLOCK": UnknownBlockError,
        "PARSE_ERROR": ParseError,
        "INTERNAL_ERROR": InternalError,
    },
)
