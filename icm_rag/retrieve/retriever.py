class Retriever:
    def __init__(self, chunker):
        self.chunker = chunker

    def chunk(self, text):
        return self.chunker.split_text(text)
