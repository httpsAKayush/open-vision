class InMemoryVectorStore:
    def __init__(self):
        self.items = {}

    def upsert(self, key: str, vector: list[float]):
        self.items[key] = vector
