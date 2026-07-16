import os
import shutil
import uuid

from fastapi import UploadFile


class FileStorageService:

    UPLOAD_DIR = "app/uploads"

    @classmethod
    def save(
        cls,
        file: UploadFile,
        extension: str
    ):

        os.makedirs(
            cls.UPLOAD_DIR,
            exist_ok=True
        )

        filename = f"{uuid.uuid4()}{extension}"

        path = os.path.join(
            cls.UPLOAD_DIR,
            filename
        )

        with open(path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return path