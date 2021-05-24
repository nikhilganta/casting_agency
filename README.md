# Udacity Capstone Project - Casting Agency

Project URL - [https://new-casting-agency.herokuapp.com](https://new-casting-agency.herokuapp.com)

## Introduction

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

It has three roles:
- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All the permissions that a casting assistant has
    - Add or delete an actor from the database
    - Modify actors and movies
- Executive Producer
    - All the permissions that a casting director has
    - Add or delete a movie from the database

## Getting Started

You need to have Python3, pip, node, and npm installed on your system for either developing or running the project

### Backend Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the main directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## API Reference

### Getting Started

- Base URL - 
- Authentication - [Auth0 Login Page](https://udacityfswd.us.auth0.com/authorize?audience=casting&response_type=token&client_id=ocgpCzK2u3hJ1iAm7mipsJQJ29Q1FSQ1&redirect_uri=http://localhost:8100/tabs/user-page)

- Casting Assistant
    - Username - casting.assistant@movie.com
    - Password - Casting@assistant
- Casting Director
    - Username - casting.director@movie.com
    - Password - Casting@director
- Executive Producer
    - Username - executive.producer@movie.com
    - Password - Executive@producer
- Customer
    - Username - customer@movie.com
    - Password - Customer@123

You can use the respective token from the header and perform the respective actions as mentioned previously

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Permission not found
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
Using postman, the below requests can be performed!

#### GET /
- General: Displays a json representing the Home Page!
- Sample request: https://new-casting-agency.herokuapp.com/
- Sample response:
```
{
    "message": "Home Page"
}
```

#### GET /actors
- General: Returns the list of actors present in the database
- Who can access: Casting Assistant, Casting Director, Executive Producer
- Sample request: GET https://new-casting-agency.herokuapp.com/actors
- Sample Response:
```
{
    "actors": [
        {
            "age": 25,
            "gender": "M",
            "id": 4,
            "name": "NIKHIL GANTA"
        },
        {
            "age": 50,
            "gender": "M",
            "id": 5,
            "name": "TONY START"
        }
    ],
    "success": true
}
```
#### GET /movies
- General: Returns the list of movies present in the database
- Who can access: Casting Assistant, Casting Director, Executive Producer
- Sample request: GET https://new-casting-agency.herokuapp.com/movies
- Sample response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sat, 03 May 2003 00:00:00 GMT",
            "title": "Iron Man 1"
        },
        {
            "id": 2,
            "release_date": "Tue, 03 May 2005 00:00:00 GMT",
            "title": "Iron Man 2"
        },
        {
            "id": 3,
            "release_date": "Thu, 03 May 2007 00:00:00 GMT",
            "title": "Iron Man 3"
        }
    ],
    "success": true
}
```

#### POST /actors
- General: Creates a new actor using new name, age and gender
- Who can access: Casting Director, Executive Producer
- Request Body:
```
{
    "name": "NIKHIL GANTA",
    "age": 25,
    "gender": "M"
}
```
- Sample request: https://new-casting-agency.herokuapp.com/actors
- Sample Response:
```
{
    "actors": [
        {
            "age": 25,
            "gender": "M",
            "id": 4,
            "name": "NIKHIL GANTA"
        }
    ],
    "success": true
}
```
#### POST /movies
- General: Creates a new movie using new title and release date
- Who can access: Executive Producer
- Request Body:
```
{
    "title": "Iron Man 1",
    "release_date": "05-03-2003"
}
```
- Sample request: POST https://new-casting-agency.herokuapp.com/movies
- Sample response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sat, 03 May 2003 00:00:00 GMT",
            "title": "Iron Man 1"
        }
    ],
    "success": true
}
```

#### PATCH /actors/<int: id>
- General: Update the details of actor with an id = id using a new name, age or gender
- Who can access: Casting Director, Executive Producer
- Request Body:
```
{
    "name": "Nikhil",
    "age": 26
}
```
- Sample request: PATCH https://new-casting-agency.herokuapp.com/actors/4
- Sample response:
```
{
    "actors": [
        {
            "age": 26,
            "gender": "M",
            "id": 4,
            "name": "Nikhil"
        }
    ],
    "success": true
}
```
#### PATCH /movies/<int: id>
- General: Update the details of movie with an id = id using a new title or release date
- Who can access: Casting Director, Executive Producer
- Request Body:
```
{
    "release_date": "12-10-2007"
}
```
- Sample request: PATCH https://new-casting-agency.herokuapp.com/movies/3
- Sample response:
```
{
    "movies": [
        {
            "id": 3,
            "release_date": "Mon, 10 Dec 2007 00:00:00 GMT",
            "title": "Iron Man 3"
        }
    ],
    "success": true
}
```
#### DELETE /actors/<int: id>
- General: Delete the actor with id = id if it exists from the database
- Who can access: Casting Director, Executive Producer
- Sample request: DELETE https://new-casting-agency.herokuapp.com/actors/5
- Sample response:
```
{
    "actor": 5,
    "success": true
}
```
#### DELETE /movies/<int: id>
- General: Delete the movie with id = id if it exists from the database
- Who can access: Executive Producer
- Sample request: DELETE https://new-casting-agency.herokuapp.com/movies/2
- Sample response:
```
{
    "movie": 2,
    "success": true
}
```