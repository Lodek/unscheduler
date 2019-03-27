export PYTHONPATH = ../unscheduler
tests = test_parsers test_building

all: $(tests)

$(patsubst %.py, %, $(tests)):
	echo '==================================================='
	python $@.py 2>&1 | tee $@.out

clean:
	rm *.out *.log
