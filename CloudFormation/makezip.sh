#!/bin/sh

ORIGIN=`pwd`
ZIP="/tmp/simpleliveworkflow_resources.zip"

if [ -z ${VIRTUAL_ENV+x} ]; then
    echo "VIRTUAL_ENV is unset"
    exit 1
else 
    rm -f $ZIP
    echo adding lambda sources
    zip -q -r $ZIP *.py
    cd "$VIRTUAL_ENV/lib/python3.6/site-packages"
    echo adding virtual environment site packages
    zip -q -r -u $ZIP * 
    cd $ORIGIN
    echo created $ZIP
fi
