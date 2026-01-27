from typing import ClassVar


class Routes:

    class Base:
        PREFIX: ClassVar[str] = '/base'
        FlagsRead : ClassVar[str] = '/flags_read'
