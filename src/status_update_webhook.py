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
	pr_number = item["pr_number"]
	sha = item["sha"]

	if "requisite_checks" not in item:
		print("No requiresite checks for PR " + url)
		return 0

	requisite_checks = item["requisite_checks"]

	print(item)

	if check not in requisite_checks:
		print(check + " check not mandatory, returning")
		return 0

	requisite_checks.remove(check)

	if not requisite_checks:
		print("Attempting to merge the pr " + url)
		if merge_pr(url):
			# delete_pr_info(sha=sha)
			print("Merged the PR")
			# response = table.query(
			# 	IndexName = "pr_number",
			# 	Limit = 1,
			# 	ScanIndexForward = False
			# 	)
			# print(response)
		else:
			print("Failed  merging")
			save_pr_info(checks=[], sha=sha, pr_number=pr_number, pr_url=url, is_failed=True)
	else:
		print("Requisite check present. Updating the item")
		save_pr_info(checks=requisite_checks, sha=sha, pr_number=pr_number, pr_url=url)