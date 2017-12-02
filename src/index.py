import json
import os
import sys
import boto3
import requests
from status_update_webhook import hook as status_update_webhook
from push_webhook import hook as push_webhook
from labeled_webhook import hook as labeled_webhook


def main(event, context):
	payload = event["body"]
	print(event)
	print(payload)
	git_event = event["headers"]["X-GitHub-Event"]
	if git_event == "push":
		push_webhook(payload)
	elif git_event == "status":
		status_update_webhook(payload)
	elif git_event == "pull_request" and payload["action"] == "labeled":
		labeled_webhook(payload)
	else:
		print("Unknown event " + git_event)