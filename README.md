

# App description 
Python Script Executor organize bash scripts in order and executes them.
In case of error or input requirement, output input controller class perform desired actions.

# App installation

Poetry:

	python3 -m pip install poetry
	
App:

	cd python_script_executor
	python3 -m poetry install

# App usage 
Copy scripts You would like to execute to python_script_executor/scripts directory.

To order scripts add numbers preceded by `_` to their names ends. If numbers are missing
scripts will be executed randomly.

Script Name Examples:

	script_0.sh
	update-apt-get_1.sh
	update-upgrade_2.sh

To start app with default settings use:

	python start.py
	
Or using poetry

	python3 -m poetry run python start.py

