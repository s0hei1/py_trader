from src.tools.di.container import Container
from src.ui.viewmodel.vm_result import VMResult

class ConfigVM:

    _risk_percentage: float
    _total_balance: float

    def __init__(self):
        self.flags_repo = Container.flags_repo()
        flags = self.flags_repo.get_or_config_flags()

        self._risk_percentage = flags.risk_percentage
        self._total_balance = flags.total_balance


    @property
    def risk_percentage(self):
        return self._risk_percentage

    @property
    def total_balance(self):
        return self._total_balance

    def set_risk_percentage(self, new_value : str):
        self._risk_percentage = float(new_value)

    def set_total_balance(self, new_value):
        self._total_balance = float(new_value)

    def update_flags(self) -> VMResult:
        try:
            self.flags_repo.set_flags(
                risk_percentage=self._risk_percentage,
                total_balance=self._total_balance
            )
            return VMResult()
        except Exception as e:
            return VMResult(has_error=True, message=str(e))

