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
To order scripts add numbers preceded by `_` to their names. If numbers are missing
scripts will be executed randomly.

Name Example:

	script_0.sh
	script_1.sh
	
To start app with default settings use:

	python start.py
	
Or using poetry

	python3 -m poetry run python start.py

