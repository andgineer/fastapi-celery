#!/bin/bash
# Increments version git tag
# Saves it into VERSION_FILE

VERSION_FILE="backend/app/version.py"

TAG=$(git describe --tags)

major=0
minor=0
build=0

regex="([0-9]+).([0-9]+).([0-9]+)"
if [[ $TAG =~ $regex ]]; then
    major="${BASH_REMATCH[1]}"
    minor="${BASH_REMATCH[2]}"
    build="${BASH_REMATCH[3]}"
fi

echo -e "Last version tag: \033[33m$major.$minor.$build\033[39m"

if [[ $(git diff-index HEAD) || $(git status) == *"is ahead"* ]]; then
        echo -e "\n\033[33mPlease commit and push all changes" \
        "before setting version tag\033[39m\n"
        exit -1
fi

if [[ "$1" == "release" ]]; then
    build=0
    minor=0
    major=$(echo $major + 1 | bc)
elif [[ "$1" == "feature" ]]; then
    build=0
    minor=$(echo $minor + 1 | bc)
elif [[ "$1" == "bug" ]]; then
    build=$(echo $build + 1 | bc)
else
    echo "usage: ./verup.sh [release|feature|bug]"
    exit -1
fi

NEW_TAG=$(echo "$major.$minor.$build")
echo -e "New    : \033[32m$NEW_TAG\033[39m"
echo -e "VERSION = '$NEW_TAG'" > $VERSION_FILE

COMMIT_MSG=$(git log $TAG..HEAD --format=oneline | awk '{$1=""; print $0}')
COMMIT_MSG=$(echo -e "\n$COMMIT_MSG\n")

echo "Changes:"
echo $COMMIT_MSG
echo

git add $VERSION_FILE
git commit -m "Version $NEW_TAG$COMMIT_MSG"

echo "...push"
    git tag $NEW_TAG -m "$COMMIT_MSG"
    git push origin $NEW_TAG
    git push
