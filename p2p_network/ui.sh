#!/bin/bash

SCRIPT=$(readlink -f $0)
BASEPATH=`dirname "$SCRIPT"`

pyuic5 $BASEPATH/AboutDialog.ui -o $BASEPATH/AboutDialog.py
pyuic5 $BASEPATH/MainWindow.ui -o $BASEPATH/MainWindow.py
pyuic5 $BASEPATH/ConnectDialog.ui -o $BASEPATH/ConnectDialog.py
pyuic5 $BASEPATH/ConnectToDialog.ui -o $BASEPATH/ConnectToDialog.py
pyuic5 $BASEPATH/EditConnectionDialog.ui -o $BASEPATH/EditConnectionDialog.py
pyuic5 $BASEPATH/LogWindow.ui -o $BASEPATH/LogWindow.py