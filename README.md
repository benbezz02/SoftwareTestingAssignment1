## Running the Project

Firstly, install any dependencies by running,

python setup.py install

Then, to run the project enter

python -u "file_directory/Assignment 1/src/main.py"

## Testing the Project

In order to run the tests, enter 

pytest -v

the -v argument just shows extra information and is not necessary

## View coverage

First run,

coverage run -m pytest

This can be viewed by running,

coverage report

and for a graphic html view of this report run,

coverage html

and open the htmlcov folder and open the index file