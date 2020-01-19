if (( $# < 1 ))
then
	echo "Usage : $0 filename"
	exit 0
fi

python3.6 Parser.py $1
python2 extractor.py 'text'
python3 to_graph.py 'graph'

