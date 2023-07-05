for dir in "ch1-3_eval"/*; do
	for FILE in "$dir"/*; do 
		python3 get_accuracy.py $FILE
		done
done
