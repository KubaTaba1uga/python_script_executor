from subprocess import Popen, PIPE

shell = Popen(
    "/home/taba1uga/Desktop/python_script_orchestrator/tests/scripts/python_input.py",
    stdin=PIPE,
)
