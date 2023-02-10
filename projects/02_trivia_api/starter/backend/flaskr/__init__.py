import os
import traceback
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
import random, json

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  Session = sessionmaker(bind = db.engine)
  session = Session()

  # CORS Set-up
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  # Creates Categories Object
  def categories_creator():
    categories = {}
    i = 0
    results = Category.query.all()
    for result in results:
      i = i + 1
      categories[i] = result.type
    return categories

  # Categories endpoint giving key-value pairs
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
    try:
      categories = categories_creator()
    except:
      traceback.print_exc()
    return jsonify ({
      "success": True,
      "categories": categories
    })

  # Returns questions in a given category
  @app.route('/categories/<int:category>/questions', methods=['GET'])
  def retrieve_from_category(category):
    try:
      questions = []
      category_string = Category.query.filter(Category.id == category).one()
      results = Question.query.filter(Question.category == str(category)).all()
      for result in results:
        questions.append({
          "id": result.id,
          "question": result.question,
          "answer": result.answer,
          "difficulty": result.difficulty,
          "category": result.category
        })
    except:
      traceback.print_exc()
    return jsonify ({
      "success": True,
      "questions": questions,
      "total_questions": len(questions),
      "current_category": category_string.type
    })

  # Returns paginated questions
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    try:
      categories = categories_creator()
      page = request.args.get("page", 1, type=int)
      questions = []
      query = Question.query.paginate(page=page , per_page=10)
      for question in query.items:
        questions.append({
          "id": question.id,
          "question": question.question,
          "answer": question.answer,
          "difficulty": question.difficulty,
          "category": question.category
        })
    except:
      traceback.print_exc()
    return jsonify ({
      "success": True,
      "questions": questions,
      "total_questions": session.query(Question).count(),
      "categories": categories,
      "current_category": "All"
    })

  # Returns single question
  @app.route('/questions/<int:id>', methods=['GET'])
  def retrieve_single_question(id):
    try:
      question = Question.query.filter(Question.id == id).all()
      if len(question) >= 1:
        return jsonify ({
        "success": True,
        "id": question[0].id,
        "question": question[0].question,
        "answer": question[0].answer,
        "category": question[0].category,
        "difficulty": question[0].difficulty
        })
      else:
        return jsonify ({
          "success": True,
          "error_message": "Question does not exist or has been deleted"
        })
    except:
      traceback.print_exc()

  # Creates new question in the database using given data
  @app.route('/questions', methods=['POST'])
  def make_question():
    try:
      question = request.get_json().get("question")
      answer = request.get_json().get("answer")
      difficulty = request.get_json().get('difficulty')
      category = request.get_json().get("category")
      new_question = Question(
        question=question,
        answer=answer,
        category=category,
        difficulty=difficulty
      )
      db.session.add(new_question)
      db.session.commit()
    except:
      db.session.rollback()
      traceback.print_exc()
    return jsonify({
      "success": True,
      "question_id": new_question.id
      })

  # Deletes a question with the given question id and DELETE method
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      Question.query.filter_by(id=id).delete()
      db.session.commit()
    except:
      traceback.print_exc()
      db.session.rollback()
    finally:
      db.session.close()
      return jsonify ({
      "success": True,
      "question_id": id
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questionsearch', methods=['POST']) 
  def search_questions():
    try:
      Question.query()
    except:
      traceback.print_exc()
    return jsonify ({
      "success": True,
      "question_id": id
      })
  
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

  @app.route('/quizzes', methods=['POST']) 
  def play_quizzes():
    try:
      Question.query()
    except:
      traceback.print_exc()
    return jsonify ({
      "success": True,
      "question_id": id
      })
      

  # Error Handlers

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

    