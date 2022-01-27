# App description 
Python Script Executor organize scripts in order and executes them.
In case of error or input requirement, output input controller class perform desired actions.

It is mostly education project, so it is not free of unexpected behaviours like:
	bad recognizing of input need
	not catching output if script executed very quickly

# App usage 
To order scripts add numbers preceded by `_` to their names. If numbers are missing
scripts will be executed randomly.

Name Example:

	script_0.sh
	script_1.sh
	
To start app with default settings use:

	python start.py

# Conclusions
It is better to create bash script to execute another bash scripts in some order than use python for it.
