#!/bin/bash

set -ev

var=$(git diff --name-only HEAD...master)
echo "$var"

python script.py 


# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" = "true" ] && [ "$TRAVIS_BRANCH" == "prod" ]; then
	python deploy.py  
 fi

