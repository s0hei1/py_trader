from src.tools.di.container import Container


class PatternVM:

    def __init__(self):
        self.pattern_repo = Container.pattern_repo()


    def get_patterns(self) :
