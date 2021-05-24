# Udacity Capstone Project - Casting Agency

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
- Sample: 

#### GET /actors
- General: Returns the list of actors present in the database
- Who can access: Casting Assistant, Casting Director, Executive Producer
#### GET /movies
- General: Returns the list of movies present in the database
- Who can access: Casting Assistant, Casting Director, Executive Producer

#### POST /actors
- General: Creates a new actor using new name, age and gender
- Who can access: Casting Director, Executive Producer
#### POST /movies
- General: Creates a new movie using new title and release date
- Who can access: Executive Producer

#### PATCH /actors/<int: id>
- General: Update the details of actor with an id = id using a new name, age or gender
- Who can access: Casting Director, Executive Producer
#### PATCH /movies/<int: id>
- General: Update the details of movie with an id = id using a new title or release date
- Who can access: Casting Director, Executive Producer

#### DELETE /actors/<int: id>
- General: Delete the actor with id = id if it exists from the database
- Who can access: Casting Director, Executive Producer
#### DELETE /movies/<int: id>
- General: Delete the movie with id = id if it exists from the database
- Who can access: Executive Producer