#!/usr/bin/bash
# get path of script
P=$(pwd)
echo "pwd: $P"

# Check if command line arguments are provided
if [ $# -gt 0 ]; then
	echo "Command line arguments:"
	for arg in "$@"; do
		echo "$arg"
	done
	# Get the full file path from the first command line parameter
	file_path="$1"
	# Extract the directory path
	directory_path=$(dirname "$file_path")
	echo "Compile in : $directory_path"
	cd $directory_path
	node $P/tools/mdCompile.cjs
	exit 0
else
	echo "Compile all"

	# sidebar. this is stuff to go into App.vue
	# so far, there is no MD content yet, only
	# localized messages
	cd $P/src/components/sidebar/
	if test -f card.json;
		then node $P/tools/mdCompile.cjs
	else
		echo "`pwd`: No header"
	fi



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
	# home
	cd $P/src/components/home/
	if test -f card.json;
		then node $P/tools/mdCompile.cjs
	else
		echo "No home"
	fi
	cd $P 
	# imprint
	cd $P/src/components/imprint/
	if test -f card.json;
		then node $P/tools/mdCompile.cjs
	else
		echo "No imprint"
	fi
	cd $P 
	# gdpr
	cd $P/src/components/gdpr/
	if test -f card.json;
		then node $P/tools/mdCompile.cjs
	else
		echo "No gdpr"
	fi
	cd $P 


	#for i in `ls -R -1 $P/src/components/tiles/`; do
	for i in `find $P/src/components/tiles -type d`; do
		echo $i;
		cd $i
		if test -f card.json;
			then node $P/tools/mdCompile.cjs
		else
			echo "Skipping `pwd`"
		fi
		cd $P 
	done

fi
