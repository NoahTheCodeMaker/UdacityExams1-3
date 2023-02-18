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
      abort(500)
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
      abort(404)
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
      abort(404)
    return jsonify ({
      "success": True,
      "questions": questions,
      "total_questions": session.query(Question).count(),
      "categories": categories,
      "current_category": "All"
    })

  # Returns single question by ID
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
        abort(404)
    except:
      traceback.print_exc()
      abort(404)

  # Creates new question in the database using given data
  @app.route('/questions', methods=['POST'])
  def make_question():
    try:
      question = request.get_json().get("question", None)
      answer = request.get_json().get("answer", None)
      difficulty = request.get_json().get('difficulty', None)
      category = request.get_json().get("category", None)
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
      abort(422)
    return jsonify({
      "success": True,
      "question_id": new_question.id
      })

  # Deletes a question with the given question id and DELETE method
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter_by(id=id).one()
      question.delete()
      db.session.commit()
      return jsonify ({
      "success": True,
      "question_id": id
      })
    except:
      traceback.print_exc()
      db.session.rollback()
      abort(404)
    finally:
      db.session.close()
    

  # Question Search endpoint
  @app.route('/questionsearch', methods=['POST']) 
  def search_questions():
    try:
      questions = []
      question = request.get_json().get("searchTerm", None)
      results = Question.query.filter(Question.question.ilike("%{}%".format(question))).all()
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
      abort(422)
    return jsonify ({
      "success": True,
      "questions": questions,
      "total_questions": len(questions),
      "current_category": "All"
      })
  
  # Quiz endpoint for selecting random questions
  @app.route('/quizzes', methods=['POST']) 
  def play_quizzes():
    try:
      quiz_category = request.get_json().get("quiz_category", None)
      previous_questions = request.get_json().get("previous_questions", [])

      category_id = quiz_category["id"]
      current_category = Category.query.filter_by(id=category_id).all()
      if current_category is None:
        abort(404)

      if category_id == 0:
        question_bank = Question.query.all()
      else:
        question_bank = Question.query.filter_by(category=str(category_id)).order_by(Question.id).all()
      if len(question_bank) == 0:
        abort(422)

      final_questions = []
      for question in question_bank:
        if question.id not in previous_questions:
          final_questions.append(question.format())
      
      if len(final_questions) == 0:
        return jsonify({
          "success": True
        })
      else:
        current_question = random.choice(final_questions)
        previous_questions.append(current_question["id"])

        return jsonify({
          "success": True,
          "question": current_question
        })

    except:
      traceback.print_exc()
      abort(422)

  # Forcing errors for error tests

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

  # Error handlers

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

    