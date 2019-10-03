export PYTHONPATH = ../unscheduler
tests = test_factory test_building test_tables test_info

all: $(tests)

$(patsubst %.py, %, $(tests)):
	echo '==================================================='
	python $@.py 2>&1 | tee $@.out

clean:
	rm *.out *.log
