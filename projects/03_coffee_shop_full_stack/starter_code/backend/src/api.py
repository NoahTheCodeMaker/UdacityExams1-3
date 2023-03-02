import traceback
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import db, db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! The line below these comments will initialize
!! the database, running this function will add one.
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Comment this line after the first run or no data will keep
'''

db_drop_and_create_all()

## ROUTES

# Public drink viewing endpoint
@app.route('/drinks', methods=['GET'])
def drinks_viewer():
    try:
        drinks = []
        drinks_query  = Drink.query.all()
        for drink in drinks_query:
            drinks.append(drink.short())
        return jsonify ({
            "success": True,
            "drinks": drinks
        })
    except:
        traceback.print_exc()
        abort(500)

# Barista endpoint for viewing drink details
@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def drinks_detail_viewer(payload):
    try:
        drinks = []
        drinks_query  = Drink.query.all()
        for drink in drinks_query:
            drinks.append(drink.long())
        return jsonify ({
            "success": True,
            "drinks": drinks
        })
    except:
        traceback.print_exc()
        abort(500)

# Drink creation endpoint for Managers
@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def create_drinks(payload):
    if 'title' and 'recipe' not in request.get_json():
        abort(422)
    try:
        title = request.get_json().get('title', None)
        recipe = request.get_json().get('recipe', None)
        new_drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
        db.session.add(new_drink)
        db.session.commit()
        return jsonify({
            "success": True,
            "drink": [new_drink.long()]
        })
    except:
        db.session.rollback()
        traceback.print_exc()
        abort(422)
    finally:
      db.session.close()

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drinks(payload, id):
    try:
        title = request.get_json().get('title', None)
        recipe = request.get_json().get('recipe', None)
        drink = Drink.query.filter_by(id=id).one()
        drink.title = title
        drink.recipe = json.dumps(recipe)
        db.session.commit()
        return jsonify({
            "success": True,
            'drinks': [drink.long()]
        })
    except:
        traceback.print_exc()
        db.session.rollback()
        abort(404)
    finally:
      db.session.close()

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drinks(payload, id):
    try:
        drink = Drink.query.filter_by(id=id).one()
        drink.delete()
        db.session.commit()
    except:
        traceback.print_exc()
        db.session.rollback()
        abort(404)
    finally:
      db.session.close()
    return jsonify ({
        "success": True,
        "delete": id
    })

## Standard Error Handlers

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
  
@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

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

# Authorization error handler
@app.errorhandler(AuthError)
def auth_error(payload):
    return jsonify({
        "success": False,
        "error": payload.status_code,
        "message": payload.error
    }), payload.status_code

if __name__ == "__main__":
    app.debug = True
    app.run()
