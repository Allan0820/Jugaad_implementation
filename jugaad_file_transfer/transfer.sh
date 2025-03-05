#!/bin/bash
value=1
if [ "$value" -gt 0  ]; then
   echo 'transfer service on'
   mv ./*.txt ../report/
fi
