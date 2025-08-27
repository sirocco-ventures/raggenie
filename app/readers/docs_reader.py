class DocsReader:

    def __init__(self, source, engine=None):
        self.source = source
        self.engine = engine

    def load(self):
        raise NotImplementedError("load method must be implemented in subclass")

