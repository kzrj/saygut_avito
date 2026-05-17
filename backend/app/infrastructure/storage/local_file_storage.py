import os
import uuid

from app.config import settings
from app.domain.ports.file_storage import FileStorage


class LocalFileStorage(FileStorage):
    async def save_image(self, data: bytes, filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
        name = f"{uuid.uuid4()}.{ext}"
        os.makedirs(settings.upload_dir, exist_ok=True)
        path = os.path.join(settings.upload_dir, name)
        with open(path, "wb") as f:
            f.write(data)
        return f"/uploads/{name}"
