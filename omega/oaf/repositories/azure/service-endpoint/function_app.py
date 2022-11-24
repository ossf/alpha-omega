"""Azure Storage Endpoint for OAF."""
import re
import bz2
import datetime
import hashlib
import json
import logging
import os
import uuid

import azure.functions as func
from azure.storage.blob import BlobClient, BlobServiceClient, BlobType, ContainerClient, __version__

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

STORAGE_CONTAINER_NAME = os.environ.get("STORAGE_CONTAINER_NAME")
if not STORAGE_CONTAINER_NAME:
    raise Exception("STORAGE_CONTAINER_NAME env variable is not set")


def connect() -> BlobServiceClient | None:
    """Connect to Azure Blob Storage using the AZURE_STORAGE_CONNECTION_STRING
    environment variable.
    """
    try:
        connection_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_str:
            raise Exception("AZURE_STORAGE_CONNECTION_STRING env variable is not set")

        return BlobServiceClient.from_connection_string(connection_str)
    except Exception as msg:
        logging.error(f"Failed to connect to Azure Blob Storage: {msg}")
        return None


def get_blob_path(subject: str) -> str:
    """Calculates the path in which the blob for subject should be stored."""
    virtual_path = hashlib.sha256(subject.encode("utf-8"), usedforsecurity=False).hexdigest()
    virtual_prefix = virtual_path[:3]
    return os.path.join(virtual_prefix, virtual_path)


@app.function_name(name="remove_expired_assertions")
@app.schedule(schedule="0 0 2 * *", arg_name="timer", run_on_startup=True)
def remove_expired_assertions(timer: func.TimerRequest) -> None:
    """Trigger for reaping expired blobs out of Azure Storage.
    This is only supported on real Azure, and not Azurite.
    Disabled by default, enable with ENABLE_EXPIRATION_REAPER=True.
    """
    if not os.environ.get("ENABLE_EXPIRATION_REAPER") in ["1", "true", "True"]:
        return

    logging.info("Removing expired assertions by Timer Trigger.")
    client = connect()
    if client is None:
        logging.error("Unable to connect to Azure Storage.")
        return

    # Get the first day of the previous month
    _date = datetime.datetime.today()
    _date = (_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    reaper_date = _date.strftime("%Y-%m-01")

    # Get the container
    container = client.get_container_client(STORAGE_CONTAINER_NAME)
    num_deleted = 0
    for blob in container.find_blobs_by_tags(f'"expiry"="{reaper_date}"'):
        logging.debug("Deleting %s", blob.name)
        container.delete_blob(blob.name)
        num_deleted += 1

    logging.info("Deleted %d stale assertions.", num_deleted)


@app.function_name(name="add_assertion")
@app.route(route="add")
@app.http_type(http_type=func.HttpMethod.POST)
def add_assertion(req: func.HttpRequest) -> func.HttpResponse:
    """Add an assertion to Azure Storage."""
    logging.debug("add_assertion() triggered by HTTP request.")

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    subject = body.get("subject")
    if not subject:
        return func.HttpResponse("Subject not provided.", status_code=400)

    blob_path = get_blob_path(subject)
    blob_name = os.path.join(blob_path, str(uuid.uuid4()))

    assertion_content = json.dumps(body.get("content")).encode("utf-8")
    assertion_compressed = bz2.compress(assertion_content, compresslevel=9)

    # Expiration Date
    tags = {}
    expiry = body.get("expiration")
    if expiry:
        if re.match("^[0-9]{4}-[0-9]{2}$", expiry):
            expiry = f"{expiry}-01"
            tags["expiry"] = expiry
        else:
            return func.HttpResponse(
                "Invalid expiration, must be in the format YYYY-MM", status_code=400
            )

    try:
        client = connect()
        if not client:
            return func.HttpResponse("Could not connect to Azure Storage", status_code=500)

        container = client.get_container_client(STORAGE_CONTAINER_NAME)
        blob = container.get_blob_client(blob_name)
        blob.upload_blob(assertion_compressed, tags=tags)

        return func.HttpResponse("Assertion added successfully", status_code=200)
    except Exception as msg:
        logging.warning("Error adding assertion: %s", msg)
        return func.HttpResponse("Error adding assertion.", status_code=500)


@app.function_name(name="find_assertions")
@app.route(route="find")
def find_assertions(req: func.HttpRequest) -> func.HttpResponse:
    """Finds assertions in Azure Storage."""
    subject = req.params.get("subject")
    if not subject:
        return func.HttpResponse(
            "Please pass a subject on the query string or in the request body.", status_code=400
        )

    try:
        client = connect()
        if not client:
            return func.HttpResponse("Could not connect to Azure Storage", status_code=500)

        container = client.get_container_client(STORAGE_CONTAINER_NAME)
        blob_path = get_blob_path(subject)

        results = []
        for blob in container.list_blobs(blob_path):
            try:
                blob_bytes = container.get_blob_client(blob).download_blob()
                blob_content = bz2.decompress(blob_bytes.readall())
                results.append(json.loads(blob_content))
            except Exception as msg:
                logging.exception("Error downloading assertion: %s", msg, exc_info=True)

        return func.HttpResponse(json.dumps(results, indent=2), status_code=200)
    except Exception as msg:
        logging.exception("Error finding assertions: %s", msg, exc_info=True)
        return func.HttpResponse("Could not find assertions", status_code=500)
