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
        CreateOne: ClassVar[str] = '/create_one'
        ReadMany: ClassVar[str] = '/read_many'


    class Pattern:
        PREFIX: ClassVar[str] = '/symbol'
        Create: ClassVar[str] = '/create_one'
        CreateMany: ClassVar[str] = '/create_many'
        CreateGroup: ClassVar[str] = '/create_many'

        ReadOne: ClassVar[str] = '/read_one'
        ReadMany: ClassVar[str] = '/read_many'
        ReadOneGroup: ClassVar[str] = '/read_one_group'
        ReadManyGroups: ClassVar[str] = '/read_many_groups'


