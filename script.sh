#!/bin/bash

set -ev

var=$(git diff --name-only HEAD...master)
echo "$var"

for filename in $var; do
	python scripts/frontmatter-test.py $filename
done

if [ "${TRAVIS_PULL_REQUEST}" = "true" ] && [ "$TRAVIS_BRANCH" == "master" ]; then
	for filename in $var; do
		python scripts/deploy.py  
	done	
fi

