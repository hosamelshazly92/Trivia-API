import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  # app = Flask(__name__, instance_relative_config=True)
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origins', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
    
  '''
  @TODO_DONE: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.route('/categories')
  @cross_origin()
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'success': True,
      'categories': formatted_categories
    })

  '''
  @TODO_DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/questions')
  @cross_origin()
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.order_by(Question.id).all()
    formatted_questions = [question.format() for question in questions]

    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]

    dict_categories = {}
    for category in categories:
      dict_categories[category.id] = category.type

    # if (len(formatted_questions) == 0):
    if formatted_questions is None:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': dict_categories
      })

  '''
  @TODO_DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

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

  @app.route('/categories/<int:category_id>/questions')
  @cross_origin()
  def get_specific_categories(category_id):
    category = Category.query.filter(Category.id == category_id).one_or_none()

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.filter(Question.category == category.id).all()
    formatted_questions = [question.format() for question in questions]

    if category is None:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'current_category': category.type,
        'questions': formatted_questions,
        'total_questions': len(formatted_questions)
      })

  '''
  @TODO_DONE: 
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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    