import os
from flask import Flask, request, abort, jsonify, redirect, url_for
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
  @TODO_DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origins', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
    
  '''
  @TODO_DONE: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.route('/categories')
  @cross_origin()
  def get_categories():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]

    dict_categories = {}
    for category in categories:
      dict_categories[category.id] = category.type

    paginate_categories = formatted_categories[start:end]

    if len(paginate_categories) == 0:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'categories': paginate_categories,
        'list_categories': dict_categories
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

    paginate_questions = formatted_questions[start:end]

    if len(paginate_questions) == 0:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': paginate_questions,
        'total_questions': len(paginate_questions),
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

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  @cross_origin()
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

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

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': dict_categories
      })

    except:
      abort(422)

  '''
  @TODO_DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/add', methods=['POST'])
  @cross_origin()
  def post_questions():
  
    body = request.get_json()

    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty')
    category = body.get('category')

    try:
      new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      
      new_question.insert()

      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.order_by(Question.id).all()
      formatted_questions = [question.format() for question in questions]

      return jsonify({
        'success': True,
        'created': new_question.id,
        'total_questions': len(formatted_questions)
      })
    
    except:
      abort(422)

  '''
  @TODO_DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  @cross_origin()
  def search_questions():

    body = request.get_json()

    try:
      searchTerm = body.get('searchTerm')

      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()
      # order_by(Question.id)
      formatted_questions = [question.format() for question in questions]

      categories = Category.query.order_by(Category.id).all()
      formatted_categories = [category.format() for category in categories]

      dict_categories = {}
      for category in categories:
        dict_categories[category.id] = category.type

      return jsonify({
        'success': True,
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': dict_categories
      })

    except:
      abort(400)

  '''
  @TODO_DONE: 
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

  @app.route('/play', methods=['POST'])
  @cross_origin()
  def play():
    
    body = request.get_json()
    
    try:
      quiz_category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')
      print(f'==========> {quiz_category}')
      
      if (quiz_category["id"] == 0):
        questions = Question.query.order_by(Question.id).all()
        previous_questions = [question.format() for question in questions]

        current_question = random.choice(previous_questions)
      else:
        questions = Question.query.filter(Question.category == quiz_category["id"]).all()
        previous_questions = [question.format() for question in questions]
        
        current_question = random.choice(previous_questions)
        print(f'==========> {current_question}')
        print(f'==========> {current_question["answer"]}')

      return jsonify({
        'success': True,
        'previousQuestion': previous_questions,
        'question': current_question
      })

    except:
      abort(400)

  '''
  @TODO_DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify ({
      'success': False,
      'error': 400,
      'message': "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify ({
      'success': False,
      'error': 404,
      'message': "resource not found"
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify ({
      'success': False,
      'error': 405,
      'message': "method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify ({
      'success': False,
      'error': 422,
      'message': "unprocessable"
    }), 422

  @app.errorhandler(500)
  def sever_error(error):
    return jsonify ({
      'success': False,
      'error': 500,
      'message': "internal server error"
    }), 500

  '''
  @TODO_DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    