#!/bin/bash

# Token of a git hub user with write permissions to the repo
export GITHUB_TOKEN=""
# A PR will be merged only if it has this many approvals
export APPROVALS_REQUIRED=0
# Comma seperated list of the requisite checks
export CHECKS="ci/circleci: style_check"
# A PR will auto merge only if it has this label
export MERGE_LABEL="To be Merged"

if [[ `hash pip` -ne 0 ]]; then
	echo 'PIP is required for the deployment'
	exit
fi
if [[ `hash zip` -ne 0 ]]; then
	echo 'ZIP is required for the deployment'
fi
if [[ `hash serverless` -ne 0 ]]; then
	echo 'Serverless is required for the deployment'
fi

mkdir -p dist
# copy from venv ?
# cp -rf env/lib/python2.7/site-packages/* dist
cp src/* dist
pip install -t dist -r requirements.txt
cp serverless.yml dist/
(cd dist; serverless deploy)
rm -rf dist