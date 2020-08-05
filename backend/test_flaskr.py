import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://admin:0008@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'answer': 'Picasso',
            'category': 2,
            'difficulty': 1,
            'question': 'Who invented Cubism?'
        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    # test get endpoint
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 10)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    # test add endpoint
    def test_add_question(self):
        res = self.client().post('/add', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_add_question_not_allowed(self):
        res = self.client().get('/questions/200', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # test delete endpoint
    # change question id to 31 to run the delete test successfully
    def test_delete_question(self):
        res = self.client().delete('/questions/32')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 32).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 32)
        self.assertEqual(question, None)

    def test_405_question_does_not_exist(self):
        res = self.client().get('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # test search endpoint
    def test_search_question_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'World'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 2)

    def test_search_question_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'sky'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    """
    TODO_DONE
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
