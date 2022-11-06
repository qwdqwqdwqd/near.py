from typing import Any, List, Literal, NewType, Optional, TypeVar

from pydantic import BaseModel

RPCEndpoint = NewType("RPCEndpoint", str)
YoctoNEAR = NewType("YoctoNEAR", int)


class RPCErrorCause(BaseModel):
    info: Any
    name: str


class RPCError(BaseModel):
    name: str
    cause: RPCErrorCause
    code: int
    data: str
    message: str


class RPCResponse(BaseModel):
    error: Optional[RPCError]
    id: str | int
    jsonrpc: Literal["2.0"]
    result: Any


class RPC:
    gas_price = RPCEndpoint("gas_price")
    status = RPCEndpoint("status")
    query = RPCEndpoint("query")


class ResultBase(BaseModel):
    ...


class GasPriceReponse(ResultBase):
    gas_price: YoctoNEAR


class AccessKey(ResultBase):
    nonce: int
    permission: Any
    block_height: int
    block_hash: str


class Key(BaseModel):
    class AccessKey(BaseModel):
        nonce: int
        permission: Any

    public_key: str
    access_key: AccessKey


class AccessKeyList(ResultBase):
    keys: List[Key]
    block_height: int
    block_hash: str


ResultSchemaT = TypeVar("ResultSchemaT", bound=ResultBase)
