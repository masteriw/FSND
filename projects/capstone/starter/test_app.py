import json
import os
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
import pytest

from app import app
from models import setup_db, Movie, Actor

# Configuração do banco de dados de teste e tokens
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

SUPERUSER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ink5MnZ0XzVuQTRyMlF1RHp5SnZPRyJ9.eyJpc3MiOiJodHRwczovL21hc3Rlcml3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjM2NTFhZTRjOGZkZmNkMTU1MzEwNzUiLCJhdWQiOiJUZXN0QXBpIiwiaWF0IjoxNzE0ODkyNTIwLCJleHAiOjE3MTc0ODQ1MjAsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidWg0YmRVUnBsNzFzTUZWaDRHTkNTY21OUjZqdjk0UVUiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Rhj5-qolJRsbs4l5KckgzGaunuQi7O8Q7VlwGob2OWwQtV0iWhfpC6W551xtsG6J2s2hqINDJylEbvlhOP5lqq3xhPzIqiD5PihwFIHix8Mh7UshEXEYQ-0W44C1a-HIOsNLgKoXCi6QUmvO0bMELIk3b03tErH1aLOj1UxOYWHAja4jbwWG7CZXjM5guIc-2Voztguk5uJNwpkqQX0qJKzXrG5DYRFbOo5hU3XwQJxvsFjUiPvMt5jtHdoleLaSCCBr-45Gj6n1wBghuuBfudO2PnyYSf_muGALvZomGCA-U4UdVx0BG_Hg_BockyBmlD2I8AxgNpHL0iqy4eWwuQ'
VIEWER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ink5MnZ0XzVuQTRyMlF1RHp5SnZPRyJ9.eyJpc3MiOiJodHRwczovL21hc3Rlcml3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjM2ZDQ2ZjdjZDE0ZWI1ZWRkNDg2ZjQiLCJhdWQiOiJUZXN0QXBpIiwiaWF0IjoxNzE0ODkyNTU0LCJleHAiOjE3MTc0ODQ1NTQsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidWg0YmRVUnBsNzFzTUZWaDRHTkNTY21OUjZqdjk0UVUiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.pW9SMQ67Qv70tIkNtAAQOdkSR3G_j9Zzh4UTzZAm8bjs-HmXbvph7AsgEfESsjmnGiKGo8N0uQ48NyN5KlW0Wfri9S3A3ij9zmiOU34we5PVokAjeHzlUlKstoHpQC-XyJkBz6r4wuyRhDYohydjpJoBJ7uAy0Hwyc8hhzBrWhJveIbeT5-J-yGAXqihWBHORzoWwsQ5bJTqiEngp98zG5gHtT9XCXtL-0WfMo9Dao1l0dNUI8ToPsKuV5RXqmKUQ9F4pzX3arKNOV93d8ugjpWkVQuxc7q0G9lQmgTQkQVROQyl1X3D-vUwvXwQheYFbfLaKJ4Y6vq-aetFhByLUA'

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    setup_db(app, database_path)

    with app.app_context():
        db = SQLAlchemy()
        db.init_app(app)
        db.create_all()

    yield app.test_client()

# Teste de sucesso para GET /actors
def test_get_actors(client: FlaskClient):
    res = client.get('/actors', headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    data = json.loads(res.data)

    assert res.status_code == 200
    assert len(data['actors']) > 0

# Teste de falha para GET /actors sem autorização
def test_get_actors_failure(client: FlaskClient):
    res = client.get('/actors')
    assert res.status_code == 401

# Teste de falha para GET /actors sem autorização
def test_get_movies_failure(client: FlaskClient):
    res = client.get('/movies')
    assert res.status_code == 401

# Teste de sucesso para GET /movies
def test_get_movies(client: FlaskClient):
    res = client.get('/movies', headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    data = json.loads(res.data)

    assert res.status_code == 200
    assert len(data['movies']) > 0

# Teste de falha para GET /movies sem autorização
def test_get_actors_failure(client: FlaskClient):
    res = client.get('/movies')
    assert res.status_code == 401

# Testes para a role Viewer
def test_viewer_get_actors(client: FlaskClient):
    res = client.get('/actors', headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    assert res.status_code == 200

def test_viewer_get_movies(client: FlaskClient):
    res = client.get('/movies', headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    assert res.status_code == 200

def test_viewer_post_actor_unauthorized(client: FlaskClient):
    res = client.post('/actors', json={'name': 'Test Actor', 'age': 30, 'gender': 'Male'}, headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    assert res.status_code == 403

def test_viewer_post_movie_unauthorized(client: FlaskClient):
    res = client.post('/movies', json={'name': 'Test Movie', 'release_date': '2024-01-01'}, headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    assert res.status_code == 403

def test_viewer_delete_movie_unauthorized(client: FlaskClient):
    res = client.delete('/movies/1', headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    assert res.status_code == 403

def test_viewer_delete_actor_unauthorized(client: FlaskClient):
    res = client.delete('/actors/1', headers={'Authorization': f'Bearer {VIEWER_TOKEN}'})
    assert res.status_code == 403

# Testes para a role Superuser
def test_superuser_post_actor(client: FlaskClient):
    res = client.post('/actors', json={'name': 'Test Actor', 'age': 30, 'gender': 'Male'}, headers={'Authorization': f'Bearer {SUPERUSER_TOKEN}'})
    assert res.status_code == 200

def test_superuser_post_movie(client: FlaskClient):
    res = client.post('/movies', json={'title': 'Old Movie', 'release_date': '1986-01-01'}, headers={'Authorization': f'Bearer {SUPERUSER_TOKEN}'})
    assert res.status_code == 200

def test_superuser_delete_movie(client):
    # Adicione um filme antes de deletar
    new_movie = {
        'title': 'Novo Filme',
        'release_date': '2024-01-01'
    }
    post_response = client.post('/movies', json=new_movie, headers={'Authorization': f'Bearer {SUPERUSER_TOKEN}'})
    assert post_response.status_code == 200
    data = post_response.get_json()
    movie_id = data['id']

    # Agora tente deletar o filme recém-adicionado
    delete_response = client.delete(f'/movies/{movie_id}', headers={'Authorization': f'Bearer {SUPERUSER_TOKEN}'})
    assert delete_response.status_code == 200

def test_superuser_delete_actor(client):
    # Adicione um ator antes de deletar
    new_actor = {
        'name': 'Novo Ator',
        'age': 30,
        'gender': 'Female'
    }
    post_response = client.post('/actors', json=new_actor, headers={'Authorization': f'Bearer {SUPERUSER_TOKEN}'})
    assert post_response.status_code == 200
    data = post_response.get_json()
    actor_id = data['id']

    # Agora tente deletar o filme recém-adicionado
    delete_response = client.delete(f'/movies/{actor_id}', headers={'Authorization': f'Bearer {SUPERUSER_TOKEN}'})
    assert delete_response.status_code == 200

