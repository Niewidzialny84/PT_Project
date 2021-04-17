# API
This is a API and the database schema that is used by server to get the needed data from db using endpoints.

## Info db:
If you want create new database please insert in CMD belowa commands:
1. python3
2. from API_PT import db
3. db.create_all()

## Info:
Link to POSTMAN: https://www.getpostman.com/collections/1d6a4248406e6ff0c984

# Endpoints:

## [POST] /api/users 
with json body (below example) to add new user
```
{
   "username": "multiEryk",
    "email": "multiEryk@wp.pl",
    "password": "123"
}
```
## [GET] /api/users 
without any arguments to get all user list

## [GET] /api/users?username=multiEryk 
with URI arg to get specific user 

## [PUT] /api/users?username=multiKorzych 
with URI arg and JSON body to modify elements of specific entity
```
{
	"username": "multiKorzych2",
	"email": "korzuszek@interia.pl",
	"password": "123"
}
```
## [PATCH] /api/users?username=multiKorzych2 
with URI arg and JSON body to modify password or email
```
{ 	
	"password": "1234"
}
```

## [DELET] /api/users?username=multiKorzych2 
with URI arg to remove from db specific user

## [POST] /api/history-manager  
with JSON body (first_username, second_username) to create new history entity
 
    {    	
	    "first_username": "multiEryk",
	    "second_username": "multiKorzych"
    }

## [POST] /api/history-manager -
with JSON body (history_id, username, content) to create new history entity

    {
            "history_id": "1",
        	"username": "multiEryk",
        	"content": "No Ello. Co tam?"
    }

## [GET] /api/history-manager 
without arg to get all history_content

## [GET] /api/history-manager?first_username=multiKorzych&second_username=multiEryk 
with URI args to get history_content for specific users

## [GET] api/history-manager/historyID?first_username=multiEryk&second_username=multiKorzych 
with URI args to get history_id for specific users
