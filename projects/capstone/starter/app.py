from flask import Flask, jsonify, request, abort
from models import setup_db, Movie, Actor
from flask_cors import CORS

app = Flask(__name__)
setup_db(app)
CORS(app)

# Endpoint para obter todos os atores
@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    return jsonify({
        'success': True,
        'actors': [actor.name for actor in actors]
    }), 200

# Endpoint para obter todos os filmes
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify({
        'success': True,
        'movies': [movie.title for movie in movies]
    }), 200

# Endpoint para deletar um ator
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        abort(404)
    actor.delete()
    return jsonify({
        'success': True,
        'deleted': actor_id
    }), 200

# Endpoint para deletar um filme
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
        abort(404)
    movie.delete()
    return jsonify({
        'success': True,
        'deleted': movie_id
    }), 200

# Endpoint para adicionar um ator
@app.route('/actors', methods=['POST'])
def add_actor():
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    actor = Actor(name=name, age=age, gender=gender)
    actor.insert()
    return jsonify({
        'success': True,
        'actor': actor.name
    }), 200

# Endpoint para adicionar um filme
@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    movie = Movie(title=title, release_date=release_date)
    movie.insert()
    return jsonify({
        'success': True,
        'movie': movie.title
    }), 200

# Endpoint para atualizar um ator
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
def update_actor(actor_id):
    body = request.get_json()
    actor = Actor.query.get(actor_id)
    if actor is None:
        abort(404)
    actor.name = body.get('name', actor.name)
    actor.age = body.get('age', actor.age)
    actor.gender = body.get('gender', actor.gender)
    actor.update()
    return jsonify({
        'success': True,
        'updated': actor_id
    }), 200

# Endpoint para atualizar um filme
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id):
    body = request.get_json()
    movie = Movie.query.get(movie_id)
    if movie is None:
        abort(404)
    movie.title = body.get('title', movie.title)
    movie.release_date = body.get('release_date', movie.release_date)
    movie.update()
    return jsonify({
        'success': True,
        'updated': movie_id
    }), 200

@app.route('/')
def index():
    return "Bem-vindo à Casting Agency!"

if __name__ == '__main__':
    app.run()
