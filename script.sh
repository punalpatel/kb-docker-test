#!/bin/bash

set -ev

python script.py

git branch
echo "${TRAVIS_BRANCH}"

var=$(git diff --name-only HEAD...master)
echo "$var"


var1=$(git diff --name-only HEAD^...master)
echo "$var1"

var2=$(git diff --name-only master...HEAD^)
echo "$var2"

var3=$(git diff --name-only master...HEAD)
echo "$var3"


var3=$(git diff --name-only master...HEAD~1)
echo "$var3"

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

