import json
import os
import sys
import boto3
import requests
from helpers import merge_pr, save_pr_info, get_pr_info

def hook(payload):
	if "state" not in payload:
		print("no status event, returning")
		return 0

	if payload["state"] != "success":
		print("Status is not succesful. returning")
		return 0

	if "context" not in payload:
		print("No context, returning")
		return 0

	check = payload["context"]
	sha = payload["sha"]
	print("Checking the status list with " + check + " and sha " + sha)

	item = get_pr_info(sha=sha)
	if not item:
		print("No PR exists for " + sha)
		return

	url = item["pr_url"]
	requisite_checks = item["requisite_checks"]
	sha = item["sha"]

	print(item)

	requisite_checks.remove(check)

	if not requisite_checks:
		print("Attempting to merge the pr " + url)
		if merge_pr(url):
			print("Merged the PR")
		else:
			print("Failed  merging")
	else:
		print("Requisite check present. Updating the item")
		save_pr_info(checks=requisite_checks, sha=sha, pr_url=url)