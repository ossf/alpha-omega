import hashlib
import io
import logging
import mimetypes
import os
import tarfile
import zipfile

from triage.models import File, FileContent, ProjectVersion, Scan

logger = logging.getLogger(__name__)


class FileImporter:
    @classmethod
    def import_file(
        cls, root: str, file_path: str, file_content: bytes, target: Scan | ProjectVersion
    ) -> bool:
        """
        Adds a file to the database.
        """
        if root is None:
            root = ""

        for file_info in cls.extract_archive(file_path, file_content):
            logger.debug("Saving file %s", file_info.get("name"))
            mime_type = mimetypes.guess_type(file_info.get("name"), strict=False)[0]
            if mime_type is None:
                mime_type = "application/octet-stream"

            content_hash = hashlib.sha256(file_info.get("content")).digest()
            file_content = FileContent.objects.get_or_create(
                hash=content_hash,
                defaults={"content_type": mime_type, "data": file_info.get("content")},
            )[0]
            file = File.objects.get_or_create(
                name=os.path.basename(file_info.get("name")),
                path=file_info.get("name"),
                content=file_content,
            )[0]

            if isinstance(target, (Scan, ProjectVersion)):
                target.files.add(file)

    @classmethod
    def extract_archive(cls, file_path: str, file_content: bytes) -> dict:
        """
        Extracts contents of an archive file.
        """
        if file_path.endswith(".tgz"):
            logger.debug("Detected archive type: tar.gz (%s)", file_path)
            with tarfile.open(fileobj=io.BytesIO(file_content), mode="r") as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        content = tar.extractfile(member)
                        yield {
                            "name": member.name,
                            "size": member.size,
                            "content": content.read() if content is not None else None,
                        }
        elif file_path.endswith(".zip"):
            logger.debug("Detected archive type: zip (%s)", file_path)
            with zipfile.ZipFile(io.BytesIO(file_content), mode="r") as zip:
                for member in zip.infolist():
                    if member.is_file():
                        yield {
                            "name": member.filename,
                            "size": member.file_size,
                            "content": zip.read(member),
                        }
        else:
            logger.debug("File %s is not an archive", file_path)
            return {"name": file_path, "size": len(file_content), "content": file_content}
