from typing import Literal, TypedDict


class ViewAccessKeyPayload(TypedDict):
    request_type: Literal["view_access_key"]
    finality: str
    account_id: str
    public_key: str


class ViewAccessKeyListPayload(TypedDict):
    request_type: Literal["view_access_key_list"]
    finality: str
    account_id: str
