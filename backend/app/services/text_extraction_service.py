from app.utils.file_extractor import extract_text


class TextExtractionService:

    @staticmethod
    def extract(
        file_path: str,
        extension: str
    ):

        return extract_text(
            file_path,
            extension
        )