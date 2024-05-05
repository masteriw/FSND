# Casting Agency API

## Introduction
The Casting Agency API is a Flask application that enables users to manage actors and movies within a casting agency. This API allows for CRUD (Create, Read, Update, Delete) operations on actors and movies.

## Getting Started

### Prerequisites
- Python 3.9.19
- Flask
- SQLAlchemy
- Auth0 tokens are provided (for authentication and authorization)

### Installation
1. Clone the repository to your local machine.
2. Install the dependencies with `pip3 install -r requirements.txt`.
3. Set up the necessary environment variables, including `DATABASE_URL` and Auth0 credentials with the supplied tokens.

### Cloud Deployment
The project has been deployed in the following URL: https://fsnd-tgjk.onrender.com/
All endpoints are available there.
Here's an example of curl request that tests the get:actors endpoint:
```curl --request GET   --url https://fsnd-tgjk.onrender.com/actors   --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ink5MnZ0XzVuQTRyMlF1RHp5SnZPRyJ9.eyJpc3MiOiJodHRwczovL21hc3Rlcml3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjM2NTFhZTRjOGZkZmNkMTU1MzEwNzUiLCJhdWQiOiJUZXN0QXBpIiwiaWF0IjoxNzE0ODkyNTIwLCJleHAiOjE3MTc0ODQ1MjAsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoidWg0YmRVUnBsNzFzTUZWaDRHTkNTY21OUjZqdjk0UVUiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Rhj5-qolJRsbs4l5KckgzGaunuQi7O8Q7VlwGob2OWwQtV0iWhfpC6W551xtsG6J2s2hqINDJylEbvlhOP5lqq3xhPzIqiD5PihwFIHix8Mh7UshEXEYQ-0W44C1a-HIOsNLgKoXCi6QUmvO0bMELIk3b03tErH1aLOj1UxOYWHAja4jbwWG7CZXjM5guIc-2Voztguk5uJNwpkqQX0qJKzXrG5DYRFbOo5hU3XwQJxvsFjUiPvMt5jtHdoleLaSCCBr-45Gj6n1wBghuuBfudO2PnyYSf_muGALvZomGCA-U4UdVx0BG_Hg_BockyBmlD2I8AxgNpHL0iqy4eWwuQ'```

Please note that the Render hosting is a little slow while the instance initiates, due to being on the free tier.

### Running the Application
Run the command `flask run` to start the local server. The application will be available at `http://localhost:5000/`.

## API Endpoints
The API provides the following endpoints:

### Actors
- `GET /actors`: Retrieves a list of all actors.
- `POST /actors`: Adds a new actor.
- `DELETE /actors/<int:actor_id>`: Deletes an actor by ID.
- `PATCH /actors/<int:actor_id>`: Updates an actor by ID.

### Movies
- `GET /movies`: Retrieves a list of all movies.
- `POST /movies`: Adds a new movie.
- `DELETE /movies/<int:movie_id>`: Deletes a movie by ID.
- `PATCH /movies/<int:movie_id>`: Updates a movie by ID.

## Authentication and Authorization
Authentication is handled via JWT tokens provided by Auth0. Permissions are defined in Auth0 and verified by the API for each protected endpoint.

## Error Handling
The API returns errors in JSON format with the appropriate status code. Examples of errors include 400 (Bad Request), 404 (Not Found), 422 (Unprocessable Entity), and 500 (Internal Server Error).

## Tests
The `test.py` file contains a suite of unit tests that ensure the functionality of the Casting Agency API endpoints. The tests are designed to verify both successful operations and proper handling of error conditions. They simulate requests with and without proper authorization, and check the responses against expected outcomes.

### Test Commentary
- Tests for **Viewer** role verify that the user can retrieve actors and movies but cannot perform operations that require higher permissions, such as adding or deleting records.
- Tests for **Superuser** role ensure that the user can perform all operations, including adding and deleting actors and movies.
- The tests check for **HTTP status codes** and **response content** to confirm that the API behaves as expected.
- The use of **fixtures** ensures that the database is configured correctly for each test case.

### Running Tests
To run the tests, use the following command:

```pytest test.py```

## Contact
Vitor de Carvalho
E-mail: masteriw@gmail.com




