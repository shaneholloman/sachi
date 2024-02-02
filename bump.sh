#!/bin/sh -xe
if [ -z "$1" ]; then
  echo "Usage: $0 <new_version>"
  exit 1
fi

git switch --detach
NEW_VERSION=$(poetry version $1 --short)
git commit -am $NEW_VERSION
git tag $NEW_VERSION

DEV_VERSION=$(poetry version patch --short --dry-run)-dev
git switch main
poetry version $DEV_VERSION
git commit -am $DEV_VERSION -m '[skip ci]'

git push origin $NEW_VERSION main
