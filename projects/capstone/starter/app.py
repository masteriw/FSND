from flask import Flask, jsonify, request, abort
from models import setup_db, Movie, Actor
from flask_cors import CORS
from auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# Endpoint para obter todos os atores
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.all()
    return jsonify({
        'success': True,
        'actors': [actor.name for actor in actors]
    }), 200

# Endpoint para obter todos os filmes
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.all()
    return jsonify({
        'success': True,
        'movies': [{'id': movie.id, 'title': movie.title} for movie in movies],
    }), 200


# Endpoint para deletar um ator
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
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
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
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
@requires_auth('post:actors')
def add_actor(payload):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    actor = Actor(name=name, age=age, gender=gender)
    actor.insert()
    return jsonify({
        'success': True,
        'actor': actor.name,
        'id': actor.id
    }), 200

# Endpoint para adicionar um filme
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movie(payload):
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    movie = Movie(title=title, release_date=release_date)
    movie.insert()
    return jsonify({
        'success': True,
        'movie': movie.title,
        'id': movie.id
    }), 200

# Endpoint para atualizar um ator
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
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
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
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

# Error handler para AuthError
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Error handler para erro 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Recurso não encontrado"
    }), 404

# Error handler para erro 422
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Não processável"
    }), 422

# Error handler para erro 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Requisição inválida"
    }), 400

# Error handler para erro 405
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Método não permitido"
    }), 405

# Error handler para erro 500
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Erro interno do servidor"
    }), 500

# Error handler para outros erros
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, AuthError):
        return handle_auth_error(e)
    else:
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Ocorreu um erro inesperado"
        }), 500

if __name__ == '__main__':
    app.run()
