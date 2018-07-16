#!/usr/bin/env bash

[[ -f ../.env ]]  && . ../.env
[[ -f .env ]]  && . .env
[[ -f .config.yml ]]  && CONFIG=./config.yml
[[ -f .circleci/config.yml ]]  && CONFIG=.circleci/config.yml


BRANCH=`git st | grep 'On branch' | sed 's/On branch //'`
TAG=${BRANCH/release\//}
JOB=build
VERBOSE=0
#
#help (){
#    echo "./test-config.sh [-b/--branch BRANCH] [-j/--job JOB] [-t/--tag TAG] [-v/--verbose 1/2/3]"
#    exit 1
#}

#for key in "$@"
while [ "$1" != "" ]; do
case $1 in
    -b=*|--branch=*)
        BRANCH="${1#*=}"
        shift # past argument
        ;;
    -j=*|--job=*)
        JOB="${1#*=}"
        shift # past argument
        ;;
    -t=*|--tag=*)
        TAG="${key#*=}"
        shift # past argument
        ;;
    -v=*|--verbose=*)
        VERBOSE="${1#*=}"
        shift # past argument
        ;;
    -b|--branch)
        BRANCH="$2"
        shift # past argument
        shift # past value
        ;;
    -j|--job)
        JOB="$2"
        shift # past argument
        shift # past value
        ;;
    -t|--tag)
        TAG="$2"
        shift # past argument
        shift # past value
        ;;
    -v|--verbose)
        VERBOSE="$2"
        shift # past argument
        shift # past value
        ;;
    --token)
        GITHUB_TOKEN="$2"
        shift # past argument
        shift # past value
        ;;
    --dry-run|--dryrun)
        DRYRUN="1"
        shift # past argument
        ;;
    -h|--help)
            help
            ;;
    *) echo "unknown option '$1'"
       help
       ;;
esac
done

#BRANCH="${BRANCH/\//%2F}"

if [ "$VERBOSE" -gt "0" ]; then
    dump
fi

if [ "$DRYRUN" == "1" ];then
    exit 0
fi

if [ -z "$GITHUB_TOKEN" ]; then
    read -p 'CircleCI token: ' GITHUB_TOKEN
fi

if [ -z "$TAG" ]; then
    TAG=`curl \
      -s \
      -H "Authorization: token ${GITHUB_TOKEN}" \
      "https://api.github.com/repos/unicef/sir-poc-fe/releases/latest" | jq -r '.tag_name'`
fi
