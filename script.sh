#!/bin/bash

set -ev

python script.py

git branch
echo "${TRAVIS_BRANCH}"


# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

