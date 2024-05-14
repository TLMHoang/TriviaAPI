# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

End point 

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET /questions`

- Description:
  - Retrieves a paginated list of questions along with category information.
- Request Arguments: page (optional): The page number (default is 1). Used for pagination.
- Response:
```json
{
  "success": true,
  "questions": [ 
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "Geography",
      "difficulty": 2 
    }
  ],
  "total_questions": 100,  
  "current_questions": 10, 
  "categories": [
    {"id": 1, "type": "Science"},
    {"id": 2, "type": "Art"},
  ],
  "current_category": null 
}
```

`DELETE /questions/<int:question_id>`

- Description: Deletes a specific question by its ID.
- Request Arguments
  - question_id (required, int): The ID of the question to be deleted.
- Response
```json
{
  "success": true,
  "deleted": 1  // The ID of the deleted question
}
```

`POST /questions`

- Description: Creates a new question.
- Request Body
  - question (required, string): The text of the question.
  - answer (required, string): The answer to the question.
  - category (required, int): The ID of the category the question belongs to.
  - difficulty (required, int): The difficulty level of the question (1-5).
```json
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "category": "Geography",
  "difficulty": 2 
}
```
- Respone:
```json
{
  "success": true,
  "created": 15  // The ID of the newly created question
}
```

`POST /questions/search`

- Description: earches for questions based on a search term and returns paginated results.
- Request Body:
  - searchTerm (string): The term to search for within the question text (case-insensitive).
```json
{
  "searchTerm": "capital"  
}
```
- Response:
```json
{
  "success": true,
  "questions": [ 
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "Geography",
      "difficulty": 2 
    }, 
  ],
  "total_questions": 5,  
  "current_questions": 5,
  "categories": [
    {"id": 1, "type": "Science"},
    {"id": 2, "type": "Art"},
  ],
  "current_category": null 
}
```

`GET /categories/<int:category_id>/questions`

- Description: Retrieves a paginated list of questions belonging to a specific category.
- Request Arguments
  - category_id (required, int): The ID of the category to filter questions by.
  - page (optional, int): The page number (default is 1). Used for pagination.
- Response:
```json
{
  "success": true,
  "questions": [ 
    {
      "id": 3,
      "question": "What is the highest mountain in the world?",
      "answer": "Mount Everest",
      "category": "Geography", 
      "difficulty": 3
    }, 
    
  ],
  "total_questions": 15, 
  "current_questions": 10,
  "categories": [
    {"id": 1, "type": "Science"},
    {"id": 2, "type": "Art"},
  ],
  "current_category": "Geography"
}
```

`POST /quizzes`

- Description: Retrieves a random question for a quiz, optionally filtered by category and excluding previously asked questions.

- Request Body:
  - quiz_category (optional, object): An object containing the id of the category to filter by. If not provided or if the ID is 0, questions from all categories will be considered.
  - previous_questions (optional, array of integers): An array of question IDs that have already been asked in the quiz.

```json
{
  "quiz_category": {"id": 3}, 
  "previous_questions": [5, 12, 21]
}
```
Response:
```json
{
  "success": true,
  "question": {
    "id": 25,
    "question": "What is the highest mountain in the world?",
    "answer": "Mount Everest",
    "category": "Geography", 
    "difficulty": 3
  }
}
```
Or
```json
{
  "success": true,
  "question": null  
}
```


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
