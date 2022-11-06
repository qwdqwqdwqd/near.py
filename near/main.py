from typing import Tuple, Union

from near.constants import DEFAULT_TIMEOUT
from near.method import Method
from near.payloads import ViewAccessKeyListPayload, ViewAccessKeyPayload
from near.providers.http import AsyncHTTPProvider, HTTPProvider
from near.types import RPC, AccessKey, AccessKeyList, GasPriceReponse, YoctoNEAR


class NearMethodsMixin:
    _gas_price: Method[Tuple[Union[int, str, None]], YoctoNEAR] = Method(
        RPC.gas_price, GasPriceReponse, lambda r: r.gas_price
    )
    _view_access_key: Method[ViewAccessKeyPayload, AccessKey] = Method(
        RPC.query, AccessKey, lambda r: r
    )
    _view_access_key_list: Method[ViewAccessKeyListPayload, AccessKeyList] = Method(
        RPC.query, AccessKeyList, lambda r: r
    )


class Near(NearMethodsMixin):
    def __init__(self, endpoint_uri: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.provider = HTTPProvider(endpoint_uri, timeout)

    def gas_price(self, block_identifier: Union[int, str, None] = None) -> YoctoNEAR:
        return self._gas_price((block_identifier,))

    def view_access_key(
        self,
        finality: str,
        account_id: str,
        public_key: str,
    ) -> AccessKey:
        return self._view_access_key(
            {
                "request_type": "view_access_key",
                "finality": finality,
                "account_id": account_id,
                "public_key": public_key,
            }
        )

    def view_access_key_list(
        self,
        finality: str,
        account_id: str,
    ) -> AccessKeyList:
        return self._view_access_key_list(
            {
                "request_type": "view_access_key_list",
                "finality": finality,
                "account_id": account_id,
            }
        )

    def is_connected(self) -> bool:
        return self.provider.is_connected()


class AsyncNear(NearMethodsMixin):
    def __init__(self, endpoint_uri: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.provider = AsyncHTTPProvider(endpoint_uri, timeout)

    async def gas_price(
        self, block_identifier: Union[int, str, None] = None
    ) -> YoctoNEAR:
        return await self._gas_price((block_identifier,))

    async def view_access_key(
        self, finality: str, account_id: str, public_key: str
    ) -> AccessKey:
        return await self._view_access_key(
            {
                "request_type": "view_access_key",
                "finality": finality,
                "account_id": account_id,
                "public_key": public_key,
            }
        )

    async def view_access_key_list(
        self,
        finality: str,
        account_id: str,
    ) -> AccessKeyList:
        return await self._view_access_key_list(
            {
                "request_type": "view_access_key_list",
                "finality": finality,
                "account_id": account_id,
            }
        )

    async def is_connected(self) -> bool:
        return await self.provider.is_connected()
