#!/usr/bin/env bash

[[ -f ../.env ]]  && . ../.env
[[ -f .env ]]  && . .env
[[ -f .config.yml ]]  && CONFIG=./config.yml
[[ -f .circleci/config.yml ]]  && CONFIG=.circleci/config.yml


BRANCH=`git st | grep 'On branch' | sed 's/On branch //'`
TAG=${BRANCH/release\//}
JOB=build
VERBOSE=1
MODE="local"

help (){
    echo "./test-config.sh"
    echo "  -b,--branch BRANCH. Default '$BRANCH'"
    echo "  -j,--job JOB. Default '$JOB'"
    echo "  -t,--tag TAG. Default '$TAG'"
    echo "  --token TOKEN. Default '$GITHUB_TOKEN'"
    echo "  -r,--remote"
    echo "  -v,--verbose"
    echo "  -q,--quiet"
    echo "  --dry-run"
    exit 1
}

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
    -q|--quiet)
        VERBOSE="0"
        shift # past argument
        shift # past value
        ;;
    -v|--verbose)
        VERBOSE="$2"
        shift # past argument
        shift # past value
        ;;
    --dry-run|--dryrun)
        DRYRUN="1"
        shift # past argument
        ;;
    -r|--remote)
        MODE="remote"
        shift # past argument
        ;;
    --circle-token)
        CIRCLE_TOKEN="$2"
        shift # past argument
        shift # past value
        ;;
    --github-token)
        GITHUB_TOKEN="$2"
        shift # past argument
        shift # past value
        ;;
    -h|--help)
            help
            ;;
    *) echo "unknown option '$1'"
       help
       ;;
esac
done

if [ "$VERBOSE" -gt "0" -o "$DRYRUN" == "1" ]; then
    echo "branch:  $BRANCH"
    echo "tag:     $TAG"
    echo "job:     $JOB"
    echo "verbose: $VERBOSE"
    echo "mode:    $MODE"
    echo "config:  $CONFIG"
    echo "Tokens:"
    echo "   GitHub:   $GITHUB_TOKEN"
    echo "   CircleCI: $CIRCLE_TOKEN"
fi

if [ "$DRYRUN" == "1" ];then
    exit 0
fi

if [ -z "$GITHUB_TOKEN" ]; then
    read -p 'CircleCI token: ' GITHUB_TOKEN
fi

#if [ -z "$TAG" ]; then
#    TAG=`curl \
#      -s \
#      -H "Authorization: token ${GITHUB_TOKEN}" \
#      "https://api.github.com/repos/unicef/sir-poc-fe/releases/latest" | jq -r '.tag_name'`
#fi

if [ $MODE == "remote" ];then
    curl --user "${CIRCLE_TOKEN}:" \
        --request POST \
        -q \
        --form build_parameters[TAG]=$TAG \
        --form build_parameters[CIRCLE_JOB]=$JOB \
        --form config=@config.yml \
        --form notify=false \
            https://circleci.com/api/v1.1/project/github/unicef/unicef-djangolib/tree/$BRANCH
else

    circleci build  -c $CONFIG \
        --job $JOB \
        -e CIRCLE_BUILD_NUM=$RANDOM \
        -e TAG=$TAG \
        -e GITHUB_TOKEN=$GITHUB_TOKEN \
        -e CIRCLE_TOKEN=$CIRCLE_TOKEN \
        --branch=$BRANCH
fi
