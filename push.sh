#!/bin/sh

setup_git() {
  git config --global user.email "punal.patel@gmail.com"
  git config --global user.name "Travis CI"
}

commit_kbs() {
  git checkout -b prod
  git add . 
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add prod https://${GH_TOKEN}@github.com/pivotal-gss/kb-docker.git > /dev/null 2>&1
  git push --quiet --set-upstream master prod 
}

setup_git
commit_kbs
upload_files
