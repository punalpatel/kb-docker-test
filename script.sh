#!/bin/bash

set -ev

var2=$(git diff --name-only HEAD^)
git diff --name-only HEAD^
echo "$var2"

python script.py


# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

