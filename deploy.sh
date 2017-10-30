#!/bin/bash

# Token of a git hub user with write permissions to the repo
export GITHUB_TOKEN=""
# A PR will be merged only if it has this many approvals
export APPROVALS_REQUIRED=2
# Comma seperated list of the requisite checks
export CHECKS="ci/circleci: style_check,ci/circleci: rake_test,ci/circleci: javascript_rake_test,ci/circleci: precompile_assets"
# A PR will auto merge only if it has this label
export MERGE_LABEL="to be merged"

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

pip install -t . -r requirements.txt
serverless deploy