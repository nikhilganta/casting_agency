from auth import AuthError
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug import exceptions

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjg5Mjk0Nzg5OTkxNTA0NjgxNiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjEwMjAyNTgsImV4cCI6MTYyMTAyNzQ1OCwiYXpwIjoib2NncEN6SzJ1M2hKMWlBbTdtaXBzSlFKMjlRMUZTUTEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Cs3ZaUYn6ZiPEi498Oj_F8X5yy78X0GhXZGu3RpE9-HldYKhEVlDt9wyTPLe9x62pZNL-koFGVtrA1zFjNHdma7QB_UhMMU9bwYzKv8i6gPw3hS4HRovbmOiiFXArroLvJYTUZjk6eHxgQJ6-iKKmINR0OWAXMH4zfrR72AqkaRbMq3VcHKKJ4KOCWn2PzMTrMC-X-SUrPoJstrAVCiFrnN55tT4MTnKOG8XivFKtJTPAvZbfHpNmjcQWNW6bc4bp2bSstSj1uMAJbscslVQJXURhf3VvFcBmDF-LQdRbb45BeASpnNz6inkmDsYysueXRXRsLwzsda6LKgNvWu1UA')
CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExODI5NzcwNDI3NTY0NDY3NTUyNCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjEwMTk0MjYsImV4cCI6MTYyMTAyNjYyNiwiYXpwIjoib2NncEN6SzJ1M2hKMWlBbTdtaXBzSlFKMjlRMUZTUTEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.CPmXu0PylOxQ_drBfugnrkfqIj4-ClmHAXM9hRnWugF0nRQ3d1WG5xNYR6-XgOmLI73gzwgBCyK1xkFTT-aqGHaohggI8y0BgKGegpZkFYTMsFJkxmItg62fbDuigahnVpUUQ4PHUc_2G7rgQIS9bOv1Ep-6JGk6mW3Aihw410LvCQa5IFo8eTjTd58YBlasMr2oV7E5h6zA1-h6bG6d0p3FWFgVGDL-qlnNLMok4cacQG2GpcbfJ1Iz62RG9nesTUsd5-rw9W_X0q6VTl0VI2hH7Iv96PHTOI0J_GwhMFqyWsizp0ii0t2L6iRmbk_cl-xo_4_dkPMlgk_SXiTJ1A')
EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDlhMGIzNTkyMDEzOTAwNjhlZDQ4YmQiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjIxMDIwMzAyLCJleHAiOjE2MjEwMjc1MDIsImF6cCI6Im9jZ3BDeksydTNoSjFpQW03bWlwc0pRSjI5UTFGU1ExIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.g5Dnm_8mEl4AsiEqO1RFZJVmfbSF-Ox9GEGD3Mu1DYptGURYMlpQvll5gE4hx6wqgZZK9H97ReBfFSXr3uuEHOd5H5hHx3d3bb3jGPIBbRtsVbYo7FaOAmuyET92jHvjxsvMomLxtzVPa2EYp16z7WUThmC09I20YqQ7Z0PTcishy2K4-R-BWZsf191uQ9_GpsY9Mf2KU98UP7LXMWHt8KRkzn5AJJS1CxIsJwptZ8ArQuuqUBwRVXaJK9PPqw4ycG4GWAtaCjTRZal34hC2Uk76r5rXcoKIs1TQpcEFR-IEFJALn8d2LM3OX3WIZyhV20wtWsdaBfG2JywmKnTqoA')
NO_PERMISSION_ROLE = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVnUzVJdGl0UjM0bWhfSW1yclQ0ZSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHlmc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDYxMTZlYjUwYTY3ZjAwNmIxODY2NDkiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjIxMDE5MTk0LCJleHAiOjE2MjEwMjYzOTQsImF6cCI6Im9jZ3BDeksydTNoSjFpQW03bWlwc0pRSjI5UTFGU1ExIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.As1r6296QrlhMQcX4bKYBV0QzM1OdTCa3sSIn1XIGd9DKNEJjXmPBDXQCzCccRSVIs-WEpUx6UjAJoID9FwNjiH5SIFwZb92j9TKB5q_I3SLY9gwK-SEJRY7ZguoI9tMk8tSaPlOgRAQ1xDtWiL5Mju58F31Bqiue-GzzB0pt_sAKV4ntZUx-UMkKRidRku4l5AN0khlcZq5OdVka1OjmBY-ZtfxXQtNuowIF1b9BDIGQYnRUT_L3zAWcugt-8OoguCpj6LqL1hTHdLO6V90iozLtGNFM9wsbEservKc4s-RSBo-9mg8v6cWV6M6-VhovgAjWQKScF8yqyMW7aG9xw')


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
            'release_date':'05-10-2021'
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