from typing import Union

from near.method import Method
from near.providers.http import AsyncHTTPProvider, HTTPProvider
from near.types import RPC, YoctoNEAR


class NearMethodsMixin:
    _gas_price: Method[[Union[int, str, None]], YoctoNEAR] = Method(
        RPC.gas_price, "gas_price"
    )


class Near(NearMethodsMixin):
    def __init__(self, endpoint_uri: str) -> None:
        self.provider = HTTPProvider(endpoint_uri)

    def gas_price(self, block_identifier: Union[int, str, None] = None) -> YoctoNEAR:
        return self._gas_price(block_identifier)

    def is_connected(self) -> bool:
        return self.provider.is_connected()


class AsyncNear(NearMethodsMixin):
    def __init__(self, endpoint_uri: str) -> None:
        self.provider = AsyncHTTPProvider(endpoint_uri)

    async def gas_price(
        self, block_identifier: Union[int, str, None] = None
    ) -> YoctoNEAR:
        return await self._gas_price(block_identifier)

    async def is_connected(self) -> bool:
        return await self.provider.is_connected()
