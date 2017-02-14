#!/bin/bash

set -ev

python script.py 

git diff --name-only prod..HEAD

git diff --name-only master..HEAD

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

