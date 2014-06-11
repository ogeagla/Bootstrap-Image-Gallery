#!/bin/env bash

DEPLOY_DIR=./deploy

if [ ! -d "$DEPLOY_DIR" ]; then
    mkdir "$DEPLOY_DIR"

    cp -r ./{js,css} $DEPLOY_DIR

    mkdir $DEPLOY_DIR/img

    cp -r ./img/{thumbnail,watermarks,watermarked} $DEPLOY_DIR/img

    cp ./index.html $DEPLOY_DIR
fi

scp -r -P 2222 $DEPLOY_DIR ogeagla@octaviangeagla.com:/home4/ogeagla/public_html/bap
