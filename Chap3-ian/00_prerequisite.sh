#!/bin/sh

SEARCH="\$YOUR_CURRENT_DIRECTORY"
REPLACE=`pwd`
FILENAME=ansible.cfg

sed -i -e "s+$SEARCH+$REPLACE+g" $FILENAME
