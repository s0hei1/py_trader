from __future__ import annotations
from third_party.candlestic import Symbol

class PyTraderSymbols:
    eur_usd: Symbol = Symbol(1, "EUR", "USD", 4)
    btc_usd: Symbol = Symbol(2, "BTC", "USD", 0)
    gbp_usd: Symbol = Symbol(3, "GBP", "USD", 4, suffix='b')

    @classmethod
    def get_symbols(cls) -> list[Symbol]:
        return [
            getattr(cls, i)
            for i in PyTraderSymbols.__annotations__
            if isinstance(getattr(cls, i), Symbol)
        ]

    @classmethod
    def get_symbol_by_name(cls, symbol_name: str) -> Symbol | None:
        return first((i for i in cls.get_symbols() if i.symbol_name == symbol_name.upper()), default=None)

    @classmethod
    def get_symbols_name(cls) -> list[str]:
        return [i.symbol_name for i in cls.get_symbols()]
