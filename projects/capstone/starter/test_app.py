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

SUPERUSER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ink5MnZ0XzVuQTRyMlF1RHp5SnZPRyJ9.eyJpc3MiOiJodHRwczovL21hc3Rlcml3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjM2NTFhZTRjOGZkZmNkMTU1MzEwNzUiLCJhdWQiOiJUZXN0QXBpIiwiaWF0IjoxNzE0ODY0MjAxLCJleHAiOjE3MTQ5NTA2MDEsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidWg0YmRVUnBsNzFzTUZWaDRHTkNTY21OUjZqdjk0UVUiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.duj0SM4HVzAY74wTmgAbjSBsKc67t4VBU1lrbdXAY2xEal2Vmx3waknbluiKm0ullsbF9khvbb5ubPzPuIZKiA07tKtQ2h7YORlLKeYIO4Vstr15uKxpltAXMDxkmqdbJvA3171ZiTIWaa0IT3bEAog7AmsmgiWoG3hFKDILBdUG90MQVqiHDdIbBakxpB_tPUDgUA4UqBAE0l07J1VbSs-6Fr58kgCmC2slRpPa_CuA-2q0VvKsRk6NAJtO3gM6kdp_bH5P98jvtxXJM_mgn-wcKtEmi29Z06bLjyZSfRvI__v7-YdOLx8jdf2lWc3bTz1W4Rd9OpXnTw-8N_9MjQ'
VIEWER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ink5MnZ0XzVuQTRyMlF1RHp5SnZPRyJ9.eyJpc3MiOiJodHRwczovL21hc3Rlcml3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjM2ZDQ2ZjdjZDE0ZWI1ZWRkNDg2ZjQiLCJhdWQiOiJUZXN0QXBpIiwiaWF0IjoxNzE0ODY5NjgwLCJleHAiOjE3MTQ5NTYwODAsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidWg0YmRVUnBsNzFzTUZWaDRHTkNTY21OUjZqdjk0UVUiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.jP9dqEjJXRnUbhkPpjtma3Pd2V6YWeJn8jWasUKIW-aWUTQ9ySi07gO61b8vMM7A_cjRyYUX_AX4D-5CiA4nhNI7eaV_Hre_QKRHwUEMW6byXaZrxEgay_6GOzKu6p7EI9Gd2YLrFwSjo_Q64Diaocp5gcW0EsOEje0DQQZu3N9bn770akfCShrPIDeB4hwwxvskXWJZbA05lvrxa94UPOeS8fKnHSxeGsqVbxX4fuBDc3rKZtJ3G2ON9x30aBD_zPLfjNHrH4FZLBUgQIMDs1SSS471hB2iWDVx-O7peSCQRsyEwu1edR9nU__5QFD674AdeA8hWpTmhK0xiyQk4w'

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

