#!/bin/bash
cd $(dirname $0)
rm -rvf _posts/*
for old_name in $(cd ..; ls *.md); do {
    new_name=$(echo "$old_name" | sed 's@\([0-9][0-9]\)@2021-\1-@')
    title=$(echo "$old_name" | sed 's@[0-9]\+-\(.*\)\.md@\1@')
    (echo -e "---\nlayout: post\ntitle:  \"$title\"\n---\n"; cat ../$old_name) > _posts/$new_name
} done
bundle exec jekyll clean
ln -svf ../docs _site
bundle exec jekyll build

