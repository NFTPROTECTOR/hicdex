from typing import Optional

import hicdex.models as models
from dipdup.models import OperationData, OperationHandlerContext, OriginationContext, TransactionContext
from dipdup.utils import http_request
from hicdex.types.hen_subjkt.parameter.registry import RegistryParameter
from hicdex.types.hen_subjkt.storage import HenSubjktStorage


async def on_registry(
    ctx: OperationHandlerContext,
    registry: TransactionContext[RegistryParameter, HenSubjktStorage],
) -> None:
    addr = registry.data.sender_address
    holder, _ = await models.Holder.get_or_create(address=addr)

    name = bytes.fromhex(registry.parameter.subjkt).decode()
    metadata_file = bytes.fromhex(registry.parameter.metadata).decode()
    metadata = {}

    try:
        addr = metadata_file.replace('ipfs://', '')
        metadata = await http_request(
            'get',
            url=f'https://cloudflare-ipfs.com/ipfs/{addr}',
        )
    except Exception:
        pass
    holder.name = name  # type: ignore
    holder.metadata_file = metadata_file  # type: ignore
    holder.metadata = metadata  # type: ignore
    await holder.save()
