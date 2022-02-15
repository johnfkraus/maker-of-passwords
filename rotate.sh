#!/bin/sh
PASSWORD="pthree.org"
for i in `seq 1000`; do
    PASSWORD=`echo -n $PASSWORD | sha1sum - | awk '{print $1}'`
done
echo $PASSWORD


