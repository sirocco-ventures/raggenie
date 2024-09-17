class DocsReader:
    
    def __init__(self, source):
        self.source = source

    def load(self):
        raise NotImplementedError("load method must be implemented in subclass")
    
