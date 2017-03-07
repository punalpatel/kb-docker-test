#!/bin/sh

setup_git() {
  git config --global user.email "punal.patel@gmail.com"
  git config --global user.name "Punal Patel"
}

commit_kbs() {
  git checkout -b kbs
  git add . 
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

push_files() {
  git remote add origin https://${GH_TOKEN}@github.com/punalpatel/kb-docker-test.git > /dev/null 2>&1
  git push --quiet --set-upstream origin kbs 
}

setup_git
commit_kbs
push_files
