import json
import io
import logging
import os
import tarfile
import zipfile

import magic
from triage.models import File, FileContent, ProjectVersion
from triage.util.finding_importers.sarif_importer import SARIFImporter
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from triage.util.content_managers.file_manager import FileManager
from core import settings

logger = logging.getLogger(__name__)


class ArchiveImporter:
    """Imports an archive of files into the database.

    The archive can contain source code (within a 'reference-source' directory),
    scan results (including SARIF), and other files."""

    def __init__(self):
        self.storage_manager = FileManager()

    def import_archive(
        self,
        filename: str,
        archive: bytes,
        project_version: ProjectVersion,
        user: AbstractBaseUser | AnonymousUser | None = None,
    ):
        """
        Adds a file to the database.
        """
        logger.debug("Importing archive: %s", filename)

        for file_info in self.extract_archive(filename, archive):
            logger.debug("Processing file: %s", file_info.get("name"))

            if "/reference-binaries/" in file_info.get("name"):
                logger.debug(
                    "File was in reference source directory, saving as source code."
                )

                # Extract each file, save it to the database
                for source_file_info in self.extract_archive(
                    file_info.get("name"), file_info.get("content")
                ):
                    logger.debug("Saving source code: %s", source_file_info.get("name"))
                    self.add_file(
                        source_file_info.get("content"),
                        source_file_info.get("name"),
                        project_version,
                        File.FileType.SOURCE_CODE,
                        save=False,
                    )

            elif file_info.get("name").endswith("sarif"):
                logger.debug("File was a SARIF file, saving as scan.")
                self.add_file(
                    file_info.get("content"),
                    file_info.get("name"),
                    project_version,
                    File.FileType.SCAN_RESULT,
                    save=False,
                )

                logger.debug("File was a SARIF file, saving as scan.")
                sarif_content = json.loads(file_info.get("content"))
                SARIFImporter.import_sarif_file(sarif_content, project_version, user)

            else:
                logger.debug("File was generic file, saving as a scan result.")
                self.add_file(
                    file_info.get("content"),
                    file_info.get("name"),
                    project_version,
                    File.FileType.SCAN_RESULT,
                    save=False,
                )

        project_version.save()

    def add_file(
        self,
        content: bytes,
        path: str,
        project_version: ProjectVersion,
        file_type: str,
        save: bool = True,
    ):
        """Adds a file to storage."""
        mime_type = magic.from_buffer(content, mime=True)

        file_key = self.storage_manager.add_file(content, path)
        # Files are unique by content, path, etc.
        file = File.objects.get_or_create(
            name=os.path.basename(path),
            path=path,
            content_type=mime_type,
            file_key=file_key,
            file_type=file_type,
        )[0]

        project_version.files.add(file)
        if save:
            project_version.save()

    def extract_archive(self, file_path: str, file_content: bytes) -> dict:
        """
        Extracts contents of an archive file.
        """
        if file_path.endswith(".tgz") or file_path.endswith(".tar.gz"):
            logger.debug("Detected archive type: tar.gz (%s)", file_path)
            with tarfile.open(fileobj=io.BytesIO(file_content), mode="r") as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        content = tar.extractfile(member)
                        yield {
                            "name": member.name,
                            "path": member.name,
                            "size": member.size,
                            "content": content.read() if content is not None else None,
                        }
        elif file_path.endswith(".zip"):
            logger.debug("Detected archive type: zip (%s)", file_path)
            with zipfile.ZipFile(io.BytesIO(file_content), mode="r") as zip_obj:
                for member in zip_obj.infolist():
                    if not member.is_dir():  # ZipInfo does not have is_file()
                        yield {
                            "name": member.filename,
                            "path": member.filename,
                            "size": member.file_size,
                            "content": zip_obj.read(member),
                        }
        else:
            logger.debug("File %s is not an archive", file_path)
            return {
                "name": file_path,
                "path": file_path,
                "size": len(file_content),
                "content": file_content,
            }
