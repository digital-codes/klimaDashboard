#!/usr/bin/bash
P=$(pwd)
echo "pwd: $P"
for i in `ls -1 $P/src/components/tiles/`; do
    echo $i;
    cd $P/src/components/tiles/$i
    /opt/node20/bin/node $P/tools/mdCompile.cjs
    cd $P 
done

