import os
from auth import AuthError
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug import exceptions

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = os.environ["CASTING_ASSISTANT"]
CASTING_DIRECTOR = os.environ["CASTING_DIRECTOR"]
EXECUTIVE_PRODUCER = os.environ["EXECUTIVE_PRODUCER"]
NO_PERMISSION_ROLE = os.environ["NO_PERMISSION_ROLE"]


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres',
                                                            'localhost:5432',
                                                            self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Nikhil Ganta',
            'age': 25,
            'gender': 'M'
        }

        self.new_actor_1 = {
            'name': 'Nikhil Ganta',
            'gender': 'M'
        }

        self.new_movie = {
            'title': 'Iron Man',
            'release_date': '05-10-2021'
        }

        self.new_movie_1 = {
            'title': 'Iron Man',
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        header = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        res = self.client().get('/actors', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['actors']), 0)

    def test_get_movies(self):
        header = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        res = self.client().get('/movies', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['movies']), 0)

    def test_create_actors(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_create_movies(self):
        header = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_422_if_create_actor_data_is_none(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().post('/actors', json=self.new_actor_1,
                                 headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_create_movie_data_is_none(self):
        header = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        res = self.client().post('/movies', json=self.new_movie_1,
                                 headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_actors(self):
        self.test_create_actors()
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().patch('/actors/2', json=self.new_actor_1,
                                  headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_update_movies(self):
        self.test_create_movies()
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().patch('/movies/2', json=self.new_movie_1,
                                  headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_404_if_update_actor_is_none(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().patch('/actors/100', json=self.new_actor_1,
                                  headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_update_movie_is_none(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().patch('/movies/100', json=self.new_movie_1,
                                  headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actors(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().delete('/actors/1', headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], 1)

    def test_delete_movies(self):
        header = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        res = self.client().delete('/movies/1', headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], 1)

    def test_404_if_delete_actor_is_none(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().delete('/actors/100', headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_delete_movie_is_none(self):
        header = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        res = self.client().delete('/movies/100', headers=header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # A role with no permissions cannot perform casting assistant actions
    def test_rbac_get_actors(self):
        header = {'Authorization': f'Bearer {NO_PERMISSION_ROLE}'}
        res = self.client().get('/actors', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    def test_rbac_get_movies(self):
        header = {'Authorization': f'Bearer {NO_PERMISSION_ROLE}'}
        res = self.client().get('/movies', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    # Casting Assistant cannot perform Casting director actions
    def test_rbac_create_actor(self):
        header = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    def test_rbac_delete_actor(self):
        header = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        res = self.client().delete('/actors/1', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    # Casting Director cannot perform Executive Producer actions
    def test_rbac_create_movie(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    def test_rbac_delete_movie(self):
        header = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        res = self.client().delete('/movies/1', headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')


if __name__ == "__main__":
    unittest.main()
