from auth import AuthError
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug import exceptions

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGFhZjgyYzU2NGY0NTAwNjlkN2RhYjEiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjIxODI2ODI5LCJleHAiOjE2MjE4MzQwMjksImF6cCI6Im9jZ3BDeksydTNoSjFpQW03bWlwc0pRSjI5UTFGU1ExIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.BjW-ySqlDgyztPsTd43V2961ewrPAKzjVgxk-3CzryeN9cX6YzdP7_QWYfcVm8hBo3U8hfGax62nKez4TQ40jf4DjEEbJBebAqqCN6haKklwksjGRlKd_Qktc-YLR5716XJoKqfTu9vzJnyPX2TCQGNqnO8KeAwbuOhZIa9wmsEKJPAqZapjDjAha1gSkd5TUalXZ-OrIFI1C6klSXpWXnCT9GFbuBOa_gp5RwOqXkBEOu7q-drkD3lnurwkrYN2qByAPMk9UuZ4p2xEgAqtuqBtl3mbbMTh6eSXx2Xvmk5bSUq2ZTdFMOyT8NKJ0rMjnTGNmk16wYXYqJyj11S4Zw')
CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGFhZjg1YzU2NGY0NTAwNjlkN2RhYmUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjIxODI4MjYyLCJleHAiOjE2MjE4MzU0NjIsImF6cCI6Im9jZ3BDeksydTNoSjFpQW03bWlwc0pRSjI5UTFGU1ExIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.EQMpFR32Gc1LiCRnTBkFya2w9LXKUXpa_5cX1tBcsCMgikVnBaicEi0vUgEyquOtJcUGzr_BQkByN1pu4JhDgu8EtfpFiB65n2pl4YWtwTHx1CwJ4JYUP9r-E8lCZmHMaBMh1B36N1hposPypoBX0WNWNbYxB0Pl0ezM46HWYNP0Ca4lT5ir1wOBTh_d0AWYXjoxLv5vQ8ptfqHy6D54s-VhYBFFQL4U3LR32U8g7ew3iMWV1ie1_aONqH8g938acXBzz9LqxOlB4fCfkV1V0f8tdnqebBZUBhsTlFWvxwBeSlWOn1IVx9-kwpBDX3cGrvf6L6o1xSpPaQiufaqcVg')
EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGFhZjg5NWIyMDBjNDAwNzExNmQ4YWIiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjIxODI4MzU4LCJleHAiOjE2MjE4MzU1NTgsImF6cCI6Im9jZ3BDeksydTNoSjFpQW03bWlwc0pRSjI5UTFGU1ExIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.DsKNCnbXVzSD8y1-7czEysBwluW_Zb3qo0rX_WKxVslDk4eSYuPZFq_urqZFP-fQu8fWIAh4SB3NhseFO73ylp4pDqu97I1nyBzu2YXqsqCj7lNvh95gUhLS9vQgZN6SHwqykMWl-W0huoAN4P_96Rbe3Cl5SQvZG08TUABwmr9HDhhVFiYe8rO3Dx-d_cI63o9k642TgQc8dCmoGhfR1sMY_J-qofzNpWDw2Hn26LVY3Zf7Ez0HMOcPgpgXke2FMH95WyUYbGp44bb385UhsMxmTTJINy3OCKsZiswOWY7pSeG7nFKM6_Q5slVtzSrbS7AnJBVcP-y4CZ66b8PcHA')
NO_PERMISSION_ROLE = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGFhZmM3Yjk1OWU4YTAwNjlhYzNlOWQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjIxODI4NDIxLCJleHAiOjE2MjE4MzU2MjEsImF6cCI6Im9jZ3BDeksydTNoSjFpQW03bWlwc0pRSjI5UTFGU1ExIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.hE84OdCM7Bags44uqhKRgp6lvrPiQU3Q2uVwPSjCRftMi785OhCK65WRMdzPATe4LJy7F6fZboWidOnpzuU4E-8aMj6JMxvVzrvuack3BxkDDILAk-KLbuR56NZYxCsPJ6LLOS_s0oWnAWXAI3UcvVy3SKQSPPzjTWh205kKE-GVndF88Rb2YtBpvHMjczsKzx2-tGeULn0l0Yl7Qyfh6_mTno7Zys1H89Kj-k4gQeJ_O2BefnT1j1RCoR23tqho47DuK4ePdKAcNXh4IX9LRx4Y6_MqBsw7UsgPuNQzarMEIeYeQWP2n6IPuAuQe5lf-lqMHOAN2fCZZRbX2c9J9A')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres', 'localhost:5432', self.database_name)
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
        res = self.client().get('/actors',
        headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['actors']), 0)

    def test_get_movies(self):
        res = self.client().get('/movies',
        headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreaterEqual(len(data['movies']), 0)

    def test_create_actors(self):
        res = self.client().post('/actors', json=self.new_actor,
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_create_movies(self):
        res = self.client().post('/movies', json=self.new_movie,
        headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_422_if_create_actor_data_is_none(self):
        res = self.client().post('/actors', json=self.new_actor_1,
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_create_movie_data_is_none(self):
        res = self.client().post('/movies', json=self.new_movie_1,
        headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_actors(self):
        self.test_create_actors()
        res = self.client().patch('/actors/2', json=self.new_actor_1,
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_update_movies(self):
        self.test_create_movies()
        res = self.client().patch('/movies/2', json=self.new_movie_1,
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_404_if_update_actor_is_none(self):
        res = self.client().patch('/actors/100', json=self.new_actor_1,
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_update_movie_is_none(self):
        res = self.client().patch('/movies/100', json=self.new_movie_1,
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actors(self):
        res = self.client().delete('/actors/1',
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], 1)

    def test_delete_movies(self):
        res = self.client().delete('/movies/1',
        headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], 1)

    def test_404_if_delete_actor_is_none(self):
        res = self.client().delete('/actors/100',
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_if_delete_movie_is_none(self):
        res = self.client().delete('/movies/100',
        headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # A role with no permissions cannot perform casting assistant actions
    def test_rbac_get_actors(self):
        res = self.client().get('/actors',
        headers={'Authorization': f'Bearer {NO_PERMISSION_ROLE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    def test_rbac_get_movies(self):
        res = self.client().get('/movies',
        headers={'Authorization': f'Bearer {NO_PERMISSION_ROLE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    # Casting Assistant cannot perform Casting director actions
    def test_rbac_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
        headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    def test_rbac_delete_actor(self):
        res = self.client().delete('/actors/1',
        headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    # Casting Director cannot perform Executive Producer actions
    def test_rbac_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

    def test_rbac_delete_movie(self):
        res = self.client().delete('/movies/1',
        headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')

if __name__ == "__main__":
    unittest.main()
