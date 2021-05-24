from flask import Flask, jsonify, request, abort
from models import *
from auth import AuthError, requires_auth
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route("/")
    def casting_agency():
        return jsonify({
            "message": "Home Page"
        })

    @app.route("/actors", methods=["GET"])
    @requires_auth("get:actors")
    def get_actors(jwt):
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def create_actor(jwt):
        body = request.get_json()
        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)

        if new_name is None or new_gender is None or new_age is None:
            abort(422)
        else:
            try:
                actor = Actor(name=new_name, age=new_age, gender=new_gender)
                actor.insert()
                return jsonify({
                    "success": True,
                    "actors": [actor.format()]
                }), 200
            except:
                abort(422)

    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def update_actor(jwt, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor is None:
            abort(404)
        else:
            try:
                body = request.get_json()
                if body.get("name", None):
                    actor.name = body.get("name")
                if body.get("age", None):
                    actor.age = body.get("age")
                if body.get("gender", None):
                    actor.gender = body.get("gender")
                actor.update()
                return jsonify({
                    "success": True,
                    "actors": [actor.format()]
                }), 200
            except:
                abort(400)

    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(jwt, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor is None:
            abort(404)
        else:
            try:
                actor.delete()
                return jsonify({
                    "success": True,
                    "actor": id
                }), 200
            except:
                abort(400)

    @app.route("/movies", methods=["GET"])
    @requires_auth("get:movies")
    def get_movies(jwt):
        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def create_movie(jwt):
        body = request.get_json()
        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)

        if new_title is None or new_release_date is None:
            abort(422)
        else:
            try:
                movie = Movie(title=new_title, release_date=new_release_date)
                movie.insert()
                return jsonify({
                    "success": True,
                    "movies": [movie.format()]
                }), 200
            except:
                abort(422)

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def update_movie(jwt, id):
        movie = Movie.query.filter_by(id=id).one_or_none()
        if movie is None:
            abort(404)
        else:
            try:
                body = request.get_json()
                if body.get("title", None):
                    movie.title = body.get("title")
                if body.get("release_date", None):
                    movie.release_date = body.get("release_date")
                movie.update()
                return jsonify({
                    "success": True,
                    "movies": [movie.format()]
                }), 200
            except:
                abort(400)

    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(jwt, id):
        movie = Movie.query.filter_by(id=id).one_or_none()
        if movie is None:
            abort(404)
        else:
            try:
                movie.delete()
                return jsonify({
                    "success": True,
                    "movie": id
                }), 200
            except:
                abort(400)

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Permission not found"
        }), 403

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.description
        }), 401

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
