import hicdex.models as models
from dipdup.models import OperationHandlerContext, TransactionContext
from hicdex.types.hen_minter.parameter.collect import CollectParameter
from hicdex.types.hen_minter.storage import HenMinterStorage


async def on_collect(
    ctx: OperationHandlerContext,
    collect: TransactionContext[CollectParameter, HenMinterStorage],
) -> None:
    swap = await models.Swap.filter(id=collect.parameter.swap_id).get()
    seller = await swap.creator
    buyer, _ = await models.Holder.get_or_create(address=collect.data.sender_address)
    token = await swap.token.get()  # type: ignore

    trade = models.Trade(
        swap=swap,
        seller=seller,
        buyer=buyer,
        token=token,
        amount=int(collect.parameter.objkt_amount),
        level=collect.data.level,
        timestamp=collect.data.timestamp,
    )
    await trade.save()

    swap.amount_left -= int(collect.parameter.objkt_amount)  # type: ignore
    if swap.amount_left == 0:
        swap.status = models.SwapStatus.FINISHED
    await swap.save()
