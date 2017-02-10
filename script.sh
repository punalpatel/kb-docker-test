#!/bin/bash

set -ev

var=$(git diff --name-only HEAD...master)
echo "$var"

echo "${TRAVIS_PULL_REQUEST}" 
echo ${TRAVIS_BRANCH}"

python script.py 

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

