import json
import os
import sys
import requests

def main(event, context):
	print(json.dumps(event))
	print(json.dumps(context))