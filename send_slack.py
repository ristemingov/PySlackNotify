import requests
import json
from settings import SLACK_WEBHOOK

def send_slack_notification(text: str):
    data = {"text":text}
    headers = {"Content-type": "application/json"}
    requests.post(SLACK_WEBHOOK,data=json.dumps(data), headers=headers)
