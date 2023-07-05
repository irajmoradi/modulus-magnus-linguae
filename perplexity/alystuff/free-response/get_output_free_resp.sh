for dir in "free_resp_sample"/*; do
	for FILE in "$dir"/*; do 
		python free_resp_get_output.py $FILE
		done
done
