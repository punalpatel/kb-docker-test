#!/bin/bash

set -ev

var=$(git diff --name-only HEAD...master)
echo "$var"

python script.py 

echo "${TRAVIS_BRANCH}"
echo "${TRAVIS_PULL_REQUEST}"
echo "${KB_USER}"
echo "${KB_TEST}"
echo "${KB_TARGET_URL}"

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

