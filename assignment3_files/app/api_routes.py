from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app, db, api
from app.models import User, Movie
from werkzeug.security import check_password_hash

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        print("Received login data:", data)

        user = User.query.filter_by(username=data.get("username")).first()

        if user:
            print(f"User found: {user.username}")
            print(f"Stored password hash: {user.password}")

        if user and check_password_hash(user.password, data.get("password")):
            access_token = create_access_token(identity=str(user.id))
            print("Generated token:", access_token)
            return {"access_token": access_token}

        print("Invalid login attempt")
        return {"message": "Invalid credentials"}, 401

class MovieList(Resource):
    @jwt_required()
    def get(self):
        movies = Movie.query.all()
        return jsonify([{
            "id": movie.id,
            "name": movie.name,
            "year": movie.year,
            "awards": movie.awards,
            "genre": movie.genre
        } for movie in movies])

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_movie = Movie(
            name=data["name"],
            year=data["year"],
            awards=data["awards"],
            genre=data.get("genre", "Unknown")
        )
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({"message": "Movie added successfully!"})

class MovieResource(Resource):
    @jwt_required()
    def get(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return jsonify({
            "id": movie.id,
            "name": movie.name,
            "year": movie.year,
            "awards": movie.awards,
            "genre": movie.genre
        })

    @jwt_required()
    def put(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        data = request.get_json()
        movie.name = data.get("name", movie.name)
        movie.year = data.get("year", movie.year)
        movie.awards = data.get("awards", movie.awards)
        movie.genre = data.get("genre", movie.genre)

        db.session.commit()
        return jsonify({"message": "Movie updated successfully!"})

    @jwt_required()
    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": "Movie deleted successfully!"})

api.add_resource(UserLogin, "/api/login")
api.add_resource(MovieList, "/api/movies")
api.add_resource(MovieResource, "/api/movies/<int:movie_id>")
