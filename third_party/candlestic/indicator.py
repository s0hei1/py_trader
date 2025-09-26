from dataclasses import dataclass
import numpy as np
@dataclass
class Indicator:
    name : str
    values : np.ndarray

    def __len__(self):
        return len(self.values)