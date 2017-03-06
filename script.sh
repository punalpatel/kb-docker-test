#!/bin/bash

set -ev

export KB_DOCKER=/kb-docker
export PCF_KBS=/pcf-kbs

echo "${TRAVIS_BRANCH}"

cd $PCF_KBS
var=$(git diff --name-only HEAD^...master)
echo $var

for filename in $var; do
	echo $filename
	if $filename:
		python $KB_DOCKER/src/KBFrontmatter.py $filename
	else:
		continue
done

# @TODO Add a local variable for non-travis testing
 if [ "$TRAVIS_BRANCH" == "prod" ]; then
	for filename in $var; do
		if $filename:
			python $KB_DOCKER/deploy.py $filename
		else:
			continue
	done
 fi
