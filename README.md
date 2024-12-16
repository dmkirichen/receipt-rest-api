# Receipt REST API

## Installation

It is better to use venv, after setting it up install all python dependencies using `pip install -r requirements.txt`

Also, you need to have working postgresql server, for now you will need to setup it for yourself and provide necessary details to variables in db_operations.py

After that, please run `.venv/Scripts/activate; cd src/; python db.py`

## Usage

You can run web-server with this command: `uvicorn main:app --reload --app-dir src/`

After that you can check what endpoints are implemented and test them using this page: http://127.0.0.1:8000/docs
