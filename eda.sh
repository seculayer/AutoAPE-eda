#!/bin/bash
######################################################################################
# eyeCloudAI 3.1 MLPS Run Script
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
######################################################################################

APP_PATH=/eyeCloudAI/app/ape
####
export PYTHONPATH=$PYTHONPATH:$APP_PATH/eda/lib:$APP_PATH/eda
export PYTHONPATH=$PYTHONPATH:$APP_PATH/pycmmn/lib:$APP_PATH/pycmmn

KEY=${1}
TASK_IDX=${2}
JOB_TYPE=${3}

/usr/local/bin/python3.7 -m eda.EDARunner ${KEY} ${TASK_IDX} ${JOB_TYPE}
