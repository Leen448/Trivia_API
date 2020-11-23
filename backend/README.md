# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.


## API Reference

### Getting Started 
``` 
Base  URL: At present this app can only be run locally and not hosted as a base URL.
The backend app is hosted at the default, http://localhost:5000/ , set as a proxy in the fronted configuration.

Authentication: This version of the application docs not require authentication or API keys.

```
### Error Handling 
```
Error are returned as JSON objects in the following format:

{
"success": False,
 "error": 404,
 "message": "Not found"
}

The API will return three error type when requests fails :
- 400 : Bad Request 
- 404:  Resource Not Found
- 422:  Not Processable
- 500:  Internal Server Error
```

 ### Endpoint 

```
GET '/categories'
GET '/questions'
DELETE '/questions/<int:id>'
POST '/post_questions'
POST '/questions'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

```
```
GET '/categories'
- Fetches a dictionary of categories.
- Returns: A JSON object which includes categories and number of categories.
- Sample response: {
    "categories":
    ["Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"],
    "number_of_categories":6,
    "success":true
}
```
```
GET '/questions'
- Fetches a dictionary that contains a list of questions.
- Returns: A JSON object which includes categories, questions, and total number of questions.
- Sample response: {
    "categories":
    {"1":"Science",
    "2":"Art",
    "3":"Geography",
    "4":"History",
    "5":"Entertainment",
    "6":"Sports"
    },
    "current_category":null,
    "questions":[
        {"answer":"Maya Angelou",
        "category":4,
        "difficulty":2,
        "id":5,
        "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"}],
        "success":true,
        "total_questions":30
}
```
```
DELETE '/questions/<int:id>'
- Delete a question by ID.
- Returns: A JSON object which includes the question ID and message indicate the deletion.
- Sample response: {
    "message":"The question with ID: 1 was deleted successfully.",
    "success":true
}
```
```
POST '/post_questions'
- Store a new question in the database.
- Data needed: A JSON object that contain the following - question(string), answer(string), category(int), and difficulty(int).
- Sample request data: {
    "question": "Who I am?",
    "answer": "Robot",
    "category": 1,
    "difficulty": 1
}
- Returns: A JSON object which includes a message indicate the addition.
- Sample response: {
    "message":"The question: 'who am I?' has been added successfully.",
    "success":true
}
```
```
POST '/questions'
- Search for question in the database.
- Data needed: A JSON object containing the search term
- Sample request data: {
    "searchTerm": "cup"
}
- Returns: A JSON object which includes the question has the search term
- Sample response:{
    "current_category":null,
    "questions":[{"answer":"Muhammad Ali",
    "category":4 ,
    "difficulty":1 ,
    "id":9,
    "question":"What boxer's original name is Cassius Clay?"
    },
    {
    "answer":"Brazil",
    "category":6,
    "difficulty":3,
    "id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"
    }
    ],
    "success":true,
    "total_questions":2
    }
```
```
GET '/categories/<int:category_id>/questions'
- Returns a list of the questions available within a specific category.
- Returns: A JSON object which includes the a list of questions for the requested category.
- Sample response: {
    "current_category":"Sports",
    "questions":[{
        "answer":"Brazil",
        "category":6,
        "difficulty":3,
        "id":10,
        "question":"Which is the only team to play in every soccer World Cup tournament?"}],
        "success":true,
        "total_questions":1
}

```
```
POST '/quizzes'
- Returns a random question within the given category.
- Data needed: A JSON object containing the previous_questions(could be empty) and category(int).
- Sample request data: {
    "previous_questions": [],
    "quiz_category": 4,
}
- Returns: A JSON object which includes a question.
- Sample response: {
    "question":{
        "answer":"Edward Scissorhands",
        "category":5,
        "difficulty":3,
        "id":6,
        "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        "success":true
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
