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
        self.database_path = "postgres://postgres:Leen448@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''
    A get request to the /questions endpoint should return a list of questions,
    number of total questions, current category, categories.
    '''

    def test_get_paginated_questions(self):
        response_object = self.client().get('/questions')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['categories'])

    '''
    A request for a non existent question should return a 404
    '''

    def test_404_get_paginated_questions(self):
        response_object = self.client().get('/questions?page=100000')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error'], 404)
        self.assertEqual(response_data['message'], "Not found")
    '''
    A get request to the /categories endpoint should return 
    a list of categories,number_of_categories.
    '''

    def test_get_category(self):
        response_object = self.client().get('/categories')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['categories'])
        self.assertTrue(response_data['number_of_categories'])

    '''
    A get request to the /categories/id/questions endpoint should return 
    a list of questions related to spicifed category, total_questions, current_category.
    '''

    def test_get_category_by_ID(self):
        response_object = self.client().get('/categories/3/questions')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['current_category'])

    '''
    A request for a non existent category should return a 404
    '''

    def test_404_get_category_by_ID(self):
        response_object = self.client().get('/categories/100/questions')
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error'], 404)
        self.assertEqual(response_data['message'], "Not found")

    def test_get_questions_by_searchterm(self):
        response_object = self.client().post(
            "/questions", json={"searchTerm": "name"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertEqual(response_data['current_category'], None)

    def test_404_get_questions_by_searchterm(self):
        response_object = self.client().post(
            "/questions", json={"searchTerm": "xyz"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['error'], 404)
        self.assertEqual(response_data['message'], "Not found")

    """A request to post a new question with all required parameters should return a 200 status code"""

    def test_success_post_new_question(self):
        response_object = self.client().post('/post_questions',
                                             json={
                                                 "question": "who am I?",
                                                 "answer": "it is me",
                                                 "category": 1,
                                                 "difficulty": 4})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['message'])

    """A request to post a new question with missing required parameters should return a 400 status code"""

    def test_400_post_new_question(self):

        response_object = self.client().post('/post_questions',
                                             json={"question": "",
                                                   "answer": "",
                                                   "category": None
                                                   })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')

    '''
        A request to delete a given question with the specified id should return a 200
        status code and should delete the question from the database
    '''
    def test_success_delete_question_based_on_id(self):

        response_object = self.client().delete("/questions/12")
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertTrue(response_data['message'])

    '''
        A request to delete a question with a 
        non-existent id should return a 400 status code
    '''

    def test_400_delete_non_existent_question(self):
        response_object = self.client().delete("/questions/1000000000")
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')

    """
    A request to get the next question in the quiz should a return a random question,
     within the given category, which is not within the list of previous question
    """

    def test_play_quiz(self):

        payload = {"previous_questions": [],
                   "quiz_category": {"id": 1}}
        endpoint = '/quizzes'
        response_object = self.client().post(endpoint, json=payload)
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        question_from_endpoint = response_data['question']

    def test_400_failure_get_questions_to_play_quiz(self):

        payload = {"previous_questions": {},
                   "quiz_category": {'id': None}}

        response_object = self.client().post('/quizzes', json=payload)
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
