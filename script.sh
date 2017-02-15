#!/bin/bash

set -ev

echo "${TRAVIS_BRANCH}"

var=$(git diff --name-only HEAD^...master)

for filename in $var; do
	python src/KBFrontmatter.py filename
	# python script.py filename
done

# @TODO Add a local variable for non-travis testing
 if [ "${TRAVIS_PULL_REQUEST}" = "true" ] && [ "$TRAVIS_BRANCH" == "prod" ]; then
	for filename in $var; do
		python scripts/deploy.py filename
	done
 fi
