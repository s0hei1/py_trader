from dataclasses import dataclass


@dataclass
class Symbol:
    base_currency: str
    quote_currency: str
    alias_names: list[str] | None = None
    prefix: str = ''
    suffix: str = ''

    def __init__(self, base_currency: str, quote_currency: str, /, alias_names: list[str] | None = None,
                 prefix: str = '',
                 suffix: str = '', ):
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.alias_names = alias_names
        self.prefix = prefix
        self.suffix  = suffix


    @property
    def symbol_name(self) -> str:
        return f"{self.base_currency}{self.quote_currency}".upper()

    @property
    def symbol_fullname(self) -> str:
        return f"{self.prefix}{self.symbol_name}{self.suffix}"

    def __eq__(self, other: 'Symbol') -> bool:
        return (
                self.base_currency.upper() == other.base_currency.upper() and
                self.quote_currency.upper() == other.quote_currency.upper())

    def __getitem__(self, item: int) -> str:
        if item == 0:
            return self.base_currency
        if item == 1:
            return self.quote_currency

        return ''
