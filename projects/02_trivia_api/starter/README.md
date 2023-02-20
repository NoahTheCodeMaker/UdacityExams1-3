# Full Stack API Final Project - Noah Dragoon

# See Backend and Frontend README.md files for the app setup

## API Documentation

# API Introduction
```
Udacity enlisted me to create an API so that the employees and students could hold trivia sessions on a regular basis in order to bond. 

The API you now see is a result of my efforts, I hope you enjoy!

```

# Getting Started
```
In it's current state, this API is hosted completely locally, so the 
Base URL is http://127.0.0.1:5000/

There are no API Keys or Authentication in the apps current state.
```

# Error Messages
The error codes 400, 404, 405, 422, and 500 are the error codes most expected to occur in this app.
Keeping this in mind, here are the returned json responses for each code so you can expect them.

Response for Error Code 400
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
Response for Error Code 404
{
  "success": False,
  "error": 404,
  "message": "resource not found"
}
Response for Error Code 405
{
  "success": False,
  "error": 405,
  "message": "method not allowed"
}
Response for Error Code 422
{
  "success": False,
  "error": 422,
  "message": "unprocessable entity"
}
Response for Error Code 500
{
  "success": False,
  "error": 500,
  "message": "internal server error"
}

# API Resource Endpoint Library
```
All Endpoints
GET '/categories'
GET '/categories/<int:category>/questions'
GET '/questions'
GET '/questions/<int:id>'
POST '/questions'
POST '/questionsearch'
POST '/quizzes'
DELETE '/questions/<int:id>'

Endpoint Descriptions in order of list above
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with keys, "categories", that contains a object of id: category_string key:value pairs, and "success" that contains a True or False Boolean indicating success.
- Example Request: curl http://127.0.0.1:5000/categories
- Example Response:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

GET '/categories/<int:category>/questions'
- Fetches all questions with the category id given in the <int:category> field
- Request Arguments: The int passed in the <int:category> field in the URL, like so '/categories/5/questions'
- Returns: An object with following keys and values:
"current_category" contains the category type string,
"success" contains a True or False Boolean indicating success,
"total_questions" contains an int showing the total amount of questions within the category,
"questions" contains an object with the following keys and values::
    "question" contains a string with the question of the Question object,
    "answer" contains a string with the answer to the question within this object,
    "id" contains an int representing the primary key of the question in the database
    "category" contains the int representing the primary key of the category in the database
    "difficulty" contains the int representing the difficulty of this question on a 1-5 scale

- Example Request: curl http://127.0.0.1:5000/categories/5/questions
- Example Response:
{
  "current_category": "Entertainment", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }], 
  "success": true, 
  "total_questions": 3
}

GET '/questions'
- Fetches paginated questions 10 at a time or if on the last page, however many questions remain
- Request Arguments: this endpoint expects the query parameter of type int named "page", like so 'http://127.0.0.1:5000/questions?page=2',
this value will default to 1 if it is not supplied with the API call.
- Returns: An object with following keys and values:
"categories" contains an object with a single key, categories, that contains an object of id: category_string key: value pairs,
"current_category" contains the category type string,
"success" contains a True or False Boolean indicating success,
"total_questions" contains an int showing the total amount of questions,
"questions" contains an object with the following keys and values::
    "question" contains a string with the question of the Question object,
    "answer" contains a string with the answer to the question within this object,
    "id" contains an int representing the primary key of the question in the database
    "category" contains the int representing the primary key of the category in the database
    "difficulty" contains the int representing the difficulty of this question on a 1-5 scale

- Example Request: curl http://127.0.0.1:5000/questions?page=1
- Example Response:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "All", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 24
}

GET '/questions/<int:id>'
- Fetches the question with the id specified in <int:id>
- Request Arguments: The int passed in the <int:category> field in the URL, like so '/questions/15'
- Returns: An object with the following keys:
"success" contains a True or False Boolean indicating success,
"question" contains a string with the question of the Question object,
"answer" contains a string with the answer to the question within this object,
"id" contains an int representing the primary key of the question in the database
"category" contains the int representing the primary key of the category in the database
"difficulty" contains the int representing the difficulty of this question on a 1-5 scale

- Example Request: curl http://127.0.0.1:5000/questions/15
- Example Response: 
{
  "answer": "Agra",
  "category": 3,
  "difficulty": 2,
  "id": 15,
  "question": "The Taj Mahal is located in which Indian city?",
  "success": true
}

POST '/questions'
- Creates a new question in the database in the questions table
- Request Arguments: The new "question", "answer", "difficulty", and "category", all sent as strings under those key names, 
as well as the data header 'Content-Type: application/json', see example request for clarification
- Returns: An object with the following keys:
"success" contains a True or False Boolean indicating success
"question_id" returns an int indicating the primary key of the new question entry created

- Example Request: curl -d '{"question":"What Football team won the first Superbowl in 1967","answer":"The Green Bay Packers","difficulty":"3","category":"6"}' -H 'Content-Type: application/json' -X POST  http://127.0.0.1:5000/questions
- Example Response: 
{
  "question_id": 35,
  "success": true
}

POST '/questionsearch'
- Sends a search term that fetches all questions containing the search term
- Request Arguments: requires single key "searchTerm" with a string value pair which serves as the search term.
as well as the data header 'Content-Type: application/json', see example request for clarification
returns
- Returns: An object with the following keys, and "questions" being the objects that contained the search term:
"total_questions" contains an int showing the total amount of questions,
"success" contains a True or False Boolean indicating success.
"current_category" contains the category type string,
"questions" contains an object with the following keys and values::
    "question" contains a string with the question of the Question object,
    "answer" contains a string with the answer to the question within this object,
    "id" contains an int representing the primary key of the question in the database
    "category" contains the int representing the primary key of the category in the database
    "difficulty" contains the int representing the difficulty of this question on a 1-5 scale

- Example Request: curl -d '{"searchTerm":"team"}' -H 'Content-Type: application/json' -X POST  http://127.0.0.1:5000/questionsearch
- Example Response: 
{
  "current_category": "All",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "The Green Bay Packers",
      "category": 6,
      "difficulty": 3,
      "id": 35,
      "question": "What Football team won the first Superbowl in 1967"
    }
  ],
  "success": true,
  "total_questions": 2
}

POST '/quizzes'
- Sends data about previous questions and category to the backend which fetches a new question from the same category.
- Request Arguments: Requires 2 arguments passed in json. First, "quiz_category" which expects an object with the two keys "type" which is the category string, and "id" which is the category's id/primary key. Second, "previous_questions", which expects a list of all of the previous questions' ids/primary keys.
- Returns: A "success" message indicating success with a boolean, and a single randomized "question" object with the following key value pairs inside:
  "question" contains a string with the question of the Question object,
  "answer" contains a string with the answer to the question within this object,
  "id" contains an int representing the primary key of the question in the database
  "category" contains the int representing the primary key of the category in the database
  "difficulty" contains the int representing the difficulty of this question on a 1-5 scale

- Example Request: curl -d '{"previous_questions":[10],"quiz_category":{"type":"sports","id":6}}' -H 'Content-Type: application/json' -X POST  http://127.0.0.1:5000/quizzes
- Example Response: 
{
  "question": {
    "answer": "The Green Bay Packers",
    "category": 6,
    "difficulty": 3,
    "id": 35,
    "question": "What Football team won the first Superbowl in 1967?"
  },
  "success": true
}

DELETE '/questions/<int:id>'
- Deletes the question with the primary key provided in <int:id>
- Request Arguments: The int passed in the <int:id> field in the URL, like so '/questions/5'
- Returns: The "question_id" of the question deleted and a "success" message indicating success with a boolean.

- Example Request: curl -X DELETE  http://127.0.0.1:5000/questions/36
- Example Response:
{
  "question_id": 36, 
  "success": true
}
```