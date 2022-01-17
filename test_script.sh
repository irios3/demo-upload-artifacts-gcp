WARNING_COUNT=150
METRICS_FILE="metrics.txt"
#echo warnings $WARNING_COUNT
#echo $WARNING_COUNT
THRESHOLD=100

if [ $WARNING_COUNT -ge $THRESHOLD ]; then
	echo "Number of warnings is $WARNING_COUNT. This is greater than threshold $THRESHOLD"
	exit 1
else
	echo "Number of warnings is $WARNING_COUNT. This is lower than threshold $THRESHOLD"
fi
