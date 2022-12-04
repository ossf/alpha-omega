# -*- coding: utf-8 -*-
"""This module provides support for import SARIF files into the Triage Portal's data model."""

import hashlib
import json
import logging
import os
import re
import uuid
from typing import Optional, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from packageurl import PackageURL

from triage.models import Finding, ProjectVersion, Scan, Tool, WorkItemState
from triage.util.general import get_complex

logger = logging.getLogger(__name__)


class SARIFImporter:
    """
    This class handles importing SARIF files into the database.
    """

    @classmethod
    def import_sarif_file(
        cls, package_url: PackageURL | str, sarif: dict, user: Optional[Type[AbstractUser]]
    ) -> bool:
        """
        Imports a SARIF file containing tool findings into the database.

        Args:
            package_url: The PackageURL to attach all findings to. This PackageURL must
                         contain a version.
            sarif: The SARIF content (as a dict) to import.
            file_archive: The file archive containing the SARIF file.

        Returns:
            True if the SARIF content was successfully imported, False otherwise.
        """
        if package_url is None:
            raise TypeError("The package_url must not be None")

        if isinstance(package_url, str):
            package_url = PackageURL.from_string(package_url)

        if package_url.version is None:
            raise TypeError(
                f"The package_url ({package_url}) does not contain a version. Unable to import."
            )

        if sarif is None:
            raise TypeError("The sarif content must not be None.")

        if sarif.get("version") != "2.1.0":
            raise ValueError("Only SARIF version 2.1.0 is supported.")

        user = get_user_model().objects.get(id=1)  # TODO: Fix this hardcoding
        project_version = ProjectVersion.get_or_create_from_package_url(package_url, user)

        num_imported = 0
        processed = set()  # Reduce duplicates

        # First load all of the rules
        for run in sarif.get("runs"):
            tool_name = get_complex(run, "tool.driver.name")
            tool_version = get_complex(run, "tool.driver.version")
            tool = Tool.objects.get_or_create(
                name=tool_name,
                version=tool_version,
                defaults={
                    "created_by": user,
                    "updated_by": user,
                    "type": Tool.ToolType.STATIC_ANALYSIS,
                },
            )[0]

            logger.debug("Processing run for tool: %s", tool)

            rule_description_map = {}
            for rule in get_complex(run, "tool.driver.rules"):
                rule_id = get_complex(rule, "id")
                rule_description = get_complex(rule, "shortDescription.text")
                if rule_id and rule_description:
                    rule_description_map[rule_id] = rule_description

            for result in run.get("results", []):
                rule_id = result.get("ruleId")
                logger.debug("Saving result for rule #%s", rule_id)

                message = get_complex(result, "message.text")
                level = get_complex(result, "level")
                for location in get_complex(result, "locations"):
                    artifact_location = get_complex(location, "physicalLocation.artifactLocation")

                    src_root = get_complex(artifact_location, "uriBaseId", "%SRCROOT%")
                    if src_root.upper() not in ["%SRCROOT%", "SRCROOT"]:
                        continue

                    uri = get_complex(artifact_location, "uri")

                    # Ensure we only insert the same message once
                    key = {
                        "title": message,
                        "path": uri,
                        "line_number": get_complex(location, "physicalLocation.region.startLine"),
                    }
                    key = hashlib.sha256(json.dumps(key).encode("utf-8")).digest()

                    if key not in processed:
                        logger.debug("New key for issue %s, adding.", message)
                        processed.add(key)

                        file_path = get_complex(artifact_location, "uri")
                        file_path = cls.normalize_file_path(file_path)

                        file = project_version.files.filter(path=file_path).first()
                        if not file:
                            logger.debug("File %s not found, skipping.", file_path)
                            continue

                        # Create the issue
                        finding = Finding()
                        finding.title = message
                        finding.normalized_title = cls.normalize_title(message)
                        finding.state = WorkItemState.NEW
                        finding.file = file
                        finding.tool = tool
                        finding.project_version = project_version

                        finding.file_line = get_complex(
                            location, "physicalLocation.region.startLine", None
                        )
                        finding.severity_level = Finding.SeverityLevel.parse(level)
                        finding.analyst_severity_level = Finding.SeverityLevel.NOT_SPECIFIED
                        finding.confidence = Finding.ConfidenceLevel.NOT_SPECIFIED

                        finding.created_by = user
                        finding.updated_by = user

                        if Finding.objects.filter(
                            title=finding.title,
                            file=finding.file,
                            file_line=finding.file_line,
                            project_version=finding.project_version,
                        ).exists():
                            logger.debug("Duplicate finding, skipping.")
                            continue

                        finding.save()

                    num_imported += 1

        if num_imported:
            logger.debug("SARIF file successfully imported.")
            return True
        else:
            logger.debug("SARIF file processed, but no issues were found.")
            return False

    @classmethod
    def normalize_file_path(self, path):
        """Normalizes a file path to be relative to the root."""
        logger.debug("normalize_file_path(%s)", path)
        try:
            result = path
            if path.split("/")[2] == "package":
                result = "/".join(path.split("/")[2:])
            logger.debug("Normalizing file path [%s] -> [%s]", path, result)
            return result
        except:
            return path

    @classmethod
    def normalize_title(self, title):
        norm = {
            r"^Bracket object notation with user input is present.*": "Bracket object notation",
            r"^Object injection via bracket notation.*": "Object injection",
            r"^`ref` usage found.*": "Use of `ref`",
        }
        for regex, replacement in norm.items():
            if re.match(regex, title, re.IGNORECASE):
                return replacement
        return title
