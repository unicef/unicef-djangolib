#!/usr/bin/env bash
set -e

BASE=`dirname $0`

[[ -f ../.env ]]  && . ../.env
[[ -f .env ]]  && . .env

CONFIG=$BASE/config.yml


BRANCH=`git st | grep 'On branch' | sed 's/On branch //'`
TAG=${BRANCH/release\//}
JOB=build
VERBOSE=0


help (){
    echo "./test-local.sh [-b/--branch BRANCH] [-j/--job JOB] [-t/--tag TAG] [-v/--verbose 1/2/3] [--token TOKEN]"
    exit 1
}

dump(){
    echo "config:  $CONFIG"
    echo "branch:  $BRANCH"
    echo "tag:     $TAG"
    echo "job:     $JOB"
    echo "verbose: $VERBOSE"
}

. $BASE/common.sh

if [ -z "$TAG" ]; then
    TAG=`curl \
      -s \
      -H "Authorization: token ${GITHUB_TOKEN}" \
      "https://api.github.com/repos/unicef/sir-poc-fe/releases/latest" | jq -r '.tag_name'`

fi

curl --user "${CIRCLE_TOKEN}:" \
    --request POST \
    -q \
    --form build_parameters[TAG]=$TAG \
    --form build_parameters[CIRCLE_JOB]=$JOB \
    --form config=@config.yml \
    --form notify=false \
        https://circleci.com/api/v1.1/project/github/bitcaster-io/bitcaster/tree/$BRANCH

