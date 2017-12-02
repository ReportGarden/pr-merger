import json
import os
import sys
import boto3
import requests
from helpers import is_approved, save_pr_info, filter_checks, merge_pr, comment_on_pr

checks = os.environ['CHECKS']
if checks:
	DEFAULT_CHECKS = checks.split(",")
else:
	DEFAULT_CHECKS = []

MERGE_LABEL = os.environ['MERGE_LABEL']

def hook(payload):
	if "pull_request" not in payload:
		print("No PR")
		return 0

	if payload["action"] != "labeled":
		print("Not labeled")
		return 0

	label = payload["label"]["name"]
	pr = payload["pull_request"]
	
	if label != MERGE_LABEL:
		print("Merge label not present, not merging")
		return 0

	if not is_approved(pr):
		comment = {
			"body": "Can't do that sire. PR is not yet approved"
		}
		comment_on_pr(pr=pr, comment=comment)
		print("Required approvals not present. Not merging")
		return 0

	pr_url = pr["_links"]["self"]["href"]
	pr_sha = pr["head"]["sha"]
	pr_number = pr["number"]
	checks = filter_checks(pr=pr, default_checks=DEFAULT_CHECKS)
	if not checks:
		print("All checks are passed during label. merging")
		if merge_pr(pr_url):
			print("Merged " + pr_url)
		else:
			comment = {
				"body": "Merge failed (You may have to update the PR manually)"
			}
			comment_on_pr(pr=pr, comment=comment)
			save_pr_info(checks=[], sha=pr_sha, pr_number=pr_number, pr_url=pr_url, is_failed=True)
	else:
		save_pr_info(pr_url=pr_url, pr_number=pr_number, sha=pr_sha, checks=checks)

