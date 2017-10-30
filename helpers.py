import json
import os
import sys
import boto3
import requests

APPROVALS_REQUIRED = int(os.environ['APPROVALS_REQUIRED'])

TOKEN = os.environ['GITHUB_TOKEN']
headers = {"Authorization": "token " + TOKEN}

def is_approved(pr):
    self_url = pr["_links"]["self"]["href"]
    reviews_request = requests.get(self_url + "/reviews", headers=headers)
    if reviews_request.status_code != 200:
        print(reviews_request)
        raise Exception("Failed to get reviewers for #" + str(pr["number"]))

    reviews = reviews_request.json()
    approvals = set()
    for review in reviews:
        if review["state"] != "APPROVED":
            pass

        approvals.add(review["user"]["login"])
    return len(approvals) >= APPROVALS_REQUIRED

def merge_pr(self_url):
    merge_request = requests.put(self_url + "/merge", headers=headers)

    return merge_request.status_code == 204

def save_pr_info(sha, pr_url, checks):
    item = {
        "sha": {
            "S": sha
        },
        "pr_url": {
            "S": pr_url
        },
        "requisite_checks": {
            "SS": checks
        }
    }
    print("Saving")
    print(item)
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(TableName="prs_to_be_merged", Item=item)

def get_pr_info(sha):
    dynamodb = boto3.client('dynamodb')
    resp = dynamodb.get_item(TableName="prs_to_be_merged", Key={"sha":{"S": sha}})
    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 or "Item" not in resp:
        print("Unable to find fetch the PR with sha " + sha)
        print(resp)
        return None

    pr_url = resp["Item"]["pr_url"]["S"]
    requisite_checks = resp["Item"]["requisite_checks"]["SS"]
    return {"sha": sha, "pr_url": pr_url, "requisite_checks": requisite_checks}

def filter_checks(pr, default_checks):
    checks = list(default_checks)
    status_url = pr["_links"]["statuses"]["href"]
    resp = requests.get(status_url, headers=headers)
    events = resp.json()

    for event in events:
        if event["state"] == "success" and event["context"] in checks:
            checks.remove(event["context"])

    print("Filtered checks")
    print(checks)
    return checks

def comment_on_pr(pr, comment):
    comment_url = pr["_links"]["comments"]["href"]
    resp = requests.post(comment_url, json=comment, headers=headers)
    print(resp)