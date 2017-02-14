#!/bin/bash

set -ev

python script.py

cat src/KBDockerValidator.py

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" ] && [ "${TRAVIS_BRANCH}" == "prod" ]; then
		python deploy.py  	
 fi

