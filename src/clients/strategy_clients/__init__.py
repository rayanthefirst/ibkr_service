# Test Strategy
from clients.strategy_clients.test_strategy import TestStrategy

# Trailing Strategies
from clients.strategy_clients.trailing_strategies.long_buy_sell_trail import LongBuySellTrail
from clients.strategy_clients.trailing_strategies.long_short_buy_sell_trail import (
    LongShortBuySellTrail,
)
from clients.strategy_clients.trailing_strategies.short_sell_buy_trail import ShortSellBuyTrail
from clients.strategy_clients.trailing_strategies.long_short_neutral_buy_sell_trail import (
    LongShortNeutralBuySellTrail,
)

STRATEGIES = {
    TestStrategy.name: TestStrategy,
    LongBuySellTrail.name: LongBuySellTrail,
    LongShortBuySellTrail.name: LongShortBuySellTrail,
    ShortSellBuyTrail.name: ShortSellBuyTrail,
    LongShortNeutralBuySellTrail.name: LongShortNeutralBuySellTrail,
}
