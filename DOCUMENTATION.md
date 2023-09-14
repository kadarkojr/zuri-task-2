# Fast API CRUD #


This documentation covers a FastAPI app that performs CRUD operations on a Postgres Database.
Listed in this documentation are:
  - Standard formats for requests and responses for each endpoint.
  - Sample usage of the API, including example requests and expected responses.
  - Limitations


## Endpoints

### Create
- *URL* : /api
- *Method* : post
- *Request Format* : JSON
user_id : person's id
name : name of person
- *Response Format* : JSON
user_id : person's id
name : name of person


### READ
- *URL* : /api
- *Method* : get
- *Response Format* : JSON
user_id : person's id
name : name of person



### Update
- *URL* : /api
- *Method* : put
- *Request Format* : JSON
user_id : person's id
name : name of person
- *Response Format* : JSON
user_id : person's id
name : name of person


### Delete
- *URL* : /api
- *Method* : delete
- *Request Format* : JSON
user_id : person's id
- *Response Format* : JSON
status code : 204


## Sample Usage

### Create

#### Request
- *POST*
- *'/https://url/api'

#### Response
- Status Code : 200
- { "user_id" : 1, "name" : "Kwabena Darko" }


### READ

#### Request
- *GET*
- *'/https://url/api/1'

#### Response
- Status Code : 200
- { "user_id" : 1, "name" : "Kwabena Darko" }


### UPDATE

#### Request
- *PUT*
- *'/https://url/api/1'
- { "user_id" : 1, "name" : "Kwabena Darko" }

#### Response
- Status Code : 200
- { "user_id" : 1, "name" : "Kwabena Darko" }


### DELETE

#### Request
- *DELETE*
- *'/https://url/api/1'

#### Response
- Status Code : 204


## Limitations
- Lack of Authentication/Authorization

