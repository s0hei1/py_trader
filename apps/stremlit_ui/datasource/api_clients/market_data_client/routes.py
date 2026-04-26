from typing import ClassVar


class Routes:

    class Base:
        PREFIX: ClassVar[str] = '/base'
        FlagsRead : ClassVar[str] = '/flags_read'

    class Candle:
        PREFIX: ClassVar[str] = '/candle'
        CreateMany: ClassVar[str] = '/create_many'
        ReadMany: ClassVar[str] = '/read_many'

    class Symbol:
        PREFIX: ClassVar[str] = '/symbol'
        CreateOne: ClassVar[str] = '/create_one'
        ReadMany: ClassVar[str] = '/read_many'


    class Broker:
        PREFIX: ClassVar[str] = '/broker'
        CreateOne: ClassVar[str] = '/create_one'
        ReadMany: ClassVar[str] = '/read_many'


    class TimeFrame:
        PREFIX: ClassVar[str] = '/time_frame'
        CreateOne: ClassVar[str] = '/create_one'
        ReadMany: ClassVar[str] = '/read_many'
