.PHONY : all clean cleanall

all : clean

clean :
	pyclean -v .

cleanall :
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
