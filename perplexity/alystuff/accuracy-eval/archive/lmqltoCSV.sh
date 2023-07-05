for dir in quizType*; do
    if [ -d "$dir" ]; then
	python3 lmqltoCSV.py "$dir"
    fi
done
