Python-based Rules Engine API

## Goals of the Project
Create an engine that will be able to evaluate data submitted to it on an ongoing basis.

## How to get started
- Pull this repository
- Create a virtual environment
- Activate the virtual environment
- Run `pip install -r requirements.txt` in your virtual environment to install dependencies
- Run `uvicorn data_validation:app --reload` to launch the server (port 8000 is default, can be overriden with --port)

## How to use
Send a POST JSON payload matching the specs in the Fact class to `/evaluate/{ruleset}` where ruleset is an existing ruleset in the file.
Return result will be whatever was specified in matching method for ruleset