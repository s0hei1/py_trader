from typing import ClassVar

class Routes:

    class MABacktesting:
        PREFIX: ClassVar[str] = '/backtesting_service'
        BackTest : ClassVar[str] = '/back_test'
        ReadManyMAs : ClassVar[str] = '/read_ma'

    class Setup:
        PREFIX: ClassVar[str] = '/setup'
        CreateOne : ClassVar[str] = '/create_one'
        ReadMany : ClassVar[str] = '/read_many'

    class RiskManagement:
        PREFIX: ClassVar[str] = '/risk_management'
        CreateOne : ClassVar[str] = '/create_one'
        ReadMany : ClassVar[str] = '/read_many'

    class Strategy:
        PREFIX: ClassVar[str] = '/strategy'
        CreateOne : ClassVar[str] = '/create_one'
        ReadMany : ClassVar[str] = '/read_many'

