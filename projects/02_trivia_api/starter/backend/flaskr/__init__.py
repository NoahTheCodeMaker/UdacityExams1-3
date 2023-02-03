import os
import traceback
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random, json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app)

  # CORS Set-up
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  # Categories endpoint giving key-value pairs
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
    try:
      categories = {}
      i = 0
      results = Category.query.all()
      for result in results:
        i = i + 1
        categories[i] = result.type
    except:
      traceback.print_exc()
    return jsonify ({
      "categories": categories
    })

  # Returns questions in a given category
  @app.route('/categories/<int:category>', methods=['GET'])
  def retrieve_from_category(category):
    try:
      questions = []
      answers = []
      difficulty = []
      question_object = []
      results = Question.query.filter(Question.category == str(category)).all()
      for result in results:
        questions.append(result.question)
        answers.append(result.answer)
        difficulty.append(result.difficulty)
        question_object.append({
          "question": result.question,
          "answer": result.answer,
          "difficulty": result.difficulty
        })
    except:
      traceback.print_exc()
    return jsonify ({
      "success": True,
      "category": category,
      "questions": questions,
      "answers": answers,
      "difficulty": difficulty,
      "questionObject": question_object,
      "total_questions": len(questions)
    })
    

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    try:
      questions = []
      query = Question.query.all()
      for question in query:
        questions.append({
          question
        })
    except:
      traceback.print_exc()
    return jsonify ({
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/400errortest', methods=['GET'])
  def test400():
    if request.method == 'GET':
      abort(400)

  @app.route('/422errortest', methods=['GET'])
  def test422():
    if request.method == 'GET':
      abort(422)

  @app.route('/500errortest', methods=['GET'])
  def test500():
    if request.method == 'GET':
      abort(500)

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400 

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable entity"
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500
  
  return app

    