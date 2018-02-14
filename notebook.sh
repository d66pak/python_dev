#!/bin/bash

ABSOLUTE=$(realpath $0)
WORK_DIR=$(dirname ${ABSOLUTE})

export OUT_DIR=${WORK_DIR}/dataOut
export IN_DIR=${WORK_DIR}/dataIn

# VIRTUAL_ENV variable will be set if virtual env is activated.
if [ -z $VIRTUAL_ENV ];
then
	echo "Loading python virtualenv..."
	source ${WORK_DIR}/py_ve/bin/activate
fi

jupyter notebook

