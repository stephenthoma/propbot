import json


def send_msg(message: str, severity: str, **kwargs):
    print(json.dumps(dict(severity=severity, message=message, **kwargs)))
