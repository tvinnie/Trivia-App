## API Reference

### Getting Started
# Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

    Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
    Delete questions.
    Add questions and require that they include question and answer text.
    Search for questions based on a text query string.
    Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

-------------------------------------------------------------------
## Trivia API Backend

# Getting Started
# Installing Dependencies
    
    Python 3.7

Follow instructions to install the latest version of python for your platform in the python docs

    Virtual Enviornment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

    PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

    pip install -r requirements.txt

This will install all of the required packages we selected within the requirements.txt file.

    Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

    Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

    psql trivia < trivia.psql

Running the server
From within the backend directory first ensure you are working using your created virtual environment.

# To run the server, execute:

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

Setting the FLASK_APP variable to flaskr directs flask to use the flaskr directory and the __init__.py file to find the application.

-------------------------------------------------------------------------------
### Trivia API Frontend
# Getting Setup

    Installing Dependencies
    Installing Node and NPM
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download.

# Installing project dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:

npm install

--------------------------------------------------------------------
### Endpoints

Expected endpoints and behaviors

# GET '/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

Request Arguments: None

Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

        {
            'categories': { '1' : "Science",
            '2' : "Art",
            '3' : "Geography",
            '4' : "History",
            '5' : "Entertainment",
            '6' : "Sports" }
        }

# GET '/questions?page=${integer}'

Fetches a paginated set of questions, a total number of questions, all categories and current category string.

Request Arguments: page - integer

Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer',
                'difficulty': 5,
                'category': 2
            },
        ],
        'totalQuestions': 100,
        'categories': { '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports" },
        'currentCategory': 'History'
    }

# GET '/categories/${id}/questions'

Fetches questions for a cateogry specified by id request argument

Request Arguments: id - integer

Returns: An object with questions for the specified category, total questions, and current category string

    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer',
                'difficulty': 5,
                'category': 4
            },
        ],
        'totalQuestions': 100,
        'currentCategory': 'History'
    }

# DELETE '/questions/${id}'

Deletes a specified question using the id of the question

Request Arguments: id - integer

Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.


# POST '/quizzes'

Sends a post request in order to get the next question

Request Body:

    {
        'previous_questions': [1, 4, 20, 15]
        quiz_category': 'current category'
    }

Returns: a single new question object

    {
        'question': {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        }
    }

# POST '/questions'

Sends a post request in order to add a new question

Request Body:

    {
        'question':  'Heres a new question string',
        'answer':  'Heres a new answer string',
        'difficulty': 1,
        'category': 3,
    }

Returns: Does not return any new data

# POST '/questions'

Sends a post request in order to search for a specific question by search term

Request Body:

    {
        'searchTerm': 'this is the term the user is looking for'
    }

Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer',
                'difficulty': 5,
                'category': 5
            },
        ],
        'totalQuestions': 100,
        'currentCategory': 'Entertainment'
    }
