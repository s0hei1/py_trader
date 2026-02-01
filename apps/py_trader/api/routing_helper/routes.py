from typing import ClassVar


class Routes:

    class Base:
        PREFIX: ClassVar[str] = '/base'
        FlagsRead : ClassVar[str] = '/flags_read'
        ConfigCreate : ClassVar[str] = '/config_create'
        ConfigReadLast : ClassVar[str] = '/config_read_last'
        ConfigReadHistory : ClassVar[str] = '/configs_history'

    class Strategy:
        PREFIX: ClassVar[str] = '/strategy'
        Create: ClassVar[str] = '/create'
        ReadOne: ClassVar[str] = '/read_one'
        ReadMany: ClassVar[str] = '/read_many'
        Update: ClassVar[str] = '/update'

    class Symbol:
        PREFIX: ClassVar[str] = '/symbol'
        Create: ClassVar[str] = '/create'
        ReadMany: ClassVar[str] = '/read_many'
