#!/bin/env bash

DEPLOY_DIR=./bap

if [ ! -d "$DEPLOY_DIR" ]; then
    mkdir "$DEPLOY_DIR"

    cp -r ./{js,css} $DEPLOY_DIR

    mkdir $DEPLOY_DIR/img

    cp -r ./img/{thumbnail,watermarked} $DEPLOY_DIR/img

    cp ./index.html $DEPLOY_DIR
fi

#scp -r -P 2222 $DEPLOY_DIR ogeagla@192.254.233.231:/home4/ogeagla/public_html/bap
