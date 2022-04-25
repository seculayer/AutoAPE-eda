#!/bin/bash

VERSION="1.0.0"
MODULE_NAME="eda"
REGISTRY_URL="registry.seculayer.com:31500"
SECRET_PATH="../access_token/token"

# docker build
DOCKER_BUILDKIT=1 docker build --no-cache --secret id=token,src=$SECRET_PATH -t $REGISTRY_URL/ape/automl-$MODULE_NAME:$VERSION .
docker push $REGISTRY_URL/ape/automl-$MODULE_NAME:$VERSION
