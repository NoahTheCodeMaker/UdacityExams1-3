# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - I used Python 3.7.0 for this project, please use the same so there are no issues. Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql -d trivia -U postgres -a -f trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

see the '/frontend' README for the instructions on how to start the frontend.

## Testing
Because of the validations I have in place, the tests will only run correctly directly after running the psql file.
Keeping this in mind, to run the tests, run
```
dropdb trivia_test (In Windows on Visual Studio Code I had to use dropdb.exe -U postgres trivia_test)
createdb trivia_test (In Windows on Visual Studio Code I had to use createdb.exe -U postgres trivia_test)
psql trivia_test < trivia.psql (In Windows on Visual Studio Code I had to use psql.exe -U postgres trivia_test < trivia.psql)
python test_flaskr.py (This works fine)
```