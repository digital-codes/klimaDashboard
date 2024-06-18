#!/usr/bin/bash
P=$(pwd)
echo "pwd: $P"
# header
cd $P/src/components/header/
if test -f card.json;
	then node $P/tools/mdCompile.cjs
else
	echo "No header"
fi
cd $P 
# footer
cd $P/src/components/footer/
if test -f card.json;
	then node $P/tools/mdCompile.cjs
else
	echo "No footer"
fi
cd $P 

for i in `ls -1 $P/src/components/tiles/`; do
    echo $i;
    cd $P/src/components/tiles/$i
    node $P/tools/mdCompile.cjs
    cd $P 
done
