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
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db(self.app, self.database_path)

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Endpoint testing

    # Testing for category object
    def test_categories_endpoint(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # Test for category endpoint failure
    def test_categories_endpoint_failure(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405) 
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 405)

    # Testing for questions by category
    def test_category_selector_endpoint(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # Testing for questions by category endpoint failure
    def test_category_selector_endpoint_failure(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 404)

    # Testing for pagination endpoint
    def test_question_pagination_endpoint(self):
        res = self.client().get('/questions', json={'page': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    # Testing for pagination endpoint failure
    def test_question_pagination_endpoint_failure(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 404)

    # Extensive test for question deletion endpoint,
    # be sure to use the psql file so that there is 
    # a question with id 9 for this test, or it will fail.
    def test_question_delete_endpoint(self):
        res1 = self.client().get('/questions/9')
        data1 = json.loads(res1.data)
        res2 = self.client().delete('/questions/9')
        data2 = json.loads(res2.data)
        res3 = self.client().get('/questions/9')
        data3 = json.loads(res3.data)

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(data1['success'], True)
        self.assertTrue(data1['id'])
        self.assertTrue(data1['question'])
        self.assertTrue(data1['answer'])
        self.assertTrue(data1['category'])
        self.assertTrue(data1['difficulty'])

        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)
        self.assertTrue(data2['question_id'])

        self.assertEqual(res3.status_code, 404)
        self.assertEqual(data3['success'], False)
        self.assertTrue(data3['message'])
        self.assertTrue(data3['error'], 404)

    # Test for question deletion endpoint failure
    def test_question_delete_endpoint_failure(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 404)

    # Test for the creation of a question
    def test_question_create_endpoint(self):
        res1 = self.client().post('/questions', json=
        {'question':'testing question', 'answer':'testing answer',
         'difficulty': '2', 'category': '3'})
        data1 = json.loads(res1.data)
        res2 = self.client().get('/questions/{}'.format(data1['question_id']))
        data2 = json.loads(res2.data)

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(data1['success'], True)
        self.assertTrue(data1['question_id'])

        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)
        self.assertTrue(data2['id'])
        self.assertTrue(data2['question'])
        self.assertTrue(data2['answer'])
        self.assertTrue(data2['category'])
        self.assertTrue(data2['difficulty'])
        self.assertEqual(data2['id'], data1['question_id'])

    # Test for the failure of question creation,
    # generated by giving a nonexistent category id
    def test_question_create_endpoint_failure(self):
        res = self.client().post('/questions', json=
        {'question':'testing question', 'answer':'testing answer',
         'difficulty': '2', 'category': '8'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 422)

    # Test for search endpoint, only works after 
    # using the trivia.psql file before starting
    def test_question_search_endpoint(self):
        res = self.client().post('/questionsearch', json={'searchTerm': 'testing question'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

    # Testing for search endpoint failure,
    # generated by giving no search term
    def test_question_search_endpoint_failure(self):
        res = self.client().post('/questionsearch')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 422)

    # Test for the quizzes endpoint
    def test_quizzes_endpoint(self):
        res = self.client().post(
            '/quizzes', 
            json={
            'quiz_category': {"type": "sports","id": 6},
            'previous_questions': [10]
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["question"])
        self.assertEqual(data['question']["id"], 11)
    
    # Test for the quizzes endpoint failure, 
    # generated by giving a nonexistent category id
    def test_quizzes_endpoint_failure(self):
        res = self.client().post(
            '/quizzes', 
            json={
            'quiz_category': {"type": "sports","id": 8},
            'previous_questions': [10]
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422) 
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 422)

    # Error tests
    def test_400_bad_request(self):
        res = self.client().get('/400errortest')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_404_not_found(self):
        res = self.client().get('/animalworldgorillatreelionlamppostelephantman')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_422_unprocessable_entity(self):
        res = self.client().get('/422errortest')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_500_internal_server_error(self):
        res = self.client().get('/500errortest')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()