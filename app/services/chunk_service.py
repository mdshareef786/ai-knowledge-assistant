from app.utils.text_chunker import chunk_text


class ChunkService:

    @staticmethod
    def create(text: str):

        return chunk_text(text)