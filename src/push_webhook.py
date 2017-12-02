import json
import os
import sys
import boto3
import requests
from helpers import merge_pr, save_pr_info, get_pr_info, delete_pr_info

DEFAULT_CHECKS = os.environ['CHECKS'].split(",")

def hook(payload):
	if "before" not in payload or "after" not in payload:
		print("not push action, returning")
		return 0

	before_sha = payload["before"]
	after_sha = payload["after"]
	item = get_pr_info(sha=before_sha)
	if not item:
		print("No pr for the sha " + before_sha)
		return 0

	delete_pr_info(sha=before_sha)
	save_pr_info(pr_url=item["pr_url"], pr_number=item["pr_number"], sha=after_sha, checks=DEFAULT_CHECKS, retry_count=item["retry_count"])
