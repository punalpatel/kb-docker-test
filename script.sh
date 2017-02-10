#!/bin/bash

set -ev

var=$(git diff --name-only HEAD...master)
echo "$var"

var1=$(git diff --name-only master...HEAD)
echo "$var1"

var2=$(git diff --name-only prod...HEAD)
echo "$var2"

echo "${TRAVIS_PULL_REQUEST}" 
echo "${TRAVIS_BRANCH}"

python script.py 

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

