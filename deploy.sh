#!/bin/bash

# Token of a git hub user with write permissions to the repo
export GITHUB_TOKEN=""

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