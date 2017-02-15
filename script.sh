#!/bin/bash

set -ev

echo "${TRAVIS_BRANCH}"

var=$(git diff --name-only HEAD^...master)
echo $var

for filename in $var; do
	echo $filename
	python src/KBFrontmatter.py $filename
done

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" = "true" ] && [ "$TRAVIS_BRANCH" == "prod" ]; then
	for filename in $var; do
		python scripts/deploy.py filename
	done
 fi
