from typing import ClassVar


class Routes:

    class Base:
        PREFIX: ClassVar[str] = '/base'
        FlagsRead : ClassVar[str] = '/flags_read'
        ConfigCreate : ClassVar[str] = '/config_create'
        ConfigReadLast : ClassVar[str] = '/config_read_last'
        ConfigReadHistory : ClassVar[str] = '/configs_history'