import os
import datetime
import json

from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2


def enqueue_task(queue_name: str, handler_url: str, payload: dict, execute_in_seconds: int):
    """Create a task for a given queue with an arbitrary payload."""
    client = tasks_v2.CloudTasksClient()

    location = "us-central1"
    project = os.environ["GCP_PROJECT"]

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue_name)

    # Construct the request body.
    payload["secret"] = os.environ["APP_SECRET"]
    payload_bytes = json.dumps(payload).encode()
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=execute_in_seconds)
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(d)
    task = {
        "schedule_time": timestamp,
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": handler_url,  # The full url path that the task will be sent to.
            "headers": {"Content-type": "application/json"},
            "body": payload_bytes,
        },
    }

    # Use the client to build and send the task.
    response = client.create_task(request={"parent": parent, "task": task})

    print("Created task {}".format(response.name))
